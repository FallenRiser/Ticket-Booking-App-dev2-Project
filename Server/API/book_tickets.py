from flask import current_app, request, jsonify, make_response
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
import json
from models import db
from models import Users,Roles,roles_users, Theatre, Movie, Screen, TheaterTimeSlot, Booking, Ratings
from API.validation import UserError, PropertyExistError, TheatreError
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime, timedelta
from security import datastore
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request
from sqlalchemy import and_, or_, not_


class book_tickets(Resource):

    @jwt_required()
    def post(self,movie_id):

        print(movie_id)
        movieid = request.form['movieid']
        city = request.form['city']
        city = city.capitalize()
        date_str = request.form['date']
        print(movie_id,city,date_str)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        print('###############################')
        theatres_and_screens = TheaterTimeSlot.query.filter(TheaterTimeSlot.theater_id == Theatre.id,
                TheaterTimeSlot.screen_id == Screen.id, TheaterTimeSlot.end_date > date,
                TheaterTimeSlot.movie_id == movieid).all()
        print(theatres_and_screens)
        distinct_theater_screen = set((theater.theater_id, theater.screen_id) for theater in theatres_and_screens)

        theatres_and_screens_list = []
        theatres_and_screens_dict = {}

        for theater_id, screen_id in distinct_theater_screen:
            print('theater',theater_id, city)
            theater = Theatre.query.filter(Theatre.id == theater_id, Theatre.city == city ).first()
            screen = Screen.query.filter_by(id=screen_id).first()
            print('theater',theater)
            
                

            if theater is not None and screen is not None:
                time_slot = TheaterTimeSlot.query.filter_by(theater_id=theater_id, screen_id=screen_id, movie_id=movieid).first()
                if time_slot is not None:

                    bookings = Booking.query.filter_by(theater_id=theater_id, screen_id=screen_id, movie_id=movieid, booking_date=date).all()
                    print('bookings', bookings)
                    if bookings:
                        total_booked_tickets = sum(booking.num_tickets for booking in bookings)
                        available_capacity = screen.seat_capacity - total_booked_tickets
                    else:
                        print('available capacity', screen.seat_capacity)
                        available_capacity = screen.seat_capacity

                    if theater in theatres_and_screens_dict:
                        theatres_and_screens_dict[theater]["screens"].append({
                    "screen_id": screen.id,
                    "screen_number": screen.number,
                    "technology": screen.technology,
                    "seat_capacity": screen.seat_capacity,
                    "available_capacity": screen.available_capacity,
                    "premium": screen.premium,
                    "start_time": time_slot.start_time.strftime("%H:%M"),
                    "end_time": time_slot.end_time.strftime("%H:%M")
                })
                    else:
                        theatres_and_screens_dict[theater] = {
                            "theater_id": theater.id,
                            "theater_name": theater.name,
                            "theatre_city": theater.city,
                            "screens": [{
                                "screen_id": screen.id,
                                "screen_number": screen.number,
                                "technology": screen.technology,
                                "seat_capacity": screen.seat_capacity,
                                "available_capacity": available_capacity,
                                "premium": screen.premium,
                                "start_time": time_slot.start_time.strftime("%H:%M"),
                                "end_time": time_slot.end_time.strftime("%H:%M")
                            }]
                        }

                       
        if theatres_and_screens_dict == {}:
            #return make_response(jsonify({"message": "No Theatres found"}),400)
            return make_response(jsonify({"message": "No Theatres Found"}), 404)
        else:
            theatres_and_screens_list = list(theatres_and_screens_dict.values())
        

            return make_response(jsonify(theatres_and_screens_list), 200)  


class Booking_Tickets(Resource):
    @jwt_required()
    def get(self, user_id):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)
    
        current_user_id = get_jwt_identity()

        user_id = user_id
        booking_info = []
        book = Booking.query.filter_by(user_id = user_id).all()
        for booking in book:
            bookdate = booking.booking_date
            booktime = booking.booking_time.strftime("%H:%M")
            bookedpersons = booking.num_tickets
            amount = booking.total_amount
            theatre = Theatre.query.filter_by(id = booking.theater_id).first()
            if theatre:
                theatre_name = theatre.name
                theatre_city = theatre.city
            screen = Screen.query.filter_by(id = booking.screen_id).first()
            if screen:
                screen_no = screen.number
                screen_tech = screen.technology
            movie = Movie.query.filter_by(id = booking.movie_id).first()
            if movie:
                movie_name = movie.title
                movie_id = movie.id
            print('HERE!!!')    
            usr_rating = Ratings.query.filter_by(user_id = booking.user_id, movie_id = movie_id).first()
            if usr_rating:
                rating = usr_rating.rating
            else:
                rating = 0        
            all_details = {'theatre_name': theatre_name,
                           'theatre_city': theatre_city,
                           'movie_id': movie_id,
                           'screen_number': screen_no,
                           'screen_tech': screen_tech,
                           'movie_name': movie_name,
                           'booking_date' : bookdate,
                           'booking_time' : booktime,
                           'booked_tickets': bookedpersons,
                           'amount' : amount,
                           'rating': rating}
            booking_info.append(all_details)
        print(booking_info)    

        return make_response(jsonify(booking_info),200)



    @jwt_required()
    def post(self):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)
    
        current_user_id = get_jwt_identity()
        print('#####')
        data = request.get_json()
        movie_id = data.get('movieId')
        theatre_id = data.get('theaterId')
        screen_id = data.get('screenId')
        user_id = data.get('user_id')
        no_people = data.get('numPeople')
        amount = data.get('fare')
        time_str = data.get('time')
        date_str = data.get('date')

        print(movie_id, screen_id, amount, time_str, date_str, user_id,theatre_id, no_people)

        print('########################################################################################')

        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        start_time_str = time_str[:5]
        format = "%H:%M"
        time = datetime.strptime(start_time_str, format).time()
        print(time)
        
        #print(start_time_str)
        #time = datetime.strptime(start_time_str, "%H:%M")
        print(time)

        if (movie_id is None or theatre_id is None or screen_id is None or user_id is None or no_people is None or amount is None
            or time is None or date is None):

            return make_response(jsonify({'message': 'Invalid Details recieved'}),400)    
        else:

            bookings = Booking.query.filter_by(theater_id=theatre_id, screen_id=screen_id, movie_id=movie_id, booking_date=date).all()
            screen = Screen.query.filter_by(id=screen_id).first()
            print('bookings', bookings)
            if bookings:
                total_booked_tickets = sum(booking.num_tickets for booking in bookings)
                available_capacity = screen.seat_capacity - total_booked_tickets
            else:
                #print('available capacity', screen.seat_capacity)
                
                available_capacity = screen.seat_capacity

            if available_capacity > no_people:
                available_capacity = available_capacity - no_people
                screen = Screen.query.get(screen_id)
                screen.available_capacity = available_capacity
                db.session.commit()

                new_booking = Booking( movie_id=movie_id, theater_id=theatre_id, screen_id=screen_id, user_id=user_id,
                                num_tickets=no_people, total_amount=amount, booking_time=time, booking_date=date)   

                db.session.add(new_booking)
                db.session.commit()
                return make_response(jsonify({'message': 'Booking Done!!!!!!'}),201)
            
            else:

                return make_response(jsonify({'message': 'Not Enough Seats Available'}),400)
                        
     



