from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
from flask_migrate import Migrate
db = SQLAlchemy()



# TODO: connect to a local postgresql database
def db_setup(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db

    

    
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String(), default='')
    seeking_description = db.Column(db.String(), default='')
    seeking_talent = db.Column(db.Boolean, default=False)
    website = db.Column(db.String())
    genres = db.Column(ARRAY(db.String),nullable=False)
    create_at = db.Column(db.DateTime, default= datetime.now())

    shows = db.relationship('Show', backref='Venue', lazy='dynamic')
    
    def __init__(self, name, genres, address, city, state, phone,website, facebook_link, image_link,
                 seeking_talent=False, seeking_description=""):
        self.name = name
        self.genres = genres
        self.city = city
        self.state = state
        self.address = address
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.website =  website
        self.seeking_description = seeking_description
    
    def insert(self):
            db.session.add(self)
            db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
    def short(self):
        return{
            'id':self.id,
            'name':self.name,
        }
    
    def long(self):
        print(self)
        return{
            'id' :self.id,
            'name' :self.name,
            'city' : self.city,
            'state' :self.state,
        }
    
    def detail(self):
        return{
            'id' :self.id,
            'name' :self.name,
            'genres' : self.genres,
            'address' :self.address,
            'city' :self.city,
            'state':self.state,
            'phone' :self.phone,
            'website' :self.website,
            'facebook_link':self.facebook_link,
            'seeking_talent' :self.seeking_talent,
            'seeking_description' :self.seeking_description,
            'image_link' :self.image_link
        }
     








  

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'
    

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String,nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), default='')
    website = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Artist', lazy=True)
    create_at = db.Column(db.DateTime, default=datetime.now())

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    def __init__(self, name, genres, city, state, phone, image_link, website, facebook_link,
                 seeking_venue=False, seeking_description=""):
        self.name = name
        self.genres = genres
        self.city = city
        self.state = state
        self.phone = phone
        self.website =  website
        self.facebook_link = facebook_link
        self.seeking_description = seeking_description
        self.image_link = image_link
        
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def short(self):
        return{
            'id': self.id,
            'name':self.name,
        }
    
    def details(self):
        return{
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'city': self.city,
            'state':self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,

        }
class Show(db.Model):

    __tablename__ = 'Show'
    id = db.Column(db.Integer,primary_key=True)
    venue_id = db.Column(db.Integer, ForeignKey(Venue.id), nullable=False)
    artist_id = db.Column(db.Integer, ForeignKey(Artist.id), nullable=False)
    start_time = db.Column(db.String(), nullable=False)


    def __init__(self, venue_id,artist_id,start_time):
        self.venue_id = venue_id
        self.artist_id = artist_id
        self.start_time = start_time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def detail(self):
        return{
            'venue_id' :self.venue_id,
            'venue_name' :self.Venue.name,
            'artist_id' :self.artist_id,
            'artist_name' :self.Artist.name,
            'artist_image_link' :self.Artist.image_link,
            'start_time' :self.start_time
        }

    def artist_infos(self):
        return{
            'artist_id' :self.artist_id,
            'artist_name' :self.Artist.name,
            'artist_image_link' :self.Artist.image_link,
            'start_time' :self.start_time

        }
 
    
    def venue_infos(self):
        return{
            'venue_id' :self.venue_id,
            'venue_name' :self.Venue.name,
            'venue_image_link' :self.Venue.image_link,
            'start_time' :self.start_time
            
        }
