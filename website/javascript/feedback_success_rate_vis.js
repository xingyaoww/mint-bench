let sr_wo_feedback_raw;
let sr_w_feedback_raw;

const task_types = [
  'avg_micro',
  'reasoning',
  'decision_making',
  'code_generation'
];

const sortby_options = {
  FEEDBACK: "sort-by-feedbacksr",
  NO_FEEDBACK: "sort-by-nofeedbacksr",
  FEEDBACK_DELTA: "sort-by-feedbackdelta"
}
let cur_sortby_option = sortby_options.FEEDBACK;

const task_type_to_name = {
  'avg_micro': 'Micro Average',
  'reasoning': 'Reasoning',
  'decision_making': 'Decision-Making',
  'code_generation': 'Code Generation'
}

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
  'Vicuna-v1.5 (13B, SIFT)',
  'vicuna-7b-v1.5 (7B, SIFT)',

  'gpt-4-0613 (closed-source)',
]

function calculateDifferences(sr_wo_feedback, sr_w_feedback, task_type) {
  // Ensure both data arrays have the same length
  if (sr_wo_feedback[task_type].length !== sr_w_feedback[task_type].length) {
    throw new Error(`Data length mismatch: sr_wo_feedback and sr_w_feedback should have the same length for ${task_type}.`);
  }

  // Sort both datasets by name for matching
  const dataNoFeedback = sr_wo_feedback[task_type].sort((a, b) => a[0].localeCompare(b[0])).slice();
  const dataWithFeedback = sr_w_feedback[task_type].sort((a, b) => a[0].localeCompare(b[0])).slice();

  // Calculate differences
  return dataWithFeedback.map((item, index) => {
    const nameWithFeedback = item[0];
    const nameWithoutFeedback = dataNoFeedback[index][0];

    // Check if names match for the same index
    if (nameWithFeedback !== nameWithoutFeedback) {
      throw new Error(`Name mismatch at index ${index}: ${nameWithFeedback} and ${nameWithoutFeedback}`);
    }

    const diff = item[1] - dataNoFeedback[index][1];
    // name, sr_wo_feedback, sr_w_feedback, diff
    return [nameWithFeedback, dataNoFeedback[index][1], item[1], diff];
  });
}

function formatWithSign(num) {
  const fixedNum = parseFloat(num).toFixed(2); // Fix the number to 2 decimal places
  return (Math.sign(num) === 1 ? "+" : "") + fixedNum; // Add a '+' sign if the number is positive
}

let last_task_type = 'avg_micro';
let last_names_to_keep = all_models;
let chart = null;

function createChart(task_type, namesToKeep) {
  const sr_with_diff = calculateDifferences(sr_wo_feedback_raw, sr_w_feedback_raw, task_type);
  const sr_with_diff_filtered = sr_with_diff.filter(item => namesToKeep.includes(item[0]));

  // Sort filtered data by feedback success rate
  if (cur_sortby_option === sortby_options.FEEDBACK) {
    sr_with_diff_filtered.sort((a, b) => b[2] - a[2]);
  } else if (cur_sortby_option === sortby_options.NO_FEEDBACK) {
    sr_with_diff_filtered.sort((a, b) => b[1] - a[1]);
  } else if (cur_sortby_option === sortby_options.FEEDBACK_DELTA) {
    sr_with_diff_filtered.sort((a, b) => b[3] - a[3]);
  }

  // Prepare your data
  const labels = sr_with_diff_filtered.map(item => item[0]);
  const sr_wo_feedback_data = sr_with_diff_filtered.map(item => item[1]);
  const sr_w_feedback_data = sr_with_diff_filtered.map(item => item[2]);
  const diff_data = sr_with_diff_filtered.map(item => item[3]);

  const title_text = 'Task Success Rate (' + task_type_to_name[task_type] + ')';

  if (chart) {
    chart.destroy();
  }

  const ctx = document.getElementById('chart-sr-w-feedback');
  chart = new Chart(ctx, {
    plugins: [ChartDataLabels],
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'No Feedback',
          data: sr_wo_feedback_data,
          backgroundColor: 'rgba(158, 159, 163, 0.5)',
          datalabels: {
            labels: {
              'No Feedback': null
            }
          }
        },
        {
          label: 'With GPT-4 Feedback',
          data: sr_w_feedback_data,
          backgroundColor: '#add8e6',
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
      },
      indexAxis: 'y',
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          stacked: true,
          title: {
            display: true,
            text: 'Evaluated LLM',
            font: {
              size: 14,
            }
          }
        },
        x: {
          grace: 20,
          title: {
            display: true,
            text: 'Task Success Rate (%)',
            font: {
              size: 14,
            }
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: title_text,
          font: function (context) {
            var width = context.chart.width;
            var size = Math.round(width / 32);
            size = Math.min(size, 16);

            return {
              weight: 'bold',
              size: size
            };
          }
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
          position: 'bottom'
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              label += context.formattedValue + '%';
              return label;
            },
            footer: function (tooltipItems) {
              // Calculate difference
              let no_feedback = 0;
              let with_feedback = 0;
              tooltipItems.forEach(function (tooltipItem) {
                if (tooltipItem.dataset.label === 'No Feedback') {
                  no_feedback = tooltipItem.raw;
                } else if (tooltipItem.dataset.label === 'With GPT-4 Feedback') {
                  with_feedback = tooltipItem.raw;
                }
              });
              let diff = with_feedback - no_feedback;
              return 'Diff: ' + diff.toFixed(2) + '%';
            }
          }
        },
        datalabels: {
          align: 'end',
          anchor: 'end',
          color: 'black',
          padding: 0,
          formatter: function (value, context) {
            let nofeedback_perf = 0;
            let withfeedback_perf = 0;
            context.chart.data.datasets.forEach(function (dataset) {
              if (dataset.label === 'No Feedback') {
                nofeedback_perf = dataset.data[context.dataIndex];
              } else if (dataset.label === 'With GPT-4 Feedback') {
                withfeedback_perf = dataset.data[context.dataIndex];
              }
            });
            let diff = withfeedback_perf - nofeedback_perf;
            return nofeedback_perf + '%' + ' (' + formatWithSign(diff.toFixed(2)) + '%)';
          },
          font: function (context) {
            var width = context.chart.width;
            var size = Math.round(width / 48);
            size = Math.min(size, 14);
            return {
              size: size
            };
          }
        }
      }
    }
  });
}



