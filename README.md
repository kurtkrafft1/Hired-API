# Hired Django RESTful App 

This is the back-end counterpart to the full-stack [Hired React App](https://github.com/kurtkrafft1/Hired). A full description of the app can be found there. 

# Project Setup

1. Clone the repo and cd into it:

    `git clone git@github.com:kurtkrafft1/Hired.git && cd $_`

1. Set up your virtual environment:

    `python -m venv hiredEnv`

1. Activate virtual environment:

    `source ./hiredEnv/bin/activate`

1. Install dependencies:

    `pip install -r requirements.txt`

1. Run migrations:

    `python manage.py makemigrations`
    `python manage.py migrate`

1. Load fixtures:

    `python manage.py loaddata */fixtures/*.json`


1. Start the API server:

    `python manage.py runserver`

1. Follow the [steps on the front-end web app readme]((https://github.com/kurtkrafft1/Hired) to view the web app in your browser

## Technology Utilized
1. Django
1. Python
1. SQLite
1. Fixtures
1. ORM & SQL queries
1. Models
1. API Endpoint Views  
1. User authentication with authtoken
1. url routing

## Made By:
- [Kurt Krafft](https://github.com/kurtkrafft1)

![ERD] (/images/erd.png)    