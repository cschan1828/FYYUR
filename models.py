from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genre = db.relationship('Venue_Genre', backref='Venue')
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_url = db.Column(db.String(500))
    facebook_url = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Venue')

    def __repr__(self):
        return '<Venue {v}>'.format(v=self)

    @property
    def serialize_short(self):
        return {
            'city': self.city,
            'state': self.state,
            'venues':[{
                'id': self.id,
                'name': self.name,
                'num_upcoming_shows': [s.serialize for s in self.shows if s.start_time>=datetime.utcnow()]
            }]
        }
    
    @property
    def serialize_long(self):
        venue = {
            'id': self.id,
            'name': self.name,
            'genres': [g.genre for g in self.genre],
            'state': self.state,
            'city': self.city,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_url,
            'seeking_talent': self.seeking_talent,
            'seeking_seeking_description': self.seeking_description,
            'image_link': self.image_url,
            'past_shows': [s.serialize for s in self.shows if s.start_time<datetime.utcnow()],
            'upcoming_shows': [s.serialize for s in self.shows if s.start_time>=datetime.utcnow()]
        }
        venue['past_shows_count'] = len(venue['past_shows'])
        venue['upcoming_shows_count'] = len(venue['upcoming_shows'])

        return venue

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genre = db.relationship('Artist_Genre', backref='Artist_Genre')
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_url = db.Column(db.String(500))
    facebook_url = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description =  db.Column(db.String(120))
    shows = db.relationship('Show',backref='Artist')

    @property
    def serialize_short(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    @property
    def serialize_long(self):
        artist = {
            'id': self.id,
            'name': self.name,
            'genres': [g.genre for g in self.genre],
            'state': self.state,
            'city': self.city,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_url,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_url,
            'past_shows': [s.serialize for s in self.shows if s.start_time<datetime.utcnow()],
            'upcoming_shows': [s.serialize for s in self.shows if s.start_time>=datetime.utcnow()]
        }

        artist['past_shows_count'] = len(artist['past_shows'])
        artist['upcoming_shows_count'] = len(artist['upcoming_shows'])

        return artist

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    start_time = db.Column(db.DateTime(timezone=False), nullable=False)

    @property
    def serialize(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': Venue.query.get(self.venue_id).name,
            'artist_id': self.artist_id,
            'artist_image_link': Artist.query.get(self.artist_id).name,
            'start_time': self.start_time.strftime('%m/%d/%Y')
        }


class Venue_Genre(db.Model):
    __tablename__ = 'Venue_Genre'
    
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    genre = db.Column(db.String(120), nullable=False)

class Artist_Genre(db.Model):
    __tablename__ = 'Artist_Genre'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    genre = db.Column(db.String(120), nullable=False)