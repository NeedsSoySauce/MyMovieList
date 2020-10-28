
![image](https://user-images.githubusercontent.com/30617834/97424047-0921a500-1975-11eb-81d6-ccb01b80bb92.png)

# COMPSCI 235 Assignment 3

This assignment involved extending the previous assignment to persist changes using a database. SQLAlchemy's ORM was used with simple in-memory caching added using Flask-Caching. TDD practices were applied throughout development with unit and integration tests being implemented for the ORM and database repository respectively.

## Setup

These setup instructions assume you already have Python and [virtualenv](https://pypi.org/project/virtualenv/) installed. The following will clone this repository, setup and activate a virtual environment, and install dependencies.

### Windows

```shell script
git clone https://github.com/NeedsSoySauce/COMPSCI-235-A3.git
cd .\COMPSCI-235-A3\
virtualenv .virtualenv
.\.virtualenv\Scripts\activate
pip install -r requirements.txt
```

### Mac OS / Linux

```shell script
git clone https://github.com/NeedsSoySauce/COMPSCI-235-A3.git
cd .\COMPSCI-235-A3\
virtualenv .virtualenv
source .\.virtualenv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

The *.env* file at the project's root contains configuration settings. They are defined as follows:

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application. Can be set to true to force the database repository to be repopulated on each run.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.
* `SQLALCHEMY_DATABASE_URI`: URI for the database SQLAlchemy will use.
* `SQLALCHEMY_ECHO`: Set to True to log debugging information from SQLAlchemy.
* `REPOSITORY`: Specifies what repository to use. Either 'memory' or 'database'. 
* `MAX_LINES_TO_LOAD`: Integer. Specifies the maximum number of movies to populate the repository with. If not specified all available movies are loaded. 

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

