# Movies API
An API to simulate the backend system of a movie renting service.
## Table of Contents
1. [About](#about)
1. [Database](#database)
1. [Docs](#docs)
1. [Setup](#setup)
1. [Tests](#tests)
## About
An API to simulate the backend system of a movie renting service. Written using FAST API.  
It allows users to register themselves, login for token. Then they can make purchases, see movies that are available and so on.  
Some endpoints require admin permissions.
## Database
The database is represented by this ERD diagram. API uses a sqlite database.  
![database picture](https://i.imgur.com/p01BpvS.png)
## Docs
Click here to see the [docs](https://matixezor-movies-api.herokuapp.com/docs). I think the docs are self-explanatory.  
There you can also play around with the api right away.  
To play around with it use the acc:
 * username: test_mail
 * password: test
## Setup
The API is written in Python 3.8.1 ant there are some dependencies. Run this command to install them: ``pip install -r /path/to/requirements.txt``.  
You need to fill ``SECRET_KEY`` in config file. To get that key use ``openssl rand -hex 32`` command. To run it locally use ``uvicorn main:app``. 
## Tests
There are some tests to ensure the endpoints behave how they should even if the code is changed. To run them simply use ``pytests`` command.
