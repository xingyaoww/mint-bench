
//Formatter to generate charts
var chartFormatter = function(cell, formatterParams, onRendered){
    var content = document.createElement("span");
    var values = cell.getValue();

    //invert values if needed
    if(formatterParams.invert){
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

    if(formatterParams.fill){
        options.fill = formatterParams.fill
    }

    //instantiate piety chart after the cell element has been aded to the DOM
    onRendered(function(){
        peity(content, formatterParams.type,  options);
    });

    return content;
};


var colorFormatter = function(cell) {
    var value = cell.getValue();
    
    // Check for the specific string "-"
    if (value === "-") {
        return value;
    }

    // Determine your float range here. 
    // For instance, if the float range is between 0 to 10:
    var min = 0.0;
    var max = 100;

    // Default colors - blue to red
    // 	107, 142, 35
    var startColor = { r: 255, g: 255, b: 255 };
    var endColor = { r: 107, g: 142, b: 35 };

    // Clamp value to the range for safety
    value = Math.max(min, Math.min(max, value));

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


document.addEventListener('DOMContentLoaded', function () {
    fetch('website/data/benchmark.json')
        .then(response => response.json())
        .then(tabledata => {
            console.log(tabledata)
            // add a field into each row as "line" to be used for the chart
            tabledata.forEach(row => {
                row.line = [row['1'], row['2'], row['3'], row['4'], row['5']]
            })
            // // make sure each value is a float with two digits
            // tabledata.forEach(row => {
            //     Object.keys(row).forEach(key => {
            //         if (key != "model" && key != "size") {
            //             row[key] = parseFloat(row[key]).toFixed(2)
            //         }
            //     })
            // })

            var table = new Tabulator("#benchmark-table", {
                data: tabledata,           //load row data from array
                layout: "fitDataFill",
                // textSize: "14px",
                movableColumns: false,      //allow column order to be changed
                initialSort: [             //set the initial sort order of the data
                    { column: "5", dir: "desc" },
                ],
                columnDefaults: {
                    tooltip: true,         //show tool tips on cells
                },
                columns: [                 //define the table columns
                    { title: "Model Family", field: "model", widthGrow:1},
                    { title: "Size", field: "size"},
                    { title: "Type", field: "type"},
                    {//create column group
                        title:"Tool-augmented Task-Solving Success Rate (within k turns)",
                        columns:[
                            {title:"k = 1", field:"1", hozAlign:"center", formatter: colorFormatter},
                            {title:"k = 2", field:"2", hozAlign:"center", formatter: colorFormatter},
                            {title:"k = 3", field:"3", hozAlign:"center", formatter: colorFormatter},
                            {title:"k = 4", field:"4", hozAlign:"center", formatter: colorFormatter},
                            {title:"k = 5", field:"5", sorter:"number", hozAlign:"center", formatter: colorFormatter},
                            {title:"Slope", field:"Slope", sorter:"number"},
                            // {title:"Line Chart", field:"line", width: 50, formatter:chartFormatter, formatterParams: {type:"line"}},
                            // {title: "Bar", field: "line", width: 50, formatter: chartFormatter, formatterParams: { type: "bar"} },
                        ],
                    },
                    {//create column group
                        title:"Ability to Leverage Language Feedback",
                        columns:[
                            {title:"k = 5 (+Feedback)", field:"Success Rate (5 turn) w\/ GPT-4 Feedback", hozAlign:"center", formatter: colorFormatter},
                            {title:"&Delta;Feedback", field:"Delta Feedback"},
                        ],
                    },
                ],
            });
            return table;
        });

})

