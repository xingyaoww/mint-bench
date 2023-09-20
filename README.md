# MINT: Multi-turn Interactive Evaluation for Large Language Models

Official Repo for paper [MINT: Multi-turn Interactive Evaluation for Large Language Models](https://arxiv.org/abs/2309.10691) by [Xingyao Wang](https://xingyaoww.github.io/)\*, [Zihan Wang](https://zihanwang314.github.io/)\*, [Jiateng Liu](https://lumos-jiateng.github.io/), [Yangyi Chen](https://yangyi-chen.github.io/), [Lifan Yuan](https://lifan-yuan.github.io/), [Hao Peng](https://haopeng-nlp.github.io/) and [Heng Ji](http://blender.cs.illinois.edu/hengji.html).

**MINT** benchmark aims to evaluate LLMs' ability to solve tasks with **m**ulti-turn **int**eractions by (1) using tools and (2) leveraging natural language feedback.

Please visit our [website](https://xingyaoww.github.io/mint-bench) for more information and visualization.

> :warning: WARNING: Evaluation of LLMs requires executing untrusted model-generated code. Users are *strongly encouraged* to sandbox the code execution so that it does not perform destructive actions on their host or network. We highly recommend using the provided docker image for isolated execution.


## :rocket: Quick Start

### Environment Setup

```bash
git clone https://github.com/xingyaoww/mint-bench
cd mint-bench
# Download all data for evaluation & all existing model outputs
./scripts/setup.sh
```

You can choose to use docker (recommended) or local setup as follows.

#### Docker Setup (Recommended)

You only need to ensure that you have docker installed on your local computer following [the official guide](https://docs.docker.com/desktop/install/linux-install/).

#### Local Setup

```bash
# Install Anaconda or Miniconda first if you don't have it already.
conda env create -f environment.yml
conda activate mint
# Install the MINT package
pip install -e .
```

### Model Setup

**To evaluate huggingface-compatible open-source models**, check instructions [here](docs/SERVING.md).

**To evaluate API-base closed-source models**, set Your API Key:

```bash
# Obtain OpenAI API access from https://openai.com/blog/openai-api
# This key is necessary for all models since, by default, we use GPT-4 for feedback generation
export OPENAI_API_KEY='YOUR KEY HERE';

# The following keys are optional
# Will only be used if you use Bard or Claude as the evaluated model/feedback provider
# https://www.googlecloudcommunity.com/gc/AI-ML/Google-Bard-API/m-p/538517
export BARD_API_KEY='YOUR KEY HERE';
# https://docs.anthropic.com/claude/docs/getting-access-to-claude
export ANTHROPIC_API_KEY='YOUR KEY HERE';
```

Please refer to [docs/CONFIG.md](docs/CONFIG.md) if you want to evaluate a custom API-based model.


### Generate Config

MINT uses configuration files to specify the experiment settings (e.g., which models to use, which datasets to use, etc.).
We provide a script [`mint/configs/config_variables.py`](mint/configs/config_variables.py) to generate default config files for you.

Please refer to [docs/CONFIG.md](docs/CONFIG.md) if you want to add an evaluated model, a different LLM that provides feedback, or different experiment setting (e.g., feedback type).

```bash
# Create configuration files for your experiment.
# By default configs will be saved to configs/ and model outputs will be saved to data/outputs
python mint/configs/generate_config.py
```

### Evaluate Models
**If you want to use a docker environment for better isolation**: We recommend using a terminal multiplexer (e.g., [tmux](https://github.com/tmux/tmux/wiki)) to start the docker for better management.
Please make sure you have admin permission by adding the prefix "sudo" or have your admin [add you to the docker user group](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).
You will enter an interactive docker environment with all dependencies installed:
```bash
./scripts/docker/run_interactive.sh
```

Run the following once you are inside the docker container (for docker-setup), or you are in the conda environment (`conda activate mint`):
```bash
# Use this script to run the experiment
# You can specify which config file you want to run by modifying the script
# By default, we will run multiple configs in parallel and save output to `output.txt` in corresponding outputs folder
./scripts/run.sh

# If you want to run the experiment in debug mode (only run 1 config at a time), run the following
DEBUG_MODE=1 ./scripts/run.sh
```

### Analyze and Visualize Output

**Analyze result**: You can use the notebook `scripts/notebook/analyze_output.ipynb` to analyze the model you evaluated and reproduce tables and figures from the paper.

**Visualize the results**: The following code will start a streamlit-based visualizer to visualize your directory.
```bash
streamlit run scripts/visualizer.py -- --data_dir data/outputs
```


## :star2: Contributing

We welcome contributions to this repo from the community!

To add your model to the benchmark, you can start an issue and submit your model outputs `<model_name>.zip` [here](https://uofi.app.box.com/f/07369c26b565487cb976aba921ca080d).
Please take a look at [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for more details about contributing models, tools, and data.

## :books: Citation

If you find this repo helpful, please cite our paper:

```bibtex
@misc{wang2023mint,
      title={MINT: Evaluating LLMs in Multi-turn Interaction with Tools and Language Feedback},
      author={Xingyao Wang and Zihan Wang and Jiateng Liu and Yangyi Chen and Lifan Yuan and Hao Peng and Heng Ji},
      year={2023},
      eprint={2309.10691},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
