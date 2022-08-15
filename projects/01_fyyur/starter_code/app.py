#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *
#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI] - Added Imports
#----------------------------------------------------------------------------#

from flask_migrate import Migrate
import sys
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
# [Yvan TCHOUDIE DJOMESSI] - DONE- Also added __table_args__ = {'quote': []} to avoid table with quote in the DB, which lead issues

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Models have been refactored in a separate file (models.py) to follow Separation of Concerns design principles as requested in the project requirements

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI] - I updated this format_datetime funciton to consider the case where the value is already a datetime.
# In fact, it was generating an error: 
# So I added a condition check
#----------------------------------------------------------------------------#



def format_datetime(value, format='medium'):
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
  #date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  #Querying the venues
  queried_venues = (
        Venue.query.with_entities(Venue.id, Venue.name, Venue.state, Venue.city)
        .order_by(Venue.city, Venue.state)
        .all()
    ) #We order by location so that when we will be using data, we will do so location by location

  #Initializing the variables
  areas_data = []
  prev_location = None
  i = -1

  for venue in queried_venues:
    curr_location = f"{venue.city}, {venue.state}"
    if prev_location != curr_location:
      #We have finished with previous location, so we can populate data for the next
      areas_data.append({"city": venue.city, "state": venue.state, "venues": []})
      i = i + 1
      prev_location = curr_location

    #We get the area venue data for the  actual venue
    area_venue_id = venue.id
    area_venue_name = venue.name
    area_venue_upcoming_shows_query1 = Show.query
    area_venue_upcoming_shows_query2 = area_venue_upcoming_shows_query1.filter(
        db.and_(Show.venue_id == venue.id, Show.start_time > datetime.now())
    )
    area_venue_num_upcoming_shows = area_venue_upcoming_shows_query2.count()
    
    #And then populate it in the areas_data
    areas_data[i]["venues"].append(
      {
        "id": area_venue_id,
        "name": area_venue_name,
        "num_upcoming_shows": area_venue_num_upcoming_shows,
      }
    )

  #We can then render the venues.html with the required areas_data
  return render_template('pages/venues.html', areas=areas_data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#


  searched = request.form.get('search_term', '').strip()
  
  #We query the venues
  venues_query1 = Venue.query.with_entities(Venue.id, Venue.name)
  
  #Then We filter based on the term the user is searching
  venues_query2 = venues_query1.filter(Venue.name.ilike(f"%{searched}%"))
  
  #And then we fetch all the results
  venues_result_search = venues_query2.all()
  
  #We can then build the response data with the various search results
  response = {
    "count": len(venues_result_search),
    "data": [
      {
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": Show.query.filter(
          db.and_(Show.venue_id == venue.id, Show.start_time > datetime.now())
          ).count(),
      }
      for venue in venues_result_search
    ],
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  #Querying from the database: described_venue will contains the information of the venue, if the venue with id "venue_id" exists in our database
  described_venue = Venue.query.get(venue_id)
  venue_data = {}


  #Here we check if these Value exist (Were we able to find an venue with venue_id from the Database? Meaning Did the previous query return data?)
  #If we have values, we then read these values and classify them between former shows (date before actual date) and upcoming shows

  if described_venue:
    venue_former_shows = []
    venue_upcoming_shows = []
    
    for actual_show in described_venue.shows:
      artist = {
        "artist_id": actual_show.artist_id,
        "artist_name": actual_show.artist.name,
        "artist_image_link": actual_show.artist.image_link,
        "start_time": actual_show.start_time,
      }

      #if the date of the show is before now, it is a former show
      if actual_show.start_time < datetime.now():
          venue_former_shows.append(artist)
      else:
          #However, if the show is now or after now, it is an upcoming show
          venue_upcoming_shows.append(artist)
    
    #Now we can put these data in the venue_data, by following the data format expected by our template show_venue.html
    venue_data = {
      **described_venue.__dict__,
      "past_shows": venue_former_shows,
      "upcoming_shows": venue_upcoming_shows,
      "past_shows_count": len(venue_former_shows),
      "upcoming_shows_count": len(venue_upcoming_shows),
    }

    # We can then render our template (assuming nothing went wrong)
    return render_template("pages/show_venue.html", venue=venue_data)

  #If we reach this place, it means there was an error (because we were not able to render, meaning we were not able to execute all the previous intructions)
  return render_template("errors/404.html")
  ###*** data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  ###*** return render_template('pages/show_venue.html', venue=data)
  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  
  #We initialize the form by using the class VenueForm | initilizing effectiveness through the request.form
  venue_form = VenueForm(request.form)
  

  #We can then render new_venue.html
  return render_template('forms/new_venue.html', form=venue_form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE - Also added request.form as attribute of VenueForm(), since The object instanciation needs the Form. This is what allow to set the data. I also applied it on other places where I use the forms
  #----------------------------------------------------------------------------#


  #We retrieve the form by using the class VenueForm | initilizing effectiveness through the request.form
  form = VenueForm(request.form)
  
  #We check if the form is valid (and that we are in post method for the request). if ok, we get data from the form and then we perform the insert transaciton in the database
  if request.method == "POST" and form.validate():
    
    form_name = request.form.get("name")
    form_city = request.form.get("city")
    form_state = request.form.get("state")
    form_address = request.form.get("address")
    form_phone = request.form.get("phone")
    form_image_link = request.form.get("image_link")
    form_facebook_link = request.form.get("facebook_link")
    form_website = request.form.get("website")
    #form_seeking_talent = request.form.get("seeking_talent", 'N')
    #Initializing the form_seeking_talent var
    form_seeking_talent = True
    if (request.form.get("seeking_talent")):
      form_seeking_talent = True
    else:
        form_seeking_talent = False
    form_seeking_description = request.form.get("seeking_description")
    form_genres = request.form.getlist("genres")

    #We perform the transaction through a try / except / finally
    try:
      venue = Venue(
        name=form_name,
        city=form_city,
        state=form_state,
        address=form_address,
        phone=form_phone,
        image_link=form_image_link,
        facebook_link=form_facebook_link,
        website=form_website,
        seeking_talent=form_seeking_talent,
        seeking_description=form_seeking_description,
        genres=form_genres,
      )
      db.session.add(venue)

      db.session.commit()
      flash(f"Venue {form_name} was successfully listed!")
    
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash(f"Ooooooops. An error occurred. Venue {form_name} could not be listed.")
    
    finally:
      db.session.close()

    return render_template('pages/home.html')

  
  #if we reach here, this means it was not valid and we were not able to insert and redirect
  
  got_form = VenueForm(request.form)

  return render_template('forms/new_venue.html', form=got_form)

  # on successful db insert, flash success
  ####*** flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  
  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  ###*** return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  #We perform the query in a try / except / finally bloc
  try:
    venue_query1 = db.session.query(Venue)
    venue_query2 = venue_query1.filter(Venue.id == venue_id)
    
    #We fetch the first
    venue_to_delete = venue_query2.first()
    
    #Now we can delete the venue
    db.session.delete(venue_to_delete)
    db.session.commit()

    flash(f"The venue {venue_to_delete.name} has been successfully deleted.")
  
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash(f"Ooooooops. An error occurred. Venue {venue_to_delete.name} could not be deleted.")
  
  finally:
    db.session.close()
  
  #We can go back to the home page
  return redirect(url_for("index"))

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  ###*** return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  
  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  #data=[{
  #  "id": 4,
  #  "name": "Guns N Petals",
  #}, {
  #  "id": 5,
  #  "name": "Matt Quevedo",
  #}, {
  #  "id": 6,
  #  "name": "The Wild Sax Band",
  #}]
  
  #Initialization of the artist_data
  artist_data = []

  #Querying to get the artist from the database
  artist_query1 = Artist.query.with_entities(Artist.id, Artist.name)
  
  #We fetch all the results (all the existing artists in the database)
  artist_data = artist_query1.all()

  #Now we can render the artists.html template with the required artist_data  
  return render_template('pages/artists.html', artists=artist_data)

@app.route('/artists/search', methods=['POST'])
def search_artists(): 
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  #response={
  #  "count": 1,
  #  "data": [{
  #    "id": 4,
  #    "name": "Guns N Petals",
  #    "num_upcoming_shows": 0,
  #  }]
  #}

  searched = request.form.get('search_term').strip()

  artist_query1 = Artist.query.with_entities(Artist.id, Artist.name)
  artist_query2 = artist_query1.filter(Artist.name.ilike(f"%{searched}%"))

  #We fetch all the results
  queried_artists = (artist_query2.all())
  
  response = {
    "count": len(queried_artists),
    "data": [
      {
        "id": actual_artist.id,
        "name": actual_artist.name,
        "num_upcoming_shows": Show.query.filter(
          db.and_(
            Show.artist_id == actual_artist.id, Show.start_time > datetime.now()
          )
        ).count(),
      }
      for actual_artist in queried_artists
    ],
  }

  #Now we can render the search_artists.html template
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  #Querying from the database: described_artist will contains the information of the artist, if the artist with id "artist_id" exists in our database
  described_artist = Artist.query.get(artist_id)
  artist_data = {}
  
  #Here we check if these Value exist (Were we able to find an artist with artist_id from the Database? Meaning Did the previous query return data?)
  #If we have values, we then read these values and classify them between former shows (date before actual date) and upcoming shows
  if described_artist:
    artist_former_shows = []
    artist_upcoming_shows = []
    
    for actual_show in described_artist.shows:
      venue = {
        "venue_id": actual_show.venue_id,
        "venue_name": actual_show.venue.name,
        "venue_image_link": actual_show.venue.image_link,
        "start_time": actual_show.start_time,
      }

      #if the date of the show is before now, it is a former show
      if actual_show.start_time < datetime.now():
        artist_former_shows.append(venue)
      else:
        #However, if the show is now or after now, it is an upcoming show
        artist_upcoming_shows.append(venue)

      #Now we can put these data in the artist_data, by following the data format expected by our template show_artist.html
      artist_data = {
        **described_artist.__dict__,
        "past_shows": artist_former_shows,
        "upcoming_shows": artist_upcoming_shows,
        "past_shows_count": len(artist_former_shows),
        "upcoming_shows_count": len(artist_upcoming_shows),
      }
      
      # We can then render our template (assuming nothing went wrong)
      return render_template("pages/show_artist.html", artist=artist_data)

    #If we reach this place, it means there was an error (because we were not able to render, meaning we were not able to execute all the previous intructions)
    return render_template("errors/404.html")


  return render_template('pages/show_artist.html', artist=artist_data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  #We retrieve the form by using the class ArtistForm | initilizing effectiveness through the request.form
  form = ArtistForm(request.form)
  
  #We query the artists from the database (the name and id)
  artist_query1 = Artist.query.with_entities(Artist.name, Artist.id)
  
  #We filter to consider only the case the id = artist_id
  artist_query2 = artist_query1.filter(Artist.id == artist_id)

  #As we are looking for an artist (with constraint unique on id) and that we may be in situation where artist_id does not exist as id, we shall get at most 1 (1 or 0)

  queried_artist = (artist_query2.one_or_none())

  #Then we check if we were able to find this artist from the database (if the test return true)
  #In that case, we can then render our edit_artist.html page with the queried_data of the artist

  if queried_artist:
    return render_template("forms/edit_artist.html", form=form, artist=queried_artist)

  #If we were not able to render, (so if we reach here), this means we had an error
  return render_template("errors/404.html", form=form)

  # TODO: populate form with fields from artist with ID <artist_id>

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  ###*** return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  #We retrieve the form by using the class ArtistForm | initilizing effectiveness through the request.form
  form = ArtistForm(request.form)
  
  #We check if the form is valid (and that we are in post method for the request). if ok, we get data from the form and then we perform the update transaciton in the database

  if request.method == "POST" and form.validate():
    form_name = request.form.get("name")
    form_city = request.form.get("city")
    form_state = request.form.get("state")
    form_phone = request.form.get("phone")
    form_image_link = request.form.get("image_link")
    form_facebook_link = request.form.get("facebook_link")
    form_website = request.form.get("website")
    #In case the seeking_venue was checked, we set the var to True, ortherwise, to false
    form_seeking_venue = True # We initialize it first
    if request.form.get("seeking_venue"):
      form_seeking_venue = True
    else:
      form_seeking_venue = False
    form_seeking_description = request.form.get("seeking_description")
    form_genres = request.form.getlist("genres")
    
    #We perform the transaction through a try / except / finally
    try:
      db.session.query(Artist).filter(Artist.id == artist_id).update(
        {
          "name": form_name,
          "city": form_city,
          "state": form_state,
          "phone": form_phone,
          "image_link": form_image_link,
          "facebook_link": form_facebook_link,
          "website": form_website,
          "seeking_venue": form_seeking_venue,
          "seeking_description": form_seeking_description,
          "genres": form_genres,
        }
      )
      
      db.session.commit()
      flash(f"Artist {form_name} was successfully edited!")
    
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash("Ooooooops. An error occurred. The Artist could not be edited.")
    
    finally:
      db.session.close()
    
    return redirect(url_for("show_artist", artist_id=artist_id))
  
  #if we reach here, this means it was not valid and we were not able to update and redirect
  
  artist_query1 = Artist.query.with_entities(Artist.name, Artist.id)
  artist_query2 = artist_query1.filter(Artist.id == artist_id)
  queried_artist = (artist_query2.one_or_none)
  
  return render_template("forms/edit_artist.html", form=form, artist=queried_artist)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  #We retrieve the form by using the class VenueForm | initilizing effectiveness through the request.form
  form = VenueForm(request.form)

  #We query the venues from the database (the name and id)
  venue_query1 = Venue.query.with_entities(Venue.name, Venue.id)

  #We filter to consider only the case the id = artist_id
  venue_query2 = venue_query1.filter(Venue.id == venue_id)
  
  #As we are looking for a venue (with constraint unique on id) and that we may be in situation where venue_id does not exist as id, we shall get at most 1 (1 or 0)

  queried_venue = (venue_query2.one_or_none())

  #Then we check if we were able to find this venue from the database (if the test return true)
  #In that case, we can then render our edit_venue.html page with the queried_data of the venue
  
  if queried_venue:
    return render_template("forms/edit_venue.html", form=form, venue=queried_venue)
  
  return render_template("errors/404.html", form=form)


  
  # TODO: populate form with values from venue with ID <venue_id>
  ###*** return render_template('forms/edit_venue.html', form=form, venue=venue)

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  #We retrieve the form by using the class VenueForm | initilizing effectiveness through the request.form
  form = VenueForm(request.form)


  #We check if the form is valid (and that we are in post method for the request). if ok, we get data from the form and then we perform the update transaciton in the database
  if request.method == "POST" and form.validate():
    form_name = request.form.get("name")
    form_city = request.form.get("city")
    form_state = request.form.get("state")
    form_address = request.form.get("address")
    form_phone = request.form.get("phone")
    form_image_link = request.form.get("image_link")
    form_facebook_link = request.form.get("facebook_link")
    form_website = request.form.get("website")
    #form_seeking_talent = request.form.get("seeking_talent", 'N')
    #Initializing the form_seeking_talent var
    form_seeking_talent = True
    if (request.form.get("seeking_talent")):
      form_seeking_talent = True
    else:
        form_seeking_talent = False
    form_seeking_description = request.form.get("seeking_description")
    form_genres = request.form.getlist("genres")
    
    #We perform the transaction through a try / except / finally
    try:
      db.session.query(Venue).filter(Venue.id == venue_id).update(
        {
          "name": form_name,
          "city": form_city,
          "state": form_state,
          "address": form_address,
          "phone": form_phone,
          "image_link": form_image_link,
          "facebook_link": form_facebook_link,
          "website": form_website,
          "seeking_talent": form_seeking_talent,
          "seeking_description": form_seeking_description,
          "genres": form_genres,
        }
      )
      
      db.session.commit()
      flash(f"Venue {form_name} was successfully edited!")
    
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash(f"Ooooooops. An error occurred: The Venue could not be edited.")
    
    finally:
      db.session.close()
  
    return redirect(url_for("show_venue", venue_id=venue_id))
  

  #if we reach here, this means it was not valid and we were not able to update and redirect
  
  venue_query1 = Venue.query.with_entities(Venue.name, Venue.id)
  venue_query2 = venue_query1.filter(Venue.id == venue_id)
  queried_venue = (venue_query2.one_or_none)

  
  return render_template("forms/edit_venue.html", form=form, venue=queried_venue)


  ###*** return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  
  #We initialize the form by using the class ArtistForm | initilizing effectiveness through the request.form
  artist_form = ArtistForm(request.form)

  #We can then render new_artist.html
  return render_template('forms/new_artist.html', form=artist_form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#


  #We retrieve the form by using the class ArtistForm | initilizing effectiveness through the request.form
  form = ArtistForm(request.form)

  #We check if the form is valid (and that we are in post method for the request). if ok, we get data from the form and then we perform the insert transaciton in the database
  if request.method == "POST" and form.validate():

    form_name = request.form.get("name")
    form_city = request.form.get("city")
    form_state = request.form.get("state")
    form_phone = request.form.get("phone")
    form_image_link = request.form.get("image_link")
    form_facebook_link = request.form.get("facebook_link")
    form_website = request.form.get("website")
    #In case the seeking_venue was checked, we set the var to True, ortherwise, to false
    form_seeking_venue = True # We initialize it first
    if request.form.get("seeking_venue"):
      form_seeking_venue = True
    else:
      form_seeking_venue = False
    form_seeking_description = request.form.get("seeking_description")
    form_genres = request.form.getlist("genres")

    #We perform the transaction through a try / except / finally
    try:
      artist = Artist(
        name=form_name,
        city=form_city,
        state=form_state,
        phone=form_phone,
        image_link=form_image_link,
        facebook_link=form_facebook_link,
        website=form_website,
        seeking_venue=form_seeking_venue,
        seeking_description=form_seeking_description,
        genres=form_genres,
      )  
      db.session.add(artist)
      
      db.session.commit()
      flash(f"Artist {form_name} was successfully listed!")
    
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash(f"Ooooooops. An error occurred. The Artist {form_name} could not be listed.")
    
    finally:
      db.session.close()
    
    return render_template('pages/home.html')
  
  
  #if we reach here, this means it was not valid and we were not able to insert and redirect
  
  got_form = ArtistForm(request.form)

  return render_template('forms/new_artist.html', form=got_form)

  #flash(f"Ooooooops. Form not valid.")

  #return render_template("forms/new_artist.html", form=form)
  


  # on successful db insert, flash success
  ###*** flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  ###*** return render_template('pages/home.html')

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#
  
  #We initialize the shows data
  shows_data = []
  
  #We query the shows from the database
  show_query1 = Show.query
  
  #We order the shows by the start_time
  show_query2 = show_query1.order_by(Show.start_time)
  
  #We fetch all the data
  queried_shows = show_query2.all()
  
  
  for actual_show in queried_shows:

    #We get the venue and artist data for the actual show
    actual_show_venue_id = actual_show.venue.id
    actual_show_venue_name = actual_show.venue.name
    actual_show_artist_id = actual_show.artist.id
    actual_show_artist_name = actual_show.artist.name
    actual_show_artist_image_link = actual_show.artist.image_link
    actual_show_start_time = actual_show.start_time

    #We can then add a show with these date in the shows_data var
    shows_data.append(
      {
        "venue_id": actual_show_venue_id,
        "venue_name": actual_show_venue_name,
        "artist_id": actual_show_artist_id,
        "artist_name": actual_show_artist_name,
        "artist_image_link": actual_show_artist_image_link,
        "start_time": actual_show_start_time,
      }
    )

  #Therefore, we can render the shows.html with the required shows_data

  return render_template("pages/shows.html", shows=shows_data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  
  form = ShowForm(request.form)
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  #We retrieve the form by using the class ShowForm | initilizing effectiveness through the request.form
  form = ShowForm(request.form)
  
  #We check if the form is valid (and that we are in post method for the request). if ok, we get data from the form and then we perform the insert transaciton in the database
  if request.method == "POST" and form.validate():
    
    form_venue_id = request.form.get("venue_id")
    form_artist_id = request.form.get("artist_id")
    form_start_time = request.form.get("start_time")
    
    #We perform the transaction through a try / except / finally
    try:
      show = Show(
        venue_id=form_venue_id,
        artist_id=form_artist_id,
        start_time=form_start_time,
      )
      db.session.add(show)
      
      db.session.commit()
      flash("Show was successfully listed!")
    
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash("Ooooooops. An error occurred. The Show could not be listed.")
    
    finally:
      db.session.close()
    
    return render_template('pages/home.html')
  
  #if we reach here, this means it was not valid and we were not able to insert and redirect
  got_form = ShowForm(request.form)

  return render_template('forms/new_show.html', form=got_form)

  # on successful db insert, flash success
  ###*** flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  ###*** return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
#'''
