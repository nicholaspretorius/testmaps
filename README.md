[![pipeline status](https://gitlab.com/nicholaspretorius/testmaps/badges/master/pipeline.svg)](https://gitlab.com/https://gitlab.com/nicholaspretorius/testmaps/commits/master)

## Instructions

* `python3.7 -m venv env`
* `source env/bin/activate`
* `pip list`
* `pip install -r requirements.txt`

### Swagger

* See Swagger docs at: http://localhost:5001/docs

### Setup Local DB

If you are not using Docker, you can run the app locally as follows:

* `dropdb users_dev -p 5433`
* `createdb users_dev -p 5433`
* `python manage.py recreate_db`
* `python manage.py seed_db`
* Comment line #22 and uncomment line #23 of config.py

### Run Local

* `export FLASK_APP=project/__init__.py`
* `export APP_SETTINGS=project.config.DevelopmentConfig`
* `export FLASK_ENV=development`
* `python manage.py run`

### Run docker-compose

* `docker-compose up --build`
* Check for api at: http://localhost:5001/hello
* See logs `dc logs -f` (Ctrl + c to quit)


#### Docker Housekeeping

* Show Docker disk usage: `docker system df`
* Remove <none> Docker images: `docker rmi $(docker images -f "dangling=true" -q)`
* Removed unused volumes: `docker volume prune`
* Removed unused Docker resource: `docker system prune`

### Database

* `docker-compose exec users python manage.py recreate_db`
* `docker-compose exec users python manage.py seed_db`
* `dc exec users python manage.py reset_db`
* `docker-compose exec users-db psql -U postgres`
* `\l` list the databases
* `\c users_dev` connect to the 'users_dev' db
* `\dt` list relations for that db

### Run tests

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

Flake8 is for linting, black for formatting and isort for ordering of imports.

* `dc exec users flake8 project`
* `dc exec users black project --check`
* `dc exec users black project --diff`
* `dc exec users black project`
* `dc exec users /bin/sh -c "isort project/*/*.py --check-only"`
* `dc exec users /bin/sh -c "isort project/*/*.py --diff"`
* `dc exec users /bin/sh -c "isort project/*/*.py"`

### Run the shell

* `docker-compose exec users flask shell`


### Logging

* Import: `from project.utils.logger import log`
* Usage: `log.debug(f"Message goes here: {var_name_here}")` or `log.error(f"Message goes here: {var_name_here}")`
* Levels: info, debug, error
* Check the logging.conf file for how `console` and `file` are setup as handlers. 


### Run production Dockerfile

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

* Visit `http://localhost:5001/admin/user/`


## Client

Install dependencies with Yarn: `yarn install`

Note: For some reason *create-react-app* running after an `npm install` has problems using *fsevents* with `npm test` and the client tests will not run. Using `yarn install` fixes this and `npm test` and `npm start` will work as expected.

### Run on local

* `export REACT_APP_USERS_SERVICE_URL=http://localhost:5000`
* From /services/client run: `npm start`
* Visit `http://localhost:3000`


### Run on Docker

* `export REACT_APP_USERS_SERVICE_URL=http://localhost:5001 && dc up --build`
* From project root run: `dc up --build`
* Visit `http://localhost:3007`

### Tests

* From the /services/client folder run: `npm test`
* Runs all tests in --watch mode 
* Run with coverage: `./node_modules/.bin/react-scripts test --coverage`

### Linting

* `npm run lint`
* `dc exec client npm run lint`

### Formatting

* `npm run prettier:check`
* `npm run prettier:write`
* `dc exec client npm run prettier:check`
* `dc exec client npm run prettier:write`


### Run Dockerfile.deploy locally

* `export REACT_APP_USERS_SERVICE_URL=http://localhost:8007`
* `export DATABASE_URL=db_name_goes_here`
* `docker build -f Dockerfile.deploy -t registry.heroku.com/waketestmaps/web .`
* `docker run --name waketestmaps -e PORT=8765 -e DATABASE_URL="$(echo $DATABASE_URL)" -e REACT_APP_USERS_SERVICE_URL="$(echo $REACT_APP_USERS_SERVICE_URL)" -e "SECRET_KEY=secret_key_here" -p 8007:8765 registry.heroku.com/waketestmaps/web:latest`
* `docker exec -it waketestmaps python manage.py reset_db`
* For client visit: `http://localhost:8007/`
* For api visit: `http://localhost:8007/users/`
* For Swagger visit: `http://localhost:8007/docs`
* `docker stop waketestmaps`
* `docker rm waketestmaps`

### Deploy

* `docker push registry.heroku.com/waketestmaps/web:latest`
* `heroku container:release --app waketestmaps web`
* `heroku run python manage.py reset_db`
* Visit (client)[https://waketestmaps.herokuapp.com/`]
* Visit (api)[https://waketestmaps.herokuapp.com/users/`]
* Visit (Swagger)[https://waketestmaps.herokuapp.com/docs`]