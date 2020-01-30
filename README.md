[![pipeline status](https://gitlab.com/nicholaspretorius/testmaps/badges/master/pipeline.svg)](https://gitlab.com/https://gitlab.com/nicholaspretorius/testmaps/commits/master)

## Development Notes

Below are reference notes related to developing and running the project. Please read through them to get accustomed and started.

## Instructions

Local development requires the following:

Install and activate a Python 3.7 virtual environment as follows: 

* `python3.7 -m venv env`
* `source env/bin/activate`
* `pip list`
* `pip install -r requirements.txt`

### Swagger - API Documentation

When viewing on web: 
* See swagger docs at: https://waketestmaps.herokuapp.com/docs

When running locally: 
* See Swagger docs at: http://localhost:5001/docs

### Setup Local DB

If you are not using Docker, you can run the app locally as follows - however, I would discourage this as it is not "intended" to be run this way:

* `dropdb users_dev -p 5433`
* `createdb users_dev -p 5433`
* `python manage.py recreate_db`
* `python manage.py seed_db`
* Comment line #22 and uncomment line #23 of config.py

### Run Local

To run locally via Python:

* `export FLASK_APP=project/__init__.py`
* `export APP_SETTINGS=project.config.DevelopmentConfig`
* `export FLASK_ENV=development`
* `python manage.py run`

### Run docker-compose

The recommended way of running this application is via docker-compose:

Note: Anywhere you see "dc" this is my shortcut for "docker-compose", which has been setup via an alias. 

* `docker-compose up --build`
* To sanity check that the API is running, visit: `http://localhost:5001/hello`
* See logs `docker-compose logs -f` (Ctrl + c to quit)


#### Docker Housekeeping

Docker can be a resource hog on your local machine, as such it helps to do some Docker "housekeeping" occassionally.

* Show Docker disk usage: `docker system df`
* Remove <none> Docker images: `docker rmi $(docker images -f "dangling=true" -q)`
* Removed unused volumes: `docker volume prune`
* Removed unused Docker resource: `docker system prune`

### Database

To setup and populate the database with some data, do as follows: 

* `docker-compose exec users python manage.py recreate_db`
* `docker-compose exec users python manage.py seed_db`
* `dc exec users python manage.py reset_db`

In order to view Postgres from the Docker container, do as follows: 

* `docker-compose exec users-db psql -U postgres`
* `\l` list the databases
* `\c users_dev` connect to the 'users_dev' db
* `\dt` list relations for that db

### Run tests

To run the API tests, you can do the following. Please note the various options that can be run to specify different areas of testing. there are currently 101 tests covering just over 90% of the application. 

* `docker-compose exec users pytest "project/tests"`
* `docker-compose exec users pytest "project/tests" --disable-warnings`
* `docker-compose exec users pytest "project/tests" -p no:warnings`
* `dc exec users pytest "project/tests" -p no:warnings --cov="project"`
* `dc exec users pytest "project/tests" -p no:warnings --cov="project" --cov-report html`
* Rerun tests that failed in last run: `docker-compose exec users pytest "project/tests" --lf`
* Run tests with only "config" in the name: `docker-compose exec users pytest "project/tests" -k config`
* Run tests with only "production" in the name: `docker-compose exec users pytest "project/tests" -k production`
* Stop tests after first failure: `docker-compose exec users pytest "project/tests" -x`
* Enter PBD after first failure and end the test session: `docker-compose exec users pytest "project/tests" -x --pdb`
* Stop after two failures: `docker-compose exec users pytest "project/tests" --maxfail=2`
* Show local variables in traceback: `docker-compose exec users pytest "project/tests" -l`
* List the two slowest tests: `docker-compose exec users pytest "project/tests"  --durations=2`


### Flake8, black, isort

[Flake8](http://flake8.pycqa.org/en/latest/) has been used for linting,, [black](https://black.readthedocs.io/en/stable/) for formatting and [isort](https://readthedocs.org/projects/isort/) for ordering of imports.

* `dc exec users flake8 project`
* `dc exec users black project --check`
* `dc exec users black project --diff`
* `dc exec users black project`
* `dc exec users /bin/sh -c "isort project/*/*.py --check-only"`
* `dc exec users /bin/sh -c "isort project/*/*.py --diff"`
* `dc exec users /bin/sh -c "isort project/*/*.py"`

* [Pycodestyle](https://pypi.org/project/pycodestyle/) (formerly known as Pep8) `dc exec users pycodestyle project`

### Run the shell

You can run the Flask shell as follows:

* `docker-compose exec users flask shell`


### Logging

While this has not been used in this project, it was initially written to help with logging. This is not considered part of the active project, but I have kept it for possible future reference if needed.

* Import: `from project.utils.logger import log`
* Usage: `log.debug(f"Message goes here: {var_name_here}")` or `log.error(f"Message goes here: {var_name_here}")`
* Levels: info, debug, error
* Check the logging.conf file for how `console` and `file` are setup as handlers. 

Ultimately, this will not be used. [Sentry](https://sentry.io/welcome/) would be used in order to log for both the API and the frontend. 


### Run production Dockerfile

To run the production Docker, in preparation for deploying to Heroku, do as follows:

* `docker build -f Dockerfile.prod -t registry.heroku.com/waketestmaps/web .`
* `docker run --name waketestmaps -e "PORT=8765" -p 5002:8765 registry.heroku.com/waketestmaps/web:latest`
* Visit `http://localhost:5002/hello`
* `docker stop waketestmaps`
* `docker rm waketestmaps`
* `docker push registry.heroku.com/waketestmaps/web:latest`
* `heroku container:release web`
* Visit `https://waketestmaps.herokuapp.com/hello`
* `heroku run python manage.py reset_db`

### Flask Admin

To view the Flask-Admin console:

* Visit `http://localhost:5001/admin/user/`


## Client

Install dependencies with Yarn: `yarn install`

Note: For some reason *create-react-app* running after an `npm install` has problems using *fsevents* with `npm test` and the client tests will not run. Using `yarn install` fixes this and `npm test` and `npm start` will work as expected.

### Run on Docker

To run via Docker, run the following:

* `export REACT_APP_USERS_SERVICE_URL=http://localhost:5001 && dc up --build`
* From project root run: `dc up --build`
* Visit `http://localhost:3007`

### Run on local

To run on local, run the following commands:

* `export REACT_APP_USERS_SERVICE_URL=http://localhost:5000`
* From /services/client run: `npm start`
* Visit `http://localhost:3000`

### Tests

* From the /services/client folder run: `npm test`
* Runs all tests in --watch mode 
* Run with coverage: `./node_modules/.bin/react-scripts test --coverage`
* Note: The --coverage option seems to be inconsistent. At times it reports *actual* coverage and at others it just displays nothing. I have investigated this, and got it working, only to find at a later date it no longer reports coverage. This is an open issue. Feedback or advice on this is welcomed. 

### e2e Tests

* To run Cypress, change directory into /services/client, run: `./node_modules/.bin/cypress open`
* To run Cypress from Docker run: `docker-compose run cypress ./node_modules/.bin/cypress run`


### Linting

To lint the frontend client code:

* `npm run lint`
* `dc exec client npm run lint`

### Formatting

To format the frontend client code:

* `npm run prettier:check`
* `npm run prettier:write`
* `dc exec client npm run prettier:check`
* `dc exec client npm run prettier:write`


### Run Dockerfile.deploy locally

To test/run the "deployed" Dockerfile, run the following: 

* `export REACT_APP_USERS_SERVICE_URL=http://localhost:8007`
* `export DATABASE_URL=db_name_goes_here`
* `docker build -f Dockerfile.deploy -t registry.heroku.com/waketestmaps/web .`
* `docker run --name waketestmaps -e PORT=8765 -e DATABASE_URL="$(echo $DATABASE_URL)" -e REACT_APP_USERS_SERVICE_URL="$(echo $REACT_APP_USERS_SERVICE_URL)" -e "SECRET_KEY=secret_key_here" -p 8007:8765 registry.heroku.com/waketestmaps/web:latest`
* `docker exec -it waketestmaps python manage.py reset_db`
* For client visit: `http://localhost:8007/`
* For api visit: `http://localhost:8007/wakeparks/`
* For Swagger visit: `http://localhost:8007/docs`
* `docker stop waketestmaps`
* `docker rm waketestmaps`

### Deployment

To release to Heroku (for the first time or if the Docker setup has changed) the following is required:

* `docker push registry.heroku.com/waketestmaps/web:latest`
* `heroku container:release --app waketestmaps web`
* `heroku run python manage.py reset_db`
* Visit (Swagger)[https://waketestmaps.herokuapp.com/docs`]
* Visit (API)[https://waketestmaps.herokuapp.com/wakeparks/`]
* Visit (Client)[https://waketestmaps.herokuapp.com/`]


### Notes on Auth0

* When using Google (or social login), auth.checkSession will require login on refresh for localhost (see [here](https://community.auth0.com/t/checksession-always-return-login-required-on-localhost/22119/3)). 
* When mocking Auth0, you can use this [approach](https://stackoverflow.com/questions/48552474/auth0-obtain-access-token-for-unit-tests-in-python/48554119#48554119). 