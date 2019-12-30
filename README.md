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

### Run the shell

* `docker-compose exec api flask shell`


### Logging

* Import: `from project.utils.logger import log`
* Usage: `log.debug(f"Message goes here: {var_name_here}")` or `log.error(f"Message goes here: {var_name_here}")`
* Levels: info, debug, error
* Check the logging.conf file for how `console` and `file` are setup as handlers. 

### View Swagger

* `http://localhost:5001/api/1/docs`