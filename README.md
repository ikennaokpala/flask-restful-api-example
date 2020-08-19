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

### Docker development setup (default CentOS)

    $ docker-compose up
    # Run this on another terminal tab
    $ docker exec -it api /bin/bash
    $ source $(pipenv --venv)/bin/activate
        $ make db_create
        $ make db_migrate
        $ make tests

#### Docker development setup (Ubuntu)

    $ LSARP_OS_PLATFORM=ubuntu docker-compose up
     Run the other steps from  Docker development setup (default CentOS) section

### Running Tests

To run all the tests

    $ make tests

To run a single the test file

    $ make test <name_of_test_file>

Example: 
    $ make test app/tests/test_projects.py

To run a single the test class

    $ make test <name_of_test_file>::TestClass

Example: 
    $ make test app/tests/test_projects.py::TestProjects

To run a single the test method

    $ make test <name_of_test_file>::TestClass::test_method

Example: 
    $ make test app/tests/test_projects.py::TestProjects::test_fetch_all_owned_and_collaboarating_projects_without_page_and_per_page_and_direction

To run tests with verbosity set 

    $ TEST_PROGRESS_VERBOSITY=2  make tests

or 

    $ TEST_PROGRESS_VERBOSITY=2  make test <name_of_test_file>

### Seeding and generating sample data 

By default you get a 100 rows of projects and data types and 2 MZXml and metadata shipments assigned to each data type/

    $ make db_seed

If you need more or less than 100 rows

    $ SEED_DATA_COUNT=<however_many> make db_seed
