from models import db, Users, Roles, Movie, TheaterTimeSlot, Theatre, Booking, Screen
from cache import cache
from datetime import datetime
from sqlalchemy import desc

@cache.memoize(50)
def get_all_users():
    users = Users.query.all()
    return users

@cache.memoize(50)
def get_user_username(email):
    user = Users.query.filter_by(email=email).first()
    return user

@cache.memoize(50)
def get_home_movies():
    today = datetime.now().date()
    print("In cache part")
    movie = Movie.query.filter(Movie.end_date >= today).order_by(Movie.date_added.desc()).limit(10).all()
    return movie

@cache.memoize(50)
def get_movies_by_end_date(current_date):
    movie = Movie.query.filter(Movie.end_date >= current_date).order_by(desc(Movie.date_added)).all()
    return movie

@cache.memoize(50)
def get_movies_by_movie_id(movie_id):
    print('########### get_movies_by_movie_id cache ##############')
    movie = Movie.query.filter_by(id = movie_id).first()
    return movie

@cache.memoize(50)
def get_movies_by_title(title):
    movie = Movie.query.filter_by(title = title).first()
    return movie

@cache.memoize(50)
def get_theatre_orderby_city():
    print('in get theatre order by city cache')
    theatre = Theatre.query.order_by(Theatre.city).all()
    return theatre

@cache.memoize(50)
def get_theatre_by_id(theatre_id):
    print('in get theatre by id cache')
    theatre = Theatre.query.filter_by(id=theatre_id).first()
    return theatre

@cache.memoize(50)
def TimeSlots_by_screenid(screen_id):
    timeslots = TheaterTimeSlot.query.filter_by(screen_id=screen_id).all()
    return timeslots

@cache.memoize(50)
def get_screens_by_screenid(screen_id):
    screen = Screen.query.filter_by(id=screen_id).first()
    return screen


def get_user_by_user_id(user_id):
    print('in get user by user id')
    user = Users.query.filter_by(id = user_id).first()
    return user

@cache.memoize(50)
def get_timeslot_by_theatreid_enddate(theatre_id):
    today = datetime.now().date()
    timeslot = TheaterTimeSlot.query.filter(TheaterTimeSlot.theater_id == theatre_id, TheaterTimeSlot.end_date >= today).all()
    return timeslot

@cache.memoize(50)
def get_timeslot_by_movieid(movie_id):
    timeslot = TheaterTimeSlot.query.filter_by(movie_id=movie_id).all()
    return timeslot

@cache.memoize(50)
def get_timeslot_by_id(slot_id):
    timeslot = TheaterTimeSlot.query.filter_by(id=slot_id).first()
    return timeslot