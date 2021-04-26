from setuptools import find_packages, setup

setup(
    name='anodeclstmgru',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'loguru',
        'torch',
        'scikit-learn',
        'pytorch-lightning',
        'numpy',
        'pandas-profiling',
        'plotly',
        'jupyter',
        'ipywidgets',
        'matplotlib',
        'tqdm'
    ],
    version='0.1.0',
    description='Some experiments with LSTMs and GRUs for anomaly detection use cases on publicly available dataset(s).',
    author='Henrik Steude',
    license='',
)
