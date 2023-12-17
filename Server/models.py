from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_security import UserMixin, RoleMixin
from sqlalchemy import event

Base = declarative_base
db = SQLAlchemy()


roles_users = db.Table('roles_users', 
                       db.Column('user_id', db.Integer(), db.ForeignKey('Users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('Roles.id'))) 


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable = False)
    password = db.Column(db.String(1000), nullable=False)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Roles', secondary = roles_users,
                            backref = db.backref('users' , lazy = 'subquery'))
    date_joined = db.Column(db.Date, default=datetime.datetime.utcnow)
    email_preference = db.Column(db.Boolean, default=True)


class Roles(db.Model, RoleMixin):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Theatre(db.Model):
    __tablename__ = 'Theatre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    screens = db.relationship('Screen', back_populates='theatre', lazy='subquery')


class Screen(db.Model):
    __tablename__ = 'Screen'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    technology = db.Column(db.String(100), nullable=False)
    seat_capacity = db.Column(db.Integer, nullable=False)
    available_capacity = db.Column(db.Integer, nullable=False)
    theatre_id = db.Column(db.Integer, db.ForeignKey('Theatre.id'), nullable=False)
    premium = db.Column(db.Integer, nullable=False)
    theatre = db.relationship('Theatre', back_populates='screens', lazy='subquery')


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    boxart = db.Column(db.String(255))
    director = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=False)
    cast = db.Column(db.String)
    duration = db.Column(db.String, nullable=False)
    language = db.Column(db.String)
    rate = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100))
    start_date = db.Column(db.Date, nullable=False) 
    end_date = db.Column(db.Date, nullable=False)
    date_added = db.Column(db.Date, default=datetime.datetime.utcnow)


class TheaterTimeSlot(db.Model):
    __tablename__ = 'TheaterTimeSlot'
    id = db.Column(db.Integer, primary_key=True)
    theater_id = db.Column(db.Integer, db.ForeignKey('Theatre.id'), nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('Screen.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False) 

    theater = db.relationship('Theatre', backref='time_slots')
    screen = db.relationship('Screen', backref='time_slots')
    movie = db.relationship('Movie', backref='time_slots') 


class Booking(db.Model):
    __tablename__ = 'Booking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('Theatre.id'), nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('Screen.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)  
    entry_date = db.Column(db.Date, default=datetime.datetime.utcnow)  

    user = db.relationship('Users', backref='bookings')
    movie = db.relationship('Movie', backref='bookings')
    theater = db.relationship('Theatre', backref='bookings')
    screen = db.relationship('Screen', backref='bookings')

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship('Users', backref='ratings')
    movie = db.relationship('Movie', backref='ratings')    