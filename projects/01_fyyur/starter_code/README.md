Fyyur
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

Your job is to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

## Overview

#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI]
#----------------------------------------------------------------------------#

This app which was not complete has been completed by Yvan TCHOUDIE DJOMESSI in the scope of the Nanodegree program Real data manipulation effectiveness has been developped through Model folloaing best practices of SQLAlchemy ORM and FLASK Migrate. This is based on postgresql, assuming the database fyyur is created in the user postgres with password postgres.

##

We want Fyyur to be the next new platform that artists and musical venues can use to find each other, and discover new music shows. Let's make that happen!

## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate


```
> **Note** - If we do not mention the specific version of a package, then the default latest stable package will be installed. 

#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI]
#----------------------------------------------------------------------------#

Additional installation was DONE for missing dependencies.

Given some libraries for which the version was obsolete and leading issue,
### 2. Frontend Dependencies
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` -- (Already complete.) Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` -- (Already complete.) Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- (Already complete.) Defines the forms used to create new artists, shows, and venues.
* `app.py` -- (Missing functionality.) Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `app.py` -- (Missing functionality.) Defines the data models that set up the database tables.
* `config.py` -- (Missing functionality.) Stores configuration variables and instructions, separate from the main application code. This is where you will need to connect to the database.


Instructions
-----

1. Understand the Project Structure (explained above) and where important files are located.

#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI] - DONE
#----------------------------------------------------------------------------#

2. Build and run local development following the Development Setup steps below.
#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI] - DONE
#----------------------------------------------------------------------------#

3. Fill in the missing functionality in this application: this application currently pulls in fake data, and 
needs to now connect to a real database and talk to a real backend.
#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI] - DONE
#----------------------------------------------------------------------------#

4. Fill out every `TODO` section throughout the codebase. We suggest going in order of the following:
    * Connect to a database in `config.py`. A project submission that uses a local database connection is fine.
    * Using SQLAlchemy, set up normalized models for the objects we support in our web app in the Models section of `app.py`. Check out the sample pages provided at /artists/1, /venues/1, and /shows for examples of the data we want to model, using all of the learned best practices in database schema design. Implement missing model properties and relationships using database migrations via Flask-Migrate.
    * Implement form submissions for creating new Venues, Artists, and Shows. There should be proper constraints, powering the `/create` endpoints that serve the create form templates, to avoid duplicate or nonsensical form submissions. Submitting a form should create proper new records in the database.
    * Implement the controllers for listing venues, artists, and shows. Note the structure of the mock data used. We want to keep the structure of the mock data.
    * Implement search, powering the `/search` endpoints that serve the application's search functionalities.
    * Serve venue and artist detail pages, powering the `<venue|artist>/<id>` endpoints that power the detail pages.

#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI] - DONE
#----------------------------------------------------------------------------#


#### Data Handling with `Flask-WTF` Forms
The starter codes use an interactive form builder library called [Flask-WTF](https://flask-wtf.readthedocs.io/). This library provides useful functionality, such as form validation and error handling. You can peruse the Show, Venue, and Artist form builders in `forms.py` file. The WTForms are instantiated in the `app.py` file. For example, in the `create_shows()` function, the Show form is instantiated from the command: `form = ShowForm()`. To manage the request from Flask-WTF form, each field from the form has a `data` attribute containing the value from user input. For example, to handle the `venue_id` data from the Venue form, you can use: `show = Show(venue_id=form.venue_id.data)`, instead of using `request.form['venue_id']`.

#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI] - DONE
#----------------------------------------------------------------------------#




**Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

**Install the dependencies:**
```
pip install -r requirements.txt
```


#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI]
#----------------------------------------------------------------------------#

Given some libraries for which the version was obsolete and leading issue, all the dependencies in the requirements.txt have been upgraded after their installation

	[winpty] pip install --upgrade babel
	[winpty] pip install --upgrade python-dateutil
	[winpty] pip install --upgrade flask-moment
	[winpty] pip install --upgrade flask-wtf
	[winpty] pip install --upgrade flask_sqlalchemy


In fact, below are the version moves that have been DONE:

		babel: Moved from 2.9.0 to 2.10.3
		python-deteutil: Moved from 2.6.0 to 2.8.2
		flask-moment: Moved from 0.11.0 to 1.0.4
		flask-wtf: Moved from 0.14.3 to 1.0.1
		flask_sqlalchemy: Moved from 2.4.4 to 2.5.1


5. **Run the development server:**
```
export FLASK_APP=app
export FLASK_ENV=development # enables debug mode
python app.py (pr python3 app.py)
```

6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI]
#----------------------------------------------------------------------------#

TEST Have been DONE, and the results are in the folder DEMO_20220813

At the end of the tests, a dump of the DB has also been DONE. the dump .sql file is in the same folder DEMO_20220813