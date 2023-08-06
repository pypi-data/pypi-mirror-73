from pathlib import Path

import setuptools

NAME = "xgboost_model"
REQUIRES_PYTHON = '>=3.6.0'

with open("README.md", "r") as fh:
    long_description = fh.read()

ROOT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = ROOT_DIR / NAME
about = {}
with open(PACKAGE_DIR / 'VERSION') as f:
    _version = f.read().strip()
    about['__version__'] = _version


# What packages are required for this module to be executed?
def list_reqs(fname='requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()

setuptools.setup(
    # name="xgboost-model-pkg-jarsushi", # Replace with your own username
    name=NAME,
    version=about['__version__'],
    author="Joshua Robison",
    author_email="joshua.robison.a@gmail.com",
    description="A small xgboost model package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jarsushi/house-price-predict-scratch/tree/master/src/xgboost_model",
    python_requires=REQUIRES_PYTHON,
    packages=setuptools.find_packages(),
    package_data={'regression_model': ['VERSION']},
    install_requires=list_reqs(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)