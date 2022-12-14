#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from ast import dump
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from models import db_setup, Venue, Show, Artist
from flask_migrate import Migrate
from logging import Formatter, FileHandler
from flask_wtf import Form
import sys
from forms import *
from sqlalchemy import Table, Text
from sqlalchemy.exc import SQLAlchemyError
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = db_setup(app)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


    
    
    
    

    # # TODO: implement any missing fields, as a database migration using Flask-Migrate
    
      
 
# db.create_all()
     
          
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
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  currentArtist = Artist.query.order_by(Artist.create_at.desc()).limit(10).all();
  return render_template('pages/home.html',data=currentArtist)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
    current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
    venues = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
    venue_state_and_city = ''
    data = []

    #loop through venues to check for upcoming shows, city, states and venue information
    for venue in venues:
      #filter upcoming shows given that the show start time is greater than the current time
     
      upcoming_shows = venue.shows.filter(Show.start_time > current_time).all()
      if venue_state_and_city == venue.city + venue.state:
        data[len(data) - 1]["venues"].append({
          "id": venue.id,
          "name":venue.name,
          "num_upcoming_shows": len(upcoming_shows) # a count of the number of shows
        })
      else:
        venue_state_and_city == venue.city + venue.state
        data.append({
          "city":venue.city,
          "state":venue.state,
          "venues": [{
            "id": venue.id,
            "name":venue.name,
            "num_upcoming_shows": len(upcoming_shows)
          }]
        })


    return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  venue_getdataByid = Venue.query.filter(Venue.name.ilike('%' + request.form['search_term'] + '%'))
  venue_list = list(map(Venue.short, venue_getdataByid)) 
  response = {
    "count":len(venue_list),
    "data": venue_list
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
      venue_getdataByid = Venue.query.get(venue_id)
      if venue_getdataByid:
        venue_infos = Venue.detail(venue_getdataByid)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_shows_query = Show.query.options(db.joinedload(Show.Venue)).filter(Show.venue_id == venue_id).filter(Show.start_time > current_time).all()
        new_show = list(map(Show.artist_infos, new_shows_query))
        venue_infos["upcoming_shows"] = new_show
        venue_infos["upcoming_shows_count"] = len(new_show)
        past_shows_query = Show.query.options(db.joinedload(Show.Venue)).filter(Show.venue_id == venue_id).filter(Show.start_time <= current_time).all()
        past_shows = list(map(Show.artist_infos, past_shows_query))
        venue_infos["past_shows"] = past_shows
        venue_infos["past_shows_count"] = len(past_shows)

    # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
        return render_template('pages/show_venue.html', venue=venue_infos)
      return render_template('errors/404.html')

  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TOD
  # O: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    try:
    
      new_venue = Venue(
        name=request.form['name'],
        genres=request.form.getlist('genres'),
        address=request.form['address'],
        city=request.form['city'],
        state=request.form['state'],
        phone=request.form['phone'],
        website=request.form['website_link'],
        facebook_link=request.form['facebook_link'],
        image_link=request.form['image_link'],
        seeking_talent=request.form['seeking_talent'],
        seeking_description=request.form['seeking_description'],
      )
      #insert new venue records into the db
      Venue.insert(new_venue)
      # on successful db insert, flash success
      flash('New Venue ' + request.form['name'] + ' was successfully listed!')
    except SQLAlchemyError as e:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      flash('An error occurred. when persisting Venue ' + request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')

@app.route('/venues/delete/<int:venue_id>', methods=['DELETE','GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    
    db.session.commit()
    flash('Record Venue Delete success')
  except:
    db.session.rollback() 
    flash('Cannot Delete Record Because they are already linked to an Show ')
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return  redirect(url_for('index'))
  
 

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=Artist.query.all()
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
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
    artist_regard= Artist.query.filter(Artist.name.ilike('%' + request.form['search_term'] + '%'))
    artist_list = list(map(Artist.short,  artist_regard)) 
    response = {
    "count":len(artist_list),
    "data": artist_list
  }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
    # data=Artist.query.all()
    
  artist_regard= Artist.query.get(artist_id)
  if artist_regard:
    artist_infos = Artist.details(artist_regard)
    #get the current system time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_shows_query = Show.query.options(db.joinedload(Show.Artist)).filter(Show.artist_id == artist_id).filter(Show.start_time > current_time).all()
    new_shows_list = list(map(Show.venue_infos, new_shows_query))
    artist_infos["upcoming_shows"] = new_shows_list
    artist_infos["upcoming_shows_count"] = len(new_shows_list)
    past_shows_query = Show.query.options(db.joinedload(Show.Artist)).filter(Show.artist_id == artist_id).filter(Show.start_time <= current_time).all()
    past_shows_list = list(map(Show.venue_infos, past_shows_query))
    artist_infos["past_shows"] = past_shows_list
    artist_infos["past_shows_count"] = len(past_shows_list)
    return render_template('pages/show_artist.html', artist=artist_infos)
  return render_template('errors/404.html')
   
    

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm(request.form)
  artist_getdataByid = Artist.query.get(artist_id)
  if artist_getdataByid:
    artist_infos = Artist.details(artist_getdataByid)
    form.name.data = artist_infos["name"]
    form.genres.data = artist_infos["genres"];
    form.city.data = artist_infos["city"]
    form.state.data = artist_infos["state"]
    form.phone.data = artist_infos["phone"]
    form.website_link.data = artist_infos["website"]
    form.facebook_link.data = artist_infos["facebook_link"]
    form.seeking_venue.data = artist_infos["seeking_venue"]
    form.seeking_description.data = artist_infos["seeking_description"]
    form.image_link.data = artist_infos["image_link"]
    return render_template('forms/edit_artist.html', form=form, artist=artist_infos)
  return render_template('errors/404.html')

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    form = ArtistForm(request.form)
    artist_getdataByid = Artist.query.get(artist_id)
    if artist_getdataByid:
        if form.validate():
            seeking_venue = False
            seeking_description = ''
            if 'seeking_venue' in request.form:
                seeking_venue = request.form['seeking_venue'] == 'y'
            if 'seeking_description' in request.form:
                seeking_description = request.form['seeking_description']
            setattr(artist_getdataByid, 'name', request.form['name'])
            setattr(artist_getdataByid, 'genres', request.form.getlist('genres'))
            setattr(artist_getdataByid, 'city', request.form['city'])
            setattr(artist_getdataByid, 'state', request.form['state'])
            setattr(artist_getdataByid, 'phone', request.form['phone'])
            setattr(artist_getdataByid, 'website', request.form['website_link'])
            setattr(artist_getdataByid, 'facebook_link', request.form['facebook_link'])
            setattr(artist_getdataByid, 'image_link', request.form['image_link'])
            setattr(artist_getdataByid, 'seeking_description', seeking_description)
            setattr(artist_getdataByid, 'seeking_venue', seeking_venue)
            Artist.update(artist_getdataByid)
            return redirect(url_for('show_artist', artist_id=artist_id))
        else:
            print(form.errors)
    return render_template('errors/404.html'), 404

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_getdataByid = Venue.query.get(venue_id)
  if venue_getdataByid:
    venue_infos = Venue.detail(venue_getdataByid)
    form.name.data = venue_infos["name"]
    form.genres.data = venue_infos["genres"]
    form.address.data = venue_infos["address"]
    form.city.data = venue_infos["city"]
    form.state.data = venue_infos["state"]
    form.phone.data = venue_infos["phone"]
    form.website_link.data = venue_infos["website"]
    form.facebook_link.data = venue_infos["facebook_link"]
    form.seeking_talent.data = venue_infos["seeking_talent"]
    form.seeking_description.data = venue_infos["seeking_description"]
    form.image_link.data = venue_infos["image_link"]
    return render_template('forms/edit_venue.html', form=form, venue=venue_infos)
  return render_template('errors/404.html')

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form)
    venue_getdataByid = Venue.query.get(venue_id)
    if venue_getdataByid:
        if form.validate():
            seeking_talent = False
            seeking_description = ''
            if 'seeking_talent' in request.form:
                seeking_talent = request.form['seeking_talent'] == 'y'
            if 'seeking_description' in request.form:
                seeking_description = request.form['seeking_description']
            setattr(venue_getdataByid, 'name', request.form['name'])
            setattr(venue_getdataByid, 'genres', request.form.getlist('genres'))
            setattr(venue_getdataByid, 'address', request.form['address'])
            setattr(venue_getdataByid, 'city', request.form['city'])
            setattr(venue_getdataByid, 'state', request.form['state'])
            setattr(venue_getdataByid, 'phone', request.form['phone'])
            setattr(venue_getdataByid, 'website', request.form['website_link'])
            setattr(venue_getdataByid, 'facebook_link', request.form['facebook_link'])
            setattr(venue_getdataByid, 'image_link', request.form['image_link'])
            setattr(venue_getdataByid, 'seeking_description', seeking_description)
            setattr(venue_getdataByid, 'seeking_talent', seeking_talent)
            Venue.update(venue_getdataByid)
            return redirect(url_for('show_venue', venue_id=venue_id))
        else:
            print(form.errors)
    return render_template('errors/404.html'), 404 

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  # on successful db insert, flash success
      try:
        seeking_venue = False
        seeking_description = ''
        current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
        if 'seeking_venue' in request.form:
          seeking_venue = request.form['seeking_venue'] == 'y'
        if 'seeking_description' in request.form:
          seeking_description = request.form['seeking_description']
          new_artist = Artist(
          name=request.form['name'],
          genres=request.form.getlist('genres'),
          city=request.form['city'],
          state= request.form['state'],
          phone=request.form['phone'],
          website=request.form['website_link'],
          image_link=request.form['image_link'],
          facebook_link=request.form['facebook_link'],
          seeking_venue=seeking_venue,
          seeking_description=seeking_description,
        
        )
        Artist.insert(new_artist)
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
      except SQLAlchemyError as e:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
          flash('An error occurred. When  Artist listing ' + request.form['name'] + 'could not be listed. ')

      return redirect(url_for('artists'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
    show_regard = Show.query.options(db.joinedload(Show.Venue), db.joinedload(Show.Artist)).all()
    data = list(map(Show.detail, show_regard))
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
      
    try:
      new_show = Show(
        venue_id=request.form['venue_id'],
        artist_id=request.form['artist_id'],
        start_time=request.form['start_time'],
      )
      Show.insert(new_show)

    # on successful db insert, flash success
      flash('Show was successfully listed!')
    except SQLAlchemyError as e:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      flash('An error occured. Show could not be listed.')
    return render_template('pages/home.html')

  # # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


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



# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
