#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

with app.app_context():
  db.create_all()

migrate = Migrate(app, db)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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
  """
  Return a venues list to webpage.
  """

  ### Example Data
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  
  venues = [v.serialize_short for v in Venue.query.all()]
  return render_template('pages/venues.html', areas=venues);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  """
  Case-insensitive search on venues with partial string search.
  """

  ### Example Data
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

  search_term = request.form.get('search_term', '')
  query_results = Venue.query.filter(Venue.name.ilike("%{term}%".format(term=search_term))).all()
  response = {
    'count': len(query_results),
    'data': query_results
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  """
  Display a venue page with the given venue_id
  """

  ### Example Data
  # data={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }

  return render_template('pages/show_venue.html', venue=Venue.query.get(venue_id).serialize_long)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  """
  Populate a form for a venue creating request.
  """

  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  """
  Take a venue from a form and create a record using SQLAlchemy ORM.
  """
  try:
    new_venue = Venue(
      name=request.form.get('name', ''),
      city=request.form.get('city', ''),
      state=request.form.get('state', ''),
      address=request.form.get('address', ''),
      phone=request.form.get('phone', ''),
      image_url='#',
      facebook_url=request.form.get('facebook_link', '')
    )

    db.session.add(new_venue)

    # flush session
    db.session.flush()
    
    genres = request.form.getlist('genres')
    
    for genre in genres:
      new_venue_genre = Venue_Genre(
        venue_id=new_venue.id,
        genre=genre
      )
    
    db.session.add(new_venue_genre)
    db.session.commit()

    # on successful db insert, flash success
    flash("Venue {venue_name} was successfully listed!".format(venue_name=request.form['name']))
  
  except:
    flash("An error occurred. Venue {venue_name} could not be listed.".format(venue_name=request.form['name']))
    db.session.rollback()
  
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  """
  Take a venue_id and delete a record using SQLAlchemy ORM.
  """

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage.
  
  try:
    Venues = Venue.query.get(venue_id)

    for genre in Venues.genres:
      old_genre = Venue_Genre.query.get(genre.id)
      db.session.delete(old_genre)
    
    db.session.delete(venue)
    db.session.commit()

    flash("Venue: {venue_id} has been deleted successfully".format(venue_id=venue_id))

  except:
    flash("Fail to delete venue: {venue_id}.".format(venue_id=venue_id))
    db.session.rollback()
  
  finally:
    db.session.close()

  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  """
  Return an artists list to webpage.
  """

  ### Example Data
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]

  data = [a.serialize_short for a in Artist.query.all()]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  """
  Case-insensitive search on artists with partial string search.
  """
  ### Example Data
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  
  search_term = request.form.get('search_term', '')
  query_results = Artist.query.filter(Artist.name.ilike("%{term}%".format(term=search_term))).all()
  response = {
    'count': len(query_results),
    'data': query_results
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  """
  Show the venue page with the given venue_id
  """

  ### Example Data
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  
  return render_template('pages/show_artist.html', artist=Artist.query.get(artist_id).serialize_long)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  """
  Populate a form with fields from an artist with ID <artist_id> for editing.
  """
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  
  if not artist:
    return render_template('errors/404.html'), 404
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  """
  take values from the form submitted, and update existing 
  artist record with ID <artist_id> using the new attributes
  """
  try:
    new_artist = Artist(
      name = request.form.get('name',''),
      city = request.form.get('city',''),
      state = request.form.get('state',''),
      phone = request.form.get('phone',''),
      image_url = "#",
      facebook_url = request.form.get('facebook_link', '')
    )

    artist = Artist.query.get(artist_id)
    old_genres = artist.genre
    for genre in old_genres:
      old_genre = Artist_Genre.query.get(genre.id)
      db.session.delete(old_genre)
    
    for genre in new_genres:
      new_genre = Artist_Genre(
        artist_id = artist_id,
        genre = genre
      )
      db.session.add(new_genre)

  except:
    flash("Fail to update artist: {artist_id}.".format(artist_id=artist_id))
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  """
  Populate a form with fields from a venue with ID <venue_id> for editing.
  """
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  """
  take values from the form submitted, and update existing 
  artist record with ID <artist_id> using the new attributes
  """
  try:
    new_artist = Artist(
      name = request.form.get('name',''),
      city = request.form.get('city',''),
      state = request.form.get('state',''),
      phone = request.form.get('phone',''),
      image_url = "#",
      facebook_url = request.form.get('facebook_link', '')
    )

    artist = Artist.query.get(artist_id)
    old_genres = artist.genre
    for genre in old_genres:
      old_genre = Artist_Genre.query.get(genre.id)
      db.session.delete(old_genre)
    
    for genre in new_genres:
      new_genre = Artist_Genre(
        artist_id = artist_id,
        genre = genre
      )
      db.session.add(new_genre)

  except:
    flash("Fail to update artist: {artist_id}.".format(artist_id=artist_id))
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  """
  Populate a form for a artist creating request.
  """
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  """
  Take a artist from a form and create a record using SQLAlchemy ORM.
  """

  try:
    new_artist = Artist(
      name = request.form.get('name',''),
      city = request.form.get('city',''),
      state = request.form.get('state',''),
      phone = request.form.get('phone',''),
      image_url = "#",
      facebook_url = request.form.get('facebook_link', '')
    )

    db.session.add(new_artist)
    db.session.flush()

    # on successful db insert, flash success
    flash("Artist {artist_name} was successfully listed!".format(artist_name=request.form['name']))
    
    genres = request.form.getlist('genres')

    for genre in genres:
      new_artist_genre = Artist_Genre(
        artist_id = new_artist.id,
        genre = genre
      )
      db.session.add(new_artist_genre)
    
    db.session.commit()

  except:
    flash("Fail to list {artist_name}!".format(artist_name=request.form['name']))
    print(sys.exc_info())
    db.session.rollback()

  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  """
  Return a show list to webpage.
  """

  ### Example Data
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }]

  shows = [s.serialize for s in Show.query.all()]
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  """
  Populate a form for a show creating request.
  """
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  """
  Take a show from a form and create a record using SQLAlchemy ORM.
  """

  try:
    new_show = Show(
      artist_id = request.form.get('artist_id'),
      venue_id = request.form.get('venue_id'),
      start_time = request.form.get('start_time')
    )

    db.session.add(new_show)
    db.session.commit()
    
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  except:
    print(sys.exc_info())
    flash("Fail to list show!")
    db.session.rollback()
  finally:
    db.session.close()


  return render_template('pages/home.html')

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
'''
