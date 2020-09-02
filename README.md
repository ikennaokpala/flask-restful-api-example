#### LSARP

### Prerequisites

Python Version: 3.7 or higher
Python Version Manager: pyenv
Python Environments and Packages Manager: pipenv
Database: PostgreSQL
Containerised solution: Docker and Docker compose

### Terminal commands

    Initial production installation: make install
    Initial development (with pyenv) installation: make build

    To run test: make tests

    To run application: make run

    To run all with tests commands at once : make all


### Viewing the app ###

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:3000/

### Docker development setup (default CentOS)

    $ docker-compose up
    # Run this on another terminal tab
    $ docker exec -it api-<os>-<environment> /bin/bash # Example api-centos-development
    $ source $(pipenv --venv)/bin/activate # if Dockerimage is built in development mode
        $ make db create
        $ make db migrate
        $ make tests

#### Docker development setup (Ubuntu)

    $ LSARP_OS_PLATFORM=ubuntu docker-compose up

     Run the other steps from  Docker development setup (default CentOS) section

### Running Tests

To run all the tests

    $ make tests

To run a single the test file

    $ make test <path/to/name_of_test_file>

Example: 
    $ make test app/tests/test_projects.py

To run a single the test class

    $ make test <path/to/name_of_test_file>::TestClass

Example: 
    $ make test app/tests/test_projects.py::TestProjects

To run a single the test method

    $ make test <path/to/name_of_test_file>::TestClass::test_method

Example:

    $ make test app/tests/test_projects.py::TestProjects::test_fetch_all_owned_and_collaborating_projects_without_page_and_per_page_and_direction

### Working with database

#### Initialize database

    $ make db init

#### Create database

    $ make db create

#### Drop database

    $ make db drop

#### Create database migration files

    $ make db migration

#### Update Schema with database migrations

    $ make db migrate

#### Seeding and generating sample data 

By default you get a 100 rows of projects and data types and 2 MZXml and metadata shipments assigned to each data type/

    $ make db seed

If you need more or less than 100 rows

    $ SEED_DATA_COUNT=<however_many> make db seed
