#### LSARP

### Prerequisites

Python Version: 3.7 or higher
Containerised solution: Docker and Docker compose
Database: PostgreSQL

### Terminal commands

    Initial installation: make install

    To run test: make test_prepare && make tests

    To run application: make run

    To run all commands at once : make all


### Viewing the app ###

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:3000/

### Docker development setup

    $ docker-compose up
    # Run this on another terminal tab
    $ docker exec -it api /bin/bash 
        $ make createdb
        $ python manage.py db upgrade head
        $ make tests
