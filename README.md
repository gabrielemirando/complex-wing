# Project Be Books

## Tech

I decided to use Python, since is the language I am most comfortable
with at the moment. So I started the implementation of the service using FastAPI, 
which to me is probably the best solution for a lightweight service. 
Unfortunately, given my limited experience with FastApi 
I found myself banging my head on the keyboard when writing tests. 
After being stuck for a while, I then imagined myself in a real-world scenario, 
with little time and some production-ready code to develop. It was there that 
I realized that perhaps the best choice would be to use good old Django, 
with which I am currently very confident. And so I did. I removed any possible 
functionality with which Django is shipped by default and that was not needed, 
leaving pretty much only the Rest Framework. The setup I've come up with 
looks like this:

* [Poetry](https://python-poetry.org/), for dependency management
* [Ruff](https://docs.astral.sh/ruff/), for linting and formatting
* [Django](https://www.djangoproject.com/), as web framework
* [Django Rest Framework](https://www.django-rest-framework.org/), for the APIs
* [Celery](https://docs.celeryq.dev/en/stable/), for running async tasks with ease

## Architecture

Now that the project is completed I feel like I used a bazooka to kill an ant. 
But that was partly intentional, because I took this task as an example for 
something more complicated. The architecture of the system is composed by 
the following components:

* _book-service_: the Django application that exposes the APIs
* _book-worker_: the Celery worker that runs the async tasks for creating reviews
* _rabbitmq_: as message broker for Celery
* _db_: a Postgres database to save the review information
* _redis_: to temporarily save the id of the reviews that are being created

## Code Organization

I usually follow the [Django Style Guide](https://github.com/HackSoftware/Django-Styleguide) 
when starting new Django projects. The code in project-be-books is divided into:

* _app_: the code for the only Django app in the project
* _config_: containing the project settings
* _tests_: the tests for the service

The code in the app folder is organized into unidirectional layers
`apis -> (tasks) -> services -> models`:
* _apis_ expose the endpoints for the system
* _tasks_ and _services_ contain the business logic
* _models_ define the data structure for reviews

I've written some tests verify the behavior of the various api endpoints. 
There are also some learning tests for the Gutendex API, which are currently
skipped.

## Installation

To run the project it should be enough to run the _start.sh_ script. 

An OpenAPI schema is browsable at `http://localhost:8000/`.

Launching _stop.sh_ should stop the containers and clear Docker volumes, while _test.sh_ 
should run the tests.

# Task Go Lang

Nothing much to say about this task :). I followed the Go Tutorial and tried to
fix the problems described in the README in the way it made sense to me.
