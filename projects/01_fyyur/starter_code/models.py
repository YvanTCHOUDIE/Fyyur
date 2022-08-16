#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy


from forms import *
#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI] - Added Imports
#----------------------------------------------------------------------------#

from flask_migrate import Migrate

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

# [Yvan TCHOUDIE DJOMESSI] - Also added __table_args__ = {'quote': []} to avoid table with quote in the DB, which lead issues

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
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    facebook_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    

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
    website = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)
    genres = db.Column(db.ARRAY(db.String))
    seeking_description = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))

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
