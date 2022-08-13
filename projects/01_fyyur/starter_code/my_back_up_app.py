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

class Venue(db.Model):
    __tablename__ = 'venue'
    __table_args__ = {'quote': []}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #----------------------------------------------------------------------------#
    # [Yvan TCHOUDIE DJOMESSI] - DONE
    #----------------------------------------------------------------------------#

class Artist(db.Model):
    __tablename__ = 'artist'
    __table_args__ = {'quote': []}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #----------------------------------------------------------------------------#
    # [Yvan TCHOUDIE DJOMESSI] - DONE - Also updated 'genres' to be rather a list
    #----------------------------------------------------------------------------#

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI] - DONE - Also updated 'genres' to be rather a list
#----------------------------------------------------------------------------#

class Show(db.Model):
    __tablename__ = "show"
    __table_args__ = {'quote': []}

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
    start_time = db.Column(db.DateTime())
    venue = db.relationship("Venue", backref=db.backref("shows", cascade="all, delete"))
    artist = db.relationship(
        "Artist", backref=db.backref("shows", cascade="all, delete")
    )

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

  venues = (
        Venue.query.with_entities(Venue.id, Venue.name, Venue.state, Venue.city)
        .order_by(Venue.city, Venue.state)
        .all()
    )

  data = []
  previous_location = None
  i = -1

  for venue in venues:
    current_location = f"{venue.city}, {venue.state}"
    if previous_location != current_location:
      
      data.append({"city": venue.city, "state": venue.state, "venues": []})
      i += 1
      previous_location = current_location

    
    data[i]["venues"].append(
      {
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": Show.query.filter(
            db.and_(Show.venue_id == venue.id, Show.start_time > datetime.now())
        ).count(),
      }
    )

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#


  search_term = request.form.get('search_term', '').strip()
  venues = (
    Venue.query.with_entities(Venue.id, Venue.name)
    .filter(Venue.name.ilike(f"%{search_term}%"))
    .all()
  )

  response = {
    "count": len(venues),
    "data": [
      {
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": Show.query.filter(
          db.and_(Show.venue_id == venue.id, Show.start_time > datetime.now())
          ).count(),
      }
      for venue in venues
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


  venue = Venue.query.get(venue_id)
  if venue:
    past_shows = []
    upcoming_shows = []
    
    for show in venue.shows:
      artist = {
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time,
      }

      if show.start_time < datetime.now():
          past_shows.append(artist)
      else:
          upcoming_shows.append(artist)
    
    data = {
      **venue.__dict__,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template("pages/show_venue.html", venue=data)

  return render_template("errors/404.html")
  ###*** data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  ###*** return render_template('pages/show_venue.html', venue=data)
  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  
  form = VenueForm(request.form)
  #form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE - Also added request.form as attribute of VenueForm(), since The object instanciation needs the Form. This is what allow to set the data. I also applied it on other places where I use the forms
  #----------------------------------------------------------------------------#


  #form = VenueForm()
  form = VenueForm(request.form)
  
  if request.method == "POST" and form.validate():
    try:
      venue = Venue(
        name=request.form.get("name"),
        city=request.form.get("city"),
        state=request.form.get("state"),
        address=request.form.get("address"),
        phone=request.form.get("phone"),
        image_link=request.form.get("image_link"),
        facebook_link=request.form.get("facebook_link"),
        website=request.form.get("website"),
        seeking_talent=True if request.form.get("seeking_talent") else False,
        seeking_description=request.form.get("seeking_description"),
        genres=request.form.getlist("genres"),
      )
      db.session.add(venue)
      db.session.commit()

      venue_name = venue.name
      flash(f"Venue {venue_name} was successfully listed!")
    except:
      db.session.rollback()
      print(sys.exc_info())

      venue_name = request.form.get("name")
      flash(f"An error occurred. Venue {venue_name} could not be listed.")
    finally:
      db.session.close()

    return redirect(url_for("index"))

  return render_template("forms/new_venue.html", form=form)

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

  try:
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    db.session.delete(venue)
    db.session.commit()

    flash(f"The venue {venue.name} has been successfully deleted.")
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash(f"Ooooooops. An error occurred. Venue {venue.name} could not be deleted.")
  finally:
    db.session.close()
  
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
  data = []
  data = Artist.query.with_entities(Artist.id, Artist.name).all()
  
  return render_template('pages/artists.html', artists=data)

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

  search_term = request.form.get('search_term').strip()

  artists = (
    Artist.query.with_entities(Artist.id, Artist.name)
    .filter(Artist.name.ilike(f"%{search_term}%"))
    .all()
  )
  
  response = {
    "count": len(artists),
    "data": [
      {
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": Show.query.filter(
          db.and_(
            Show.artist_id == artist.id, Show.start_time > datetime.now()
          )
        ).count(),
      }
      for artist in artists
    ],
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  artist = Artist.query.get(artist_id)
  if artist:
    past_shows = []
    upcoming_shows = []
    
    for show in artist.shows:
      venue = {
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time,
      }

      if show.start_time < datetime.now():
        past_shows.append(venue)
      else:
        upcoming_shows.append(venue)

      data = {
        **artist.__dict__,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
      }
      
      return render_template("pages/show_artist.html", artist=data)

    return render_template("errors/404.html")


  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  

  #form = ArtistForm()
  form = ArtistForm(request.form)
  
  artist = (
    Artist.query.with_entities(Artist.name, Artist.id)
    .filter(Artist.id == artist_id)
    .one_or_none()
  )

  if artist:
    return render_template("forms/edit_artist.html", form=form, artist=artist)

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


 

  #form = ArtistForm()
  form = ArtistForm(request.form)
  
  if request.method == "POST" and form.validate():
    try:
      db.session.query(Artist).filter(Artist.id == artist_id).update(
        {
          "name": request.form.get("name"),
          "city": request.form.get("city"),
          "state": request.form.get("state"),
          "phone": request.form.get("phone"),
          "image_link": request.form.get("image_link"),
          "facebook_link": request.form.get("facebook_link"),
          "website": request.form.get("website"),
          "seeking_venue": True
          if request.form.get("seeking_venue")
          else False,
          "seeking_description": request.form.get("seeking_description"),
          "genres": request.form.getlist("genres"),
        }
      )
      
      db.session.commit()
      flash(f"Artist was successfully edited!")
    
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash(f"An error occurred. Artist could not be edited.")
    finally:
      db.session.close()
    
    return redirect(url_for("show_artist", artist_id=artist_id))
  
  artist = (
    Artist.query.with_entities(Artist.name, Artist.id)
    .filter(Artist.id == artist_id)
    .one_or_none()
  )
  
  return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  #form = VenueForm()
  form = VenueForm(request.form)
  
  venue = (
    Venue.query.with_entities(Venue.name, Venue.id)
    .filter(Venue.id == venue_id)
    .one_or_none()
  )
  
  if venue:
    return render_template("forms/edit_venue.html", form=form, venue=venue)
  
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

  

  #form = VenueForm()
  form = VenueForm(request.form)
  
  if request.method == "POST" and form.validate():
    try:
      db.session.query(Venue).filter(Venue.id == venue_id).update(
        {
          "name": request.form.get("name"),
          "city": request.form.get("city"),
          "state": request.form.get("state"),
          "address": request.form.get("address"),
          "phone": request.form.get("phone"),
          "image_link": request.form.get("image_link"),
          "facebook_link": request.form.get("facebook_link"),
          "website": request.form.get("website"),
          "seeking_talent": request.form.get("seeking_talent", False),
          "seeking_description": request.form.get("seeking_description"),
          "genres": request.form.getlist("genres"),
        }
      )
      db.session.commit()
      flash(f"The Venue was successfully edited!")
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash(f"Ooooooops. An error occurred: The Venue could not be edited.")
    finally:
      db.session.close()
  
    return redirect(url_for("show_venue", venue_id=venue_id))
  
  venue = (
    Venue.query.with_entities(Venue.name, Venue.id)
    .filter(Venue.id == venue_id)
    .one_or_none()
  )
  
  return render_template("forms/edit_venue.html", form=form, venue=venue)


  ###*** return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  
  #form = ArtistForm()
  form = ArtistForm(request.form)
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  form = ArtistForm(request.form)
  
  if request.method == "POST" and form.validate():
    try:
      artist = Artist(
        name=request.form.get("name"),
        city=request.form.get("city"),
        state=request.form.get("state"),
        phone=request.form.get("phone"),
        image_link=request.form.get("image_link"),
        facebook_link=request.form.get("facebook_link"),
        website=request.form.get("website"),
        seeking_venue=True if request.form.get("seeking_venue") else False,
        seeking_description=request.form.get("seeking_description"),
        genres=request.form.getlist("genres "),
      )
      
      db.session.add(artist)
      db.session.commit()
      
      artist_name = artist.name
      flash(f"Artist {artist_name} was successfully listed!")
    except:
      db.session.rollback()
      print(sys.exc_info())

      artist_name = request.form.get("name")
      flash(f"Ooooooops. An error occurred. The Artist {artist_name} could not be listed.")
    finally:
      db.session.close()
    
    return render_template('pages/home.html')
  
  return "phone data" + request.form.get("name")

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
  
  data = []
  shows = Show.query.order_by(Show.start_time).all()
  
  for show in shows:
    data.append(
      {
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time,
      }
    )

  return render_template("pages/shows.html", shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  
  #form = ShowForm()
  form = ShowForm(request.form)
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  #----------------------------------------------------------------------------#
  # [Yvan TCHOUDIE DJOMESSI] - DONE
  #----------------------------------------------------------------------------#

  #form = ShowForm()
  form = ShowForm(request.form)
  
  if request.method == "POST" and form.validate():
    try:
      show = Show(
        venue_id=request.form.get("venue_id"),
        artist_id=request.form.get("artist_id"),
        start_time=request.form.get("start_time"),
      )
      
      db.session.add(show)
      db.session.commit()
      flash(f"Show was successfully listed!")
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash("An error occurred. Show could not be listed.")
    finally:
      db.session.close()
    
    return render_template('pages/home.html')
  
  return render_template("forms/new_show.html", form=form)
  

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
