GitHubNavigator
===============

## Requirements

* [python 2.7](https://www.python.org/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)

## Setup

* Create virtualenv:

~~~bash
$ virtualenv .venv
$ source .venv/bin/activate
~~~

* Install dependencies:

~~~bash
$ pip install -r dependencies
~~~

* Start application:

~~~bash
$ python application.py
~~~

by default application is binding to port `8080`. If you want to change it
export `PORT` env variable with desired port number.