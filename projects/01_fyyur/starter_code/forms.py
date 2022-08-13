from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL

#----------------------------------------------------------------------------#
# [Yvan TCHOUDIE DJOMESSI] - Added Imports
#----------------------------------------------------------------------------#
from flask_wtf import FlaskForm 
import enum
import re


class Genre(enum.Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    HipHop = 'Hip-Hop'
    HeavyMetal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    MusicalTheatre = 'Musical Theatre'
    pop = 'Pop'
    Punk='Punk'
    RandB='R&B'
    Reggae='Reggae'
    RocknRoll = 'Rock n Roll'
    Soul='Soul'
    Other='Other'
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class State(enum.Enum):
    AL='AL'
    AK='AK'
    AZ='AZ'
    AR='AR'
    CA='CA'
    CO='CO'
    CT='CT'
    DE='DE'
    DC='DC'
    FL='FL'
    GA='GA'
    HI='HI'
    ID='ID'
    IL='IL'
    IN='IN'
    IA='IA'
    KS='KS'
    KY='KY'
    LA='LA'
    ME='ME'
    MT='MT'
    NE='NE'
    NV='NV'
    NH='NH'
    NJ='NJ'
    NM='NM'
    NY='NY'
    NC='NC'
    ND='ND'
    OH='OH'
    OK='OK'
    OR='OR'
    MD='MD'
    MA='MA'
    MI='MI'
    MN='MN'
    MS='MS'
    MO='MO'
    PA='PA'
    RI='RI'
    SC='SC'
    SD='SD'
    TN='TN'
    TX='TX'
    UT='UT'
    VT='VT'
    VA='VA'
    WA='WA'
    WV='WV'
    WI='WI'
    WY='WY'
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


def is_valid_phone(number):    
    regex = re.compile('^\(?([0-9]{2}|[0-9]{3})\)?[-. ]?([0-9]{2}|[0-9]{3})[-. ]?([0-9]{2}|[0-9]{3})[-. ]?([0-9]{2}|[0-9]{3})$')
    return regex.match(number)


def validate(self):
    rv = FlaskForm.validate(self)
    if not rv:
        return False
    if not is_valid_phone(self.phone.data):
        self.phone.errors.append('Invalid phone.')
        return False
    if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
        self.genres.errors.append('Invalid genres.')
        return False
    if self.state.data not in dict(State.choices()).keys():
        self.state.errors.append('Invalid state.')
        return False
        # if pass validation
    return True


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', 
        validators=[DataRequired()],
        choices=Genre.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', 
        validators=[DataRequired()],
        #choices=genres_list
        choices=Genre.choices()
    )

    #----------------------------------------------------------------------------#
    # [Yvan TCHOUDIE DJOMESSI] - DONE
    #----------------------------------------------------------------------------#

    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', 
        validators=[DataRequired()],
        choices=State.choices()
            
    )
    phone = StringField(
        # TODO implement validation logic for phone 
        'phone',
        validators=[DataRequired()],
    )
    #----------------------------------------------------------------------------#
    # [Yvan TCHOUDIE DJOMESSI] - DONE
    #----------------------------------------------------------------------------#
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', 
        validators=[DataRequired()],
        choices=Genre.choices()
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
     )

     #----------------------------------------------------------------------------#
    # [Yvan TCHOUDIE DJOMESSI] - DONE
    #----------------------------------------------------------------------------#

    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )

