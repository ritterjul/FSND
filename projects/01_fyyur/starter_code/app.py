#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import babel
from datetime import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
    __tablename__ = 'Show'
    venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column('start_time', db.DateTime, primary_key=True)
    artist = db.relationship('Artist')
    venue = db.relationship('Venue')

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    genres = db.relationship('VenueGenre', cascade='all, delete-orphan')
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String())
    website = db.Column(db.String())
    facebook_link = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    image_link = db.Column(db.String())
    shows = db.relationship('Show')

class VenueGenre(db.Model):
    __tablename__ = 'VenueGenre'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    name = db.Column(db.String(), nullable=False)

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    genres = db.relationship('ArtistGenre', cascade = 'all, delete-orphan')
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String())
    website = db.Column(db.String())
    facebook_link = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    image_link = db.Column(db.String())
    shows = db.relationship('Show')

class ArtistGenre(db.Model):
    __tablename__ = 'ArtistGenre'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    name = db.Column(db.String(), nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(value, format)

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
  data = []
  for (city, state) in db.session.query(Venue.city, Venue.state).distinct().all():
    area = {}
    area['city'] = city
    area['state'] = state
    area['venues'] = []
    for area_venue in db.session.query(Venue).filter(Venue.city == city).filter(Venue.state == state).all():
      venue = {}
      venue['id'] = area_venue.id
      venue['name'] = area_venue.name
      venue['num_upcoming_shows'] = db.session.query(Show).filter(Show.venue_id == area_venue.id).filter(Show.start_time > datetime.now()).count()
      area['venues'].append(venue)
    data.append(area)
  return render_template('pages/venues.html', areas=data)  

@app.route('/venues/search', methods=['POST'])
def search_venues():
  query = db.session.query(Venue.id, Venue.name).filter(Venue.name.ilike('%{0}%'.format(request.form.get('search_term'))))
  response = {'count': query.count(), 'data': query.all()}
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  data = {col: getattr(venue, col) for col in inspect(Venue).columns.keys()}
  data['genres'] = [genre.name for genre in db.session.query(VenueGenre).filter(VenueGenre.venue_id==venue_id).all()]
  data['past_shows'] = db.session.query(Show.artist_id, Show.start_time, Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link')).filter(Show.artist_id==Artist.id).filter(Show.venue_id==venue.id).filter(Show.start_time < datetime.now()).order_by(Show.start_time).all()
  data['past_shows_count'] = len(data['past_shows'])
  data['upcoming_shows'] = db.session.query(Show.artist_id, Show.start_time, Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link')).filter(Show.artist_id==Artist.id).filter(Show.venue_id==venue.id).filter(Show.start_time > datetime.now()).order_by(Show.start_time).all()
  data['upcoming_shows_count'] = len(data['upcoming_shows'])
  return render_template('pages/show_venue.html', venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  form.genres.data = [genre.name for genre in db.session.query(VenueGenre).filter(VenueGenre.venue_id==venue_id).all()]
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  body = {}
  try:
    venue = Venue.query.get(venue_id)
    venue.name = request.form.get('name')

    db.session.query(VenueGenre).filter(VenueGenre.venue_id == venue_id).filter(~VenueGenre.name.in_(request.form.getlist('genres'))).delete(synchronize_session=False)
    for genre in request.form.getlist('genres'):
      if db.session.query(VenueGenre).filter(VenueGenre.venue_id == venue_id).filter(VenueGenre.name == genre).count() < 1:
        venue.genres.append(VenueGenre(name=genre))

    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.address = request.form.get('address')
    venue.phone = request.form.get('phone')
    venue.website = request.form.get('website')
    venue.facebook_link = request.form.get('facebook_link')
    venue.seeking_talent = (request.form.get('seeking_talent') == 'y')
    venue.seeking_description = request.form.get('seeking_description')
    venue.image_link = request.form.get('image_link')

    db.session.commit()
    body['name'] = venue.name
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash('An error occurred. The venue could not be updated.')
  else:
    flash('Venue "' + body['name'] + '" was successfully updated!')
  return redirect(url_for('show_venue', venue_id=venue_id))

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  body = {'name': request.form.get('name')}
  try:
    venue = Venue(
      name=request.form.get('name'),
      genres=[VenueGenre(name=genre) for genre in request.form.getlist('genres')],
      city=request.form.get('city'),
      state=request.form.get('state'),
      address=request.form.get('address'),
      phone=request.form.get('phone'),
      website=request.form.get('website'),
      facebook_link=request.form.get('facebook_link'),
      seeking_talent=(request.form.get('seeking_talent') == 'y'),
      seeking_description=request.form.get('seeking_description'),
      image_link=request.form.get('image_link')
    )
    db.session.add(venue) 
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue "' + body['name'] + '" could not be listed.')
  else:
    flash('Venue "' + body['name'] + '" was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
      abort (400)
  else: 
    return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = db.session.query(Artist.id, Artist.name).order_by(Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  query = db.session.query(Artist.id, Artist.name).filter(Artist.name.ilike('%{0}%'.format(request.form.get('search_term'))))
  response = {'count': query.count(), 'data': query.all()}
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  data = {col: getattr(artist, col) for col in inspect(Artist).columns.keys()}
  data['genres'] = [genre.name for genre in artist.genres]
  data['past_shows'] = db.session.query(Show.venue_id, Show.start_time, Venue.name.label('venue_name'), Venue.image_link.label('venue_image_link')).filter(Show.artist_id == artist_id).filter(Show.venue_id == Venue.id).filter(Show.start_time < datetime.now()).order_by(Show.start_time).all()
  data['past_shows_count'] = len(data['past_shows'])
  data['upcoming_shows'] = db.session.query(Show.venue_id, Show.start_time, Venue.name.label('venue_name'), Venue.image_link.label('venue_image_link')).filter(Show.artist_id == artist_id).filter(Show.venue_id==Venue.id).filter(Show.start_time > datetime.now()).order_by(Show.start_time).all()
  data['upcoming_shows_count'] = len(data['upcoming_shows'])
  return render_template('pages/show_artist.html', artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  form.genres.data = [genre.name for genre in db.session.query(ArtistGenre).filter(ArtistGenre.artist_id==artist_id).all()]
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  body = {}
  try:
    artist = Artist.query.get(artist_id)
    artist.name = request.form.get('name')

    db.session.query(ArtistGenre).filter(ArtistGenre.artist_id == artist_id).filter(~ArtistGenre.name.in_(request.form.getlist('genres'))).delete(synchronize_session=False)
    for genre in request.form.getlist('genres'):
      if db.session.query(ArtistGenre).filter(ArtistGenre.artist_id == artist_id).filter(ArtistGenre.name == genre).count() < 1:
        artist.genres.append(ArtistGenre(name=genre))

    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    artist.website = request.form.get('website')
    artist.facebook_link = request.form.get('facebook_link')
    artist.seeking_venue = (request.form.get('seeking_venue') == 'y')
    artist.seeking_description = request.form.get('seeking_description')
    artist.image_link = request.form.get('image_link')

    db.session.commit()
    body['name'] = artist.name
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash('An error occurred. The artist could not be updated.')
  else:
    flash('Artist "' + body['name'] + '" was successfully updated!')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  body = {'name': request.form.get('name')}
  try:
    artist = Artist(
      name=request.form.get('name'),
      genres=[ArtistGenre(name=genre) for genre in request.form.getlist('genres')],
      city=request.form.get('city'),
      state=request.form.get('state'),
      phone=request.form.get('phone'),
      website=request.form.get('website'),
      facebook_link=request.form.get('facebook_link'),
      seeking_venue=(request.form.get('seeking_venue') == 'y'),
      seeking_description=request.form.get('seeking_description'),
      image_link=request.form.get('image_link')
    )
    db.session.add(artist) 
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist "' + body['name'] + '" could not be listed.')
  else:
    flash('Artist "' + body['name'] + '" was successfully listed!')
  return render_template('pages/home.html')

@app.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  error = False
  try:
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
      abort (400)
  else: 
    return jsonify({'success': True})

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = db.session.query(Show.artist_id, Show.venue_id, Show.start_time, (Artist.name).label('artist_name'), (Artist.image_link).label('image_link'), (Venue.name).label('venue_name')).filter(Show.artist_id == Artist.id).filter(Show.venue_id == Venue.id).order_by(Show.start_time).all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  try:
    artist = Artist.query.get(request.form.get('artist_id'))
    venue = Venue.query.get(request.form.get('venue_id'))
    show = Show(start_time=request.form.get('start_time'))
    show.artist = artist
    show.venue = venue
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    flash('Show was successfully listed!')
  return render_template('pages/home.html')

#  Errors
#  ----------------------------------------------------------------

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
