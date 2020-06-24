# Hired Django RESTful App 

This is the back-end counterpart to the full-stack [Hired React App](https://github.com/kurtkrafft1/Hired). A full description of the app can be found there. 

# Project Setup
1. Please Note that you must place the following steps in a separate directory from the front end app!!!!

1. Clone the repo and cd into it:

    `git clone git@github.com:kurtkrafft1/Hired-API.git`

1. Navigate to the root directory: 
    `cd Hired-API`

1. Set up your virtual environment:

    `python -m venv hiredEnv`

1. Activate virtual environment:

    `source ./hiredEnv/bin/activate`

1. Install dependencies:

    `pip install -r requirements.txt`

1. I had to manually connect to the database a few times so you're going to have to set that up really quick so follow these instructions 

1. In the root directory (the one you should be in) enter this: `touch hiredapp/views/connection.py`

1. hit then `code .` or some way to open your text editor to the root directory. 

1. find that connection file the path is this `hiredapp/views/connection.py`

1. in that file enter the following code:
         `class Connection:`
         `      db_path= "your relative path here"`

1. make sure that the spacing is correct and that db_path is indented

1. In the terminal now we can run migrations:

    `python manage.py makemigrations`
    `python manage.py migrate`

1. Now that you have this set up go back to your text editor that you opened earlier and you should see a file called "db.sqlite3" right or cmd click that file and hit 'copy relative path' 

1. navigate back to the connection.py file and past that path where it says "your relative path here" keeping the quotation marks


1. in your terminal it is time to load fixtures:

    `python manage.py loaddata */fixtures/*.json`


1. Start the API server:

    `python manage.py runserver`

1. Follow the [steps on the front-end web app readme](https://github.com/kurtkrafft1/Hired) to view the web app in your browser

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