# COMPSCI 235 Assignment 1

This assignment involved the implementation of several domain models for a to-be web application.

## Setup

These setup instructions assume you already have Python and [virtualenv](https://pypi.org/project/virtualenv/) installed. The following will clone this repository, setup a virtual environment, and install dependencies.

### Windows

```shell
git clone https://github.com/NeedsSoySauce/COMPSCI-235-A1.git
cd .\COMPSCI-235-A1\
virtualenv .virtualenv
.\.virtualenv\Scripts\activate
pip install -r requirements.txt
```

### Mac OS / Linux

```
git clone https://github.com/NeedsSoySauce/COMPSCI-235-A1.git
cd .\COMPSCI-235-A1\
virtualenv .virtualenv
source .\.virtualenv\Scripts\activate
pip install -r requirements.txt
```

## Run tests

From the project's root run the following.

```shell
python -m pytest tests
```