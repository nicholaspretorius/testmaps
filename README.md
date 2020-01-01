[![pipeline status](https://gitlab.com/nicholaspretorius/testmaps/badges/master/pipeline.svg)](https://gitlab.com/https://gitlab.com/nicholaspretorius/testmaps/commits/master)

## Instructions

* `python3.7 -m venv env`
* `source env/bin/activate`
* `pip list`
* `pip install flask-restplus`

### Swagger

* See Swagger docs at: http://localhost:5001/swagger

### Run Local

* `export FLASK_APP=project/__init__.py`
* `python manage.py run`

### Run docker-compose

* `docker-compose up --build`
* Check for api at: http://localhost:5001/hello

Remove <none> Docker images: 

* `docker rmi $(docker images -f "dangling=true" -q)`

### Database

* `docker-compose exec api python manage.py recreate_db`
* `docker-compose exec db psql -U postgres`
* `\l` list the databases
* `\c users_dev` connect to the 'users_dev' db
* `\dt` list relations for that db

### Run tests

* `docker-compose exec api pytest "project/tests"`
* `docker-compose exec api pytest "project/tests" --disable-warnings`
* `docker-compose exec api pytest "project/tests" -p no:warnings`
* `dc exec api pytest "project/tests" -p no:warnings --cov="project"`
* `dc exec api pytest "project/tests" -p no:warnings --cov="project" --cov-report html`

### Flake8, black, isort

Flake8 is for linting, black for formatting and isort for ordering of imports.

* `dc exec api flake8 project`
* `dc exec api black project --check`
* `dc exec api black project --diff`
* `dc exec api black project`
* `dc exec api /bin/sh -c "isort project/*/*.py --check-only"`
* `dc exec api /bin/sh -c "isort project/*/*.py --diff"`
* `dc exec api /bin/sh -c "isort project/*/*.py"`

### Run the shell

* `docker-compose exec api flask shell`


### Logging

* Import: `from project.utils.logger import log`
* Usage: `log.debug(f"Message goes here: {var_name_here}")` or `log.error(f"Message goes here: {var_name_here}")`
* Levels: info, debug, error
* Check the logging.conf file for how `console` and `file` are setup as handlers. 

### View Swagger

* `http://localhost:5001/api/1/docs`


### Run production Dockerfile

* `docker build -f Dockerfile.prod -t registry.heroku.com/waketestmaps/web .`
* `docker run --name waketestmaps -e "PORT=8765" -p 5002:8765 registry.heroku.com/waketestmaps/web:latest`
* Visit `http://localhost:5002/api/1/hello`
* `docker stop waketestmaps`
* `docker rm waketestmaps`
* `docker push registry.heroku.com/waketestmaps/web:latest`
* `heroku container:release web`
* Visit `https://waketestmaps.herokuapp.com/api/1/hello`
* `heroku run python manage.py reset_db`

### Flask Admin

* Visit `http://localhost:5001/admin/user/`


## Client

Install dependencies with Yarn: `yarn install`

Note: For some reason *create-react-app* running after an `npm install` has problems using *fsevents* with `npm test` and the client tests will not run. Using `yarn install` fixes this and `npm test` and `npm start` will work as expected.

### Run on local

* From /services/client run: `npm start`
* Visit `http://localhost:3000`
* `export REACT_APP_USERS_SERVICE_URL=http://localhost:5001/api/1`

### Tests

* From the /services/client folder run: `npm test`
* Runs all tests in --watch mode 
* Run with coverage: `./node_modules/.bin/react-scripts test --coverage`