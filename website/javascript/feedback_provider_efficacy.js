// Global variables
let sr_feedback_provider_raw;
let chart = null;

const gpt_3_5_perf = 36.18;

const sortby_options = {
  GAIN_FROM_FEEDBACK: "sort-by-feedback-gain",
  FEEDBACK_PROVIDER_PERF: "sort-by-feedback-provider-perf",
}
let cur_sortby_option = sortby_options.GAIN_FROM_FEEDBACK;

function getSRWithFeedback(sr_feedback_provider_raw) {
  // each entry is like:     {
  //   "feedback_provider": "Llama-2 (70B, Base)",
  //   "SR5_difference": -9.73,
  //   "evaluated_LLM_feedback": -0.69
  // },
  // SRWithFeedback is by definition evaluated_LLM_feedback + 36.18, therefore should translate to: 36.87

  const sr_with_feedback = [];
  // the first entry should be item['model'] concating item['feedback_provider']
  sr_feedback_provider_raw.forEach(item => {
    sr_with_feedback.push([
      item['feedback_provider'],
      item['evaluated_LLM_feedback'] + gpt_3_5_perf, // perf after feedback
      item['SR5_difference'] + gpt_3_5_perf // perf of the feedback provider
    ]
    );
  });

  return sr_with_feedback;
}


function createFeedbackProviderChart() {
  const sr_with_feedback = getSRWithFeedback(sr_feedback_provider_raw);

  // Sort filtered data by feedback success rate
  if (cur_sortby_option === sortby_options.FEEDBACK_PROVIDER_PERF) {
    sr_with_feedback.sort((a, b) => b[2] - a[2]);
  } else if (cur_sortby_option === sortby_options.GAIN_FROM_FEEDBACK) {
    sr_with_feedback.sort((a, b) => b[1] - a[1]);
  }

  // Prepare your data
  const labels = sr_with_feedback.map(item => item[0]);
  // print this labels in command line
  const sr_feedback_gain = sr_with_feedback.map(item => item[1]);
  const sr_feedback_provider_perf = sr_with_feedback.map(item => item[2]);

  const title_text = 'Different Feedback Providers\' Ability to Improve GPT-3.5\'s Performance';

  if (chart) {
    chart.destroy();
  }

  const ctx = document.getElementById('chart-feedback-provider');
  chart = new Chart(ctx, {
    plugins: [ChartDataLabels],
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Success Rate with Feedback',
          data: sr_feedback_gain,
          backgroundColor: '#add8e6',
        },
        {
          backgroundColor: 'rgba(158, 159, 163, 0.5)',
          label: 'Feedback Provider\'s Performance',
          data: sr_feedback_provider_perf,
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
        x: {
          grace: 15,
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
        annotation: {
          annotations: {
            line1: {
              type: 'line',
              xMin: gpt_3_5_perf,
              xMax: gpt_3_5_perf,
              borderColor: '#3590ae',
              borderWidth: 4,
            },
          }
        },
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
        subtitle: {
          display: true,
          text: 'GPT-3.5\'s No Feedback Performance (Vertical Line): ' + gpt_3_5_perf.toFixed(2) + '%',
          font: function (context) {
            var width = context.chart.width;
            var size = Math.round(width / 40);
            size = Math.min(size, 14);

            return {
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
            }
          }
        },
        datalabels: {
          align: 'end',
          anchor: 'end',
          color: 'black',
          padding: 0,
          formatter: function (value, context) {
            return value.toFixed(2) + '%';
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


Object.values(sortby_options).forEach(sortby_option => {
  const btn = document.getElementById(sortby_option);

  btn.addEventListener('click', () => {

    // Find all active buttons within btn-group and remove the 'active' class
    document.querySelectorAll('.btn-group.feedback-provider-sort-by-selector .btn.active ')
      .forEach(active => {
        active.classList.remove('active');
      });

    // Add 'active' class to the clicked button
    btn.classList.add('active');

    // update global variables
    cur_sortby_option = sortby_option;

    // update the chart
    createFeedbackProviderChart();
  });
});

// Add event listener to the button
document.addEventListener('DOMContentLoaded', function () {

  fetch('website/data/feedback_comparison.json').then(response => response.json())
    .then((loaded_feedback_provider_data) => {
      // Both fetch requests have completed here
      sr_feedback_provider_raw = loaded_feedback_provider_data;

      // Do stuff

      createFeedbackProviderChart()

      // document.getElementById("visualize-feedback-provider").addEventListener("click", function () {
      //   createFeedbackProviderChart();  
      // });
    })
});
