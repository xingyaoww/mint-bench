from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="mint-bench",
    version="1.0.1",
    author="Xingyao Wang",
    author_email="xingyao6@illinois.edu",
    description="MINT Benchmark to Evaluate LLMs' Multi-Turn Interaction Capabilities.",
    url="https://xingyaoww.github.io/mint-bench",
    packages=find_packages(),
    install_requires=requirements,  # List of requirements read from requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
)