task_types.forEach(task_type => {
  const btn = document.getElementById(task_type);

  btn.addEventListener('click', () => {

    // Find all active buttons within btn-group and remove the 'active' class
    document.querySelectorAll('.btn-group.task-selector .btn.active')
      .forEach(active => {
        active.classList.remove('active');
      });

    // Add 'active' class to the clicked button
    btn.classList.add('active');

    // update global variables
    last_task_type = task_type;

    // update the chart
    createChart(task_type, last_names_to_keep);

  });
});


Object.values(sortby_options).forEach(sortby_option => {
  const btn = document.getElementById(sortby_option);

  btn.addEventListener('click', () => {

    // Find all active buttons within btn-group and remove the 'active' class
    document.querySelectorAll('.btn-group.sort-by-selector .btn.active ')
      .forEach(active => {
        active.classList.remove('active');
      });

    // Add 'active' class to the clicked button
    btn.classList.add('active');

    // update global variables
    cur_sortby_option = sortby_option;

    // update the chart
    createChart(last_task_type, last_names_to_keep);
  });
});

// Add event listener to the button
document.addEventListener('DOMContentLoaded', function () {

  Promise.all([
    fetch('website/data/sr_without_feedback.json').then(response => response.json()),
    fetch('website/data/sr_with_feedback.json').then(response => response.json())
  ])
    .then(([loaded_sr_wo_feedback_data, loaded_sr_w_feedback_data]) => {
      // Both fetch requests have completed here
      sr_wo_feedback_raw = loaded_sr_wo_feedback_data;
      sr_w_feedback_raw = loaded_sr_w_feedback_data;

      // Do stuff

      createChart(last_task_type, last_names_to_keep);

      document.getElementById("visualize-feedback-sr-no-diff-open-close").addEventListener("click", function () {

        createChart(last_task_type, all_models);  // Replace [...] with your model names

      });

      document.getElementById("visualize-feedback-sr-sift-rlhf").addEventListener("click", function () {

        createChart(last_task_type, [
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
          'vicuna-7b-v1.5 (7B, SIFT)',
        ]);
      });

      document.getElementById("visualize-feedback-sr-gpt-4-self").addEventListener("click", function () {

        createChart(last_task_type, [
          'CodeLlama-34b (34B, Base)',
          'CodeLlama-34b-Instruct (34B, SIFT)',
          'Llama-2-70b (70B, Base)',
          'Llama-2-70b-chat (70B, RLHF)',
          'claude-2 (closed-source)',
          'claude-instant-1 (closed-source)',
          'gpt-3.5-turbo-0613 (closed-source)',
          'gpt-4-0613 (closed-source)',
        ]);  // Replace [...] with your model names

      });
    })

});
