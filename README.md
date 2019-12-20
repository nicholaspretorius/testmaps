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

### Run tests

* `docker-compose exec api pytest "project/tests"`