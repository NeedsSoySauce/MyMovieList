# COMPSCI 235 Assignment 2

This assignments involved extending the first assignment into a web application using Python's Flask framework. 

## Setup

These setup instructions assume you already have Python and [virtualenv](https://pypi.org/project/virtualenv/) installed. The following will clone this repository, setup and activate a virtual environment, and install dependencies.

### Windows

```shell script
git clone https://github.com/NeedsSoySauce/COMPSCI-235-A1.git
cd .\COMPSCI-235-A1\
virtualenv .virtualenv
.\.virtualenv\Scripts\activate
pip install -r requirements.txt
```

### Mac OS / Linux

```shell script
git clone https://github.com/NeedsSoySauce/COMPSCI-235-A1.git
cd .\COMPSCI-235-A1\
virtualenv .virtualenv
source .\.virtualenv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

The *.env* file at the project's root contains configuration settings. They are defined as follows:

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

## Execution

From the project's root and within the activated virtual environment:

````shell script
flask run
```` 

## Testing

From the project's root and within the activated virtual environment:

```shell script
python -m pytest
```

To run tests with coverage:

```shell script
coverage run --source ./movie -m pytest
coverage report
```

