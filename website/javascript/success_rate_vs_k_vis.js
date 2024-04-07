let sr_vs_k_series;
let chart = null;

const color_Tableau20 = ['#4E79A7', '#A0CBE8', '#F28E2B', '#FFBE7D', '#59A14F', '#8CD17D', '#B6992D', '#F1CE63', '#499894', '#86BCB6', '#E15759', '#FF9D9A', '#79706E', '#BAB0AC', '#D37295', '#FABFD2', '#B07AA1', '#D4A6C8', '#9D7660', '#D7B5A6']


function isColliding(yValue, yAdjust, occupiedPositions) {
    // Check if the given position is already occupied.
    // We use a tolerance of +/- 1 for this example.
    const tolerance = 1;

    for (let pos of occupiedPositions) {
        if (Math.abs((yValue + yAdjust) - pos) <= tolerance) {
            return (yValue + yAdjust) >= pos ? 'up' : 'down';
        }
    }

    return null;
}

function hexToRGBA(hex, alpha = 1) {
    // Remove the hash if it exists
    hex = hex.replace('#', '');

    // Convert 3-digit to 6-digit format
    if (hex.length === 3) {
        hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    }

    // Extract the red, green, and blue components
    const r = parseInt(hex.slice(0, 2), 16);
    const g = parseInt(hex.slice(2, 4), 16);
    const b = parseInt(hex.slice(4, 6), 16);

    // Return the RGBA string
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}


function createChart(subsetNames, annotate_model_name = true) {

    if (chart) {
        chart.destroy();
    }

    const ctx = document.getElementById('chart-sr-vs-k');
    // filter the series
    const sr_vs_k_series_subset = sr_vs_k_series.filter(series => subsetNames.includes(series.label));

    // assign colors
    sr_vs_k_series_subset.forEach((series, index) => {
        series.borderColor = color_Tableau20[index];
        series.backgroundColor = color_Tableau20[index];
    });

    // Generate annotations for the data
    // Each annotation is:
    // {
    //     label1: {
    //       type: 'label',
    //       xValue: 2.5,
    //       yValue: 60,
    //       backgroundColor: 'rgba(245,245,245)',
    //       content: ['This is my text', 'This is my text, second line'],
    //       font: {
    //         size: 18
    //       }
    //     }
    //   }
    let annotations_for_data = {};
    let occupiedPositions = [];
    let extra_plugin_args = {};
    if (annotate_model_name) {
        sr_vs_k_series_subset.forEach((series, index) => {
            const label = series.label;
            const data = series.data;
            // use the last data point as the annotation point
            const yValue = data[data.length - 2]; // annotate above the data point

            let yAdjust = 0;
            let direction;
            let count = 0;
            while (direction = isColliding(yValue, yAdjust, occupiedPositions)) {
                if (direction === 'down') {
                    yAdjust -= 1;  // Move label upwards
                }
                else if (direction === 'up') {
                    yAdjust += 1;  // Move label downwards
                }
                else {
                    break;
                }
                count++;
                if (count > 10) {
                    break;
                }
            }

            occupiedPositions.push(yValue + yAdjust);  // Add the new position to the list

            annotations_for_data[label] = {
                type: 'label',
                // color: series.borderColor,
                padding: 0,
                xValue: 3 + 0.2,
                yValue: yValue + yAdjust,
                backgroundColor: hexToRGBA(series.backgroundColor, 0.8),
                content: [label],
                font: {
                    size: 10
                }
            }
        });
    } else {
        extra_plugin_args = {
            subtitle: {
                display: true,
                text: "You can click on the legend to hide or show a model's performance.",
                font: {
                    size: 12,
                }
            },
        }
    }



    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [1, 2, 3, 4, 5], // Assuming k values range from 1 to 5
            datasets: sr_vs_k_series_subset  // Assuming sr_vs_k_series is already formatted for Chart.js
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Max number of interaction turns allowed (k)',
                        font: {
                            size: 14,
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Success Rate with k-turn of Interaction (%)',
                        font: {
                            size: 14,
                        }
                    }
                }
            },
            plugins: {
                annotation: {
                    annotations: {
                        ...annotations_for_data,
                    }
                },
                colors: {
                    enabled: false,
                },
                legend: {
                    display: true,
                    labels: {
                        usePointStyle: true,
                        font: {
                            size: 10,
                        }
                    },
                    align: 'center',
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    position: 'nearest',
                    intersect: false,
                    itemSort: function (a, b) {
                        return b.raw - a.raw;
                    },
                    callbacks: {
                        title: function (context) {
                            return 'Max interaction turns k=' + context[0].label;
                        },
                        label: function (context) {
                            let label = context.dataset.label || '';

                            if (label) {
                                label += ': ';
                            }
                            label += context.formattedValue + '%';
                            return label;
                        }
                    }
                },
                title: {
                    display: true,
                    text: "LLM's task success rate with different interaction budget k",
                    font: function (context) {
                        var width = context.chart.width;
                        var size = Math.round(width / 32);
                        size = Math.min(size, 16);
                        return {
                            size: size
                        };
                    }
                },
                ...extra_plugin_args,
            }
        },

    });
}

const default_order = [
    'gpt-3.5-turbo-0613 (closed-source)',
    'claude-2 (closed-source)',
    'claude-instant-1 (closed-source)',
    'Llama-2-70b (70B, Base)',
    'Llama-2-70b-chat (70B, RLHF)',
    'CodeLlama-34b (34B, Base)',
    'CodeLlama-34b-Instruct (34B, SIFT)',
]

const all_models = [
    'CodeLlama-13b (13B, Base)',
    'CodeLlama-13b-Instruct (13B, SIFT)',
    'CodeLlama-34b (34B, Base)',
    'CodeLlama-34b-Instruct (34B, SIFT)',
    'CodeLlama-7b (7B, Base)',
    'CodeLlama-7b-Instruct (7B, SIFT)',
    'Lemur-70b-chat-v1 (70B, SIFT)',
    'Lemur-70b-v1 (70B, Base)',
    'Llama-2-13b (13B, Base)',
    'Llama-2-13b-chat (13B, RLHF)',
    'Llama-2-70b (70B, Base)',
    'Llama-2-70b-chat (70B, RLHF)',
    'Llama-2-7b (7B, Base)',
    'Llama-2-7b-chat (7B, RLHF)',
    'chat-bison-001 (closed-source)',
    'claude-2 (closed-source)',
    'claude-instant-1 (closed-source)',
    'gpt-3.5-turbo-0613 (closed-source)',
    'vicuna-13b-v1.5 (13B, SIFT)',
    'vicuna-7b-v1.5 (13B, SIFT)'
]


document.addEventListener('DOMContentLoaded', function () {
    fetch('website/data/sr_vs_k_series.json')
        .then(response => response.json())
        .then(data => {
            sr_vs_k_series = data;

            // Do stuff

            createChart(default_order);

            document.getElementById("visualize-sr-vs-k-open-behind-close").addEventListener("click", function () {
                createChart(default_order);
            });


            document.getElementById("visualize-sr-vs-k-scale-with-model-size-llama2-base").addEventListener("click", function () {
                createChart([
                    'Llama-2-7b (7B, Base)',
                    'Llama-2-13b (13B, Base)',
                    'Llama-2-70b (70B, Base)',
                ]);
            });

            document.getElementById("visualize-sr-vs-k-scale-with-model-size-llama2-rlhf").addEventListener("click", function () {
                createChart([
                    'Llama-2-7b-chat (7B, RLHF)',
                    'Llama-2-13b-chat (13B, RLHF)',
                    'Llama-2-70b-chat (70B, RLHF)',
                ]);
            });

            document.getElementById("visualize-sr-vs-k-scale-with-model-size-codellama-base").addEventListener("click", function () {
                createChart([
                    'CodeLlama-7b (7B, Base)',
                    'CodeLlama-13b (13B, Base)',
                    'CodeLlama-34b (34B, Base)',
                ]);
            });

            document.getElementById("visualize-sr-vs-k-scale-with-model-size-codellama-sift").addEventListener("click", function () {
                createChart([
                    'CodeLlama-7b-Instruct (7B, SIFT)',
                    'CodeLlama-13b-Instruct (13B, SIFT)',
                    'CodeLlama-34b-Instruct (34B, SIFT)',
                ]);
            });

            document.getElementById("visualize-sr-vs-k-vicuna-better-than-llama").addEventListener("click", function () {
                createChart([
                    'vicuna-7b-v1.5 (13B, SIFT)',
                    'Llama-2-7b-chat (7B, RLHF)',
                    'Llama-2-7b (7B, Base)',
                ]);
            });

            document.getElementById("visualize-sr-vs-k-lemur-better-than-llama").addEventListener("click", function () {
                createChart([
                    'Lemur-70b-v1 (70B, Base)',
                    'Lemur-70b-chat-v1 (70B, SIFT)',
                    'Llama-2-70b-chat (70B, RLHF)',
                    'Llama-2-70b (70B, Base)',
                ]);
            });

            document.getElementById("visualize-sr-vs-k-rlhf").addEventListener("click", function () {
                createChart([
                    'Llama-2-7b (7B, Base)',
                    'Llama-2-7b-chat (7B, RLHF)',
                    'Llama-2-13b (13B, Base)',
                    'Llama-2-13b-chat (13B, RLHF)',
                    'Llama-2-70b (70B, Base)',
                    'Llama-2-70b-chat (70B, RLHF)',
                ]);
            });

            document.getElementById("visualize-sr-vs-k-all").addEventListener("click", function () {
                createChart(all_models, false);
            });
        });

});
