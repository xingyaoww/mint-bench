
//Formatter to generate charts
var chartFormatter = function (cell, formatterParams, onRendered) {
    var content = document.createElement("span");
    var values = cell.getValue();

    //invert values if needed
    if (formatterParams.invert) {
        values = values.map(val => val * -1);
    }

    //add values to chart and style
    content.classList.add(formatterParams.type);
    content.inneHrTML = values.join(",");

    //setup chart options
    var options = {
        width: 50,
        // min: 0.0,
        // max: 100.0,
    }

    if (formatterParams.fill) {
        options.fill = formatterParams.fill
    }

    //instantiate piety chart after the cell element has been aded to the DOM
    onRendered(function () {
        peity(content, formatterParams.type, options);
    });

    return content;
};


var colorFormatter = function (cell, formatterParams) {
    var value = cell.getValue();

    // Check for the specific string "-"
    if (value === "-") {
        return value;
    }

    // Default values
    var defaults = {
        min: 0.0,
        max: 100.0,
        startColor: { r: 255, g: 255, b: 255 },
        endColor: { r: 107, g: 142, b: 35 }
    };

    // Override defaults with provided formatterParams values
    var min = (formatterParams && formatterParams.min) || defaults.min;
    var max = (formatterParams && formatterParams.max) || defaults.max;
    var startColor = (formatterParams && formatterParams.startColor) || defaults.startColor;
    var endColor = (formatterParams && formatterParams.endColor) || defaults.endColor;

    // Normalize the value between 0 and 1
    var normalizedValue = (value - min) / (max - min);

    // Compute the color gradient 
    var red = Math.floor(startColor.r + (endColor.r - startColor.r) * normalizedValue);
    var green = Math.floor(startColor.g + (endColor.g - startColor.g) * normalizedValue);
    var blue = Math.floor(startColor.b + (endColor.b - startColor.b) * normalizedValue);

    // make sure the value is rounded to 1 decimal place
    value = parseFloat(value).toFixed(1)

    return "<span style='display: block; width: 100%; height: 100%; background-color: rgb(" + red + ", " + green + ", " + blue + ");'>" + value + "</span>";
}


var barColorFn = function (value, formatterParams) {
    var defaults = {
        range : [-50, 50],
        low: { r: 255, g: 100, b: 150 },
        high: { r: 150, g: 255, b: 150 }
    };

    // Override defaults with provided formatterParams values

    var low_range = (formatterParams && formatterParams.range[0]) || defaults.range[0];
    var high_range = (formatterParams && formatterParams.range[1]) || defaults.range[1];
    var low = (formatterParams && formatterParams.low) || defaults.low;
    var high = (formatterParams && formatterParams.high) || defaults.high;

    // Clamp the value to the range [-100, 100]
    value = Math.max(low_range, Math.min(high_range, value));
    var range = high_range - low_range;

    // Normalize the value to the range [0, 1]
    var normalizedValue = (value + range / 2) / range;
    // Interpolate between the two colors based on the normalized value
    var interpolated = {
        r: Math.floor(low.r + (high.r - low.r) * normalizedValue),
        g: Math.floor(low.g + (high.g - low.g) * normalizedValue),
        b: Math.floor(low.b + (high.b - low.b) * normalizedValue)
    };

    return 'rgba(' + interpolated.r + ',' + interpolated.g + ',' + interpolated.b + ',0.9)';
}

document.addEventListener('DOMContentLoaded', function () {
    Promise.all([
        fetch('website/data/benchmark.json').then(response => response.json()),
        fetch('website/data/feedback_comparison.json').then(response => response.json())
    ])
        .then(([benchmark_tabledata, benchmark_feedback_efficancy_tabledata]) => {

            // 1. Benchmark Table
            benchmark_tabledata.forEach(row => {
                row.line = [row['1'], row['2'], row['3'], row['4'], row['5']]
            })

            var table = new Tabulator("#benchmark-table", {
                data: benchmark_tabledata,
                layout: "fitDataFill",
                movableColumns: false,
                initialSort: [
                    { column: "5", dir: "desc" },
                ],
                columnDefaults: {
                    tooltip: true,
                },
                columns: [
                    { title: "Model Family", field: "model", widthGrow: 1 },
                    { title: "Size", field: "size" },
                    { title: "Type", field: "type" },
                    {//create column group
                        title: "Tool-augmented Task-Solving Success Rate (within k turns)",
                        columns: [
                            { title: "k = 1", field: "1", hozAlign: "center", formatter: colorFormatter },
                            { title: "k = 2", field: "2", hozAlign: "center", formatter: colorFormatter },
                            { title: "k = 3", field: "3", hozAlign: "center", formatter: colorFormatter },
                            { title: "k = 4", field: "4", hozAlign: "center", formatter: colorFormatter },
                            { title: "k = 5", field: "5", sorter: "number", hozAlign: "center", formatter: colorFormatter },
                            { title: "Slope", field: "Slope", sorter: "number" },
                        ],
                    },
                    {//create column group
                        title: "Ability to Leverage Language Feedback",
                        columns: [
                            {
                                title: "k = 5 (+Feedback)", field: "Success Rate (5 turn) w\/ GPT-4 Feedback",
                                hozAlign: "center", formatter: colorFormatter
                            },
                            { title: "&Delta;Feedback", field: "Delta Feedback" },
                        ],
                    },
                ],
            });

            // 2. Benchmark Feedback Efficancy Table
            benchmark_feedback_efficancy_tabledata.forEach(row => {
                row.model = row.feedback_provider_info.model;
                row.size = row.feedback_provider_info.size;
                row.type = row.feedback_provider_info.type;
            })

            var feedback_efficacy_table = new Tabulator("#benchmark-feedback-efficancy-table", {
                data: benchmark_feedback_efficancy_tabledata,
                layout: "fitDataFill",
                movableColumns: false,
                initialSort: [
                    { column: "evaluated_LLM_feedback", dir: "desc" },
                ],
                columnDefaults: {
                    tooltip: true,
                },
                columns: [
                    {
                        title: "Feedback Provider",
                        columns: [
                            { title: "Model Family", field: "model", widthGrow: 1 },
                            { title: "Size", field: "size" },
                            { title: "Type", field: "type" }
                        ]
                    },
                    {
                        title: "&Delta; Task Success Rate compared to GPT-3.5",
                        field: "SR5_difference",
                        formatter: "progress",
                        sorter: "number",
                        formatterParams: {
                            min: -50, max: 50,
                            legend: true,
                            color: barColorFn,
                        },
                    },
                    {
                        title: "&Delta; GPT-3.5 Success Rate with Provided Feedback",
                        field: "evaluated_LLM_feedback",
                        sorter: "number",
                        formatter: "progress",
                        // width: 100,
                        formatterParams: {
                            min: -30, max: 30,
                            legend: true,
                            color: barColorFn
                        },

                    },
                ]
            });
        });

})

