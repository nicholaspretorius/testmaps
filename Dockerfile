FROM python:3.7.4-alpine

WORKDIR /usr/src/app

# set environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

CMD python manage.py run -h 0.0.0.0