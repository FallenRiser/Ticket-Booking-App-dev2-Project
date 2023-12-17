from flask import current_app, request, jsonify, make_response
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
import json
from models import db
from models import Users,Roles,roles_users, Theatre, Movie, Screen, TheaterTimeSlot
from API.validation import UserError, PropertyExistError, TheatreError
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime, timedelta
from security import datastore
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request
from sqlalchemy import and_, or_, not_
from data_access import get_timeslot_by_theatreid_enddate, get_movies_by_movie_id, get_timeslot_by_movieid, get_timeslot_by_id

def is_screen_booked(screen, start_date, end_date, start_time, end_time):
    for timeslot in screen.time_slots:
        if (timeslot.start_date <= start_date <= timeslot.end_date or
            timeslot.start_date <= end_date <= timeslot.end_date or
            (start_date < timeslot.start_date and end_date > timeslot.end_date) or
            (start_date == timeslot.start_date and end_date == timeslot.end_date)):
            if (timeslot.start_time <= start_time <= timeslot.end_time or
                timeslot.start_time <= end_time <= timeslot.end_time or
                (start_time < timeslot.start_time and end_time > timeslot.end_time) or
                (start_time == timeslot.start_time and end_time == timeslot.end_time)):
                return True

    return False

class moviefromtheatre(Resource):
    def get(self, theatre_id):
        data_list = []
        time_slots = get_timeslot_by_theatreid_enddate(theatre_id)
        print(time_slots)
        for time_slot in time_slots:
            movie_info = get_movies_by_movie_id(time_slot.movie_id)
            data = {
                'movie_id': movie_info.id,
                'title': movie_info.title,
                'director': movie_info.director,
                'description': movie_info.description,
                'cast': movie_info.cast,
                'duration': movie_info.duration,
                'language': movie_info.language,
                'rate': movie_info.rate,
                'genre': movie_info.genre,
                'start_date': movie_info.start_date,
                'end_date': movie_info.end_date,
                'screen_id': time_slot.screen_id,
                'start_time': time_slot.start_time.strftime('%H:%M'),
                'end_time': time_slot.end_time.strftime('%H:%M'),
            }
            data_list.append(data)

        return make_response(jsonify(data_list), 200) 

class movie_timings(Resource):
    @jwt_required()
    def get(self,movie_id):

        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)
    
        current_user_id = get_jwt_identity()
        role_str = request.headers.get('Role')
        role = json.loads(role_str)
        print(movie_id)
        if role != 'admin':
            return make_response(jsonify({"message": "Forbidden access"}), 403)
        movie = Movie.query.get(movie_id)
        if not movie:
            return make_response(jsonify({"message": "Movie not found"}), 404)
        
        time_slots = get_timeslot_by_movieid(movie_id)
        
        timings_data = []
        for slot in time_slots:
            theatre = Theatre.query.get(slot.theater_id)
            screen = Screen.query.get(slot.screen_id)
            
            timings_data.append({
                'id': slot.id,
                'theatre': theatre.name,
                'screen_no': screen.number,
                'start_date': slot.start_date.strftime('%Y-%m-%d'),
                'end_date': slot.end_date.strftime('%Y-%m-%d'),
                'start_time': slot.start_time.strftime('%H:%M'),
                'end_time': slot.end_time.strftime('%H:%M'),
            })
        
        return make_response(jsonify(timings_data),200)



    @jwt_required()
    def post(self):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)
        
        current_user_id = get_jwt_identity()
        role_str = request.headers.get('Role')
        role = json.loads(role_str)

        if role != 'admin':
            return make_response(jsonify({"message": "Forbidden access"}), 403)
        
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        start_time_str = request.form['start_time']
        end_time_str = request.form['end_time']

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()


        theaters_and_screens = Theatre.query.join(Screen).outerjoin(TheaterTimeSlot, and_(
                                TheaterTimeSlot.theater_id == Theatre.id,
                                TheaterTimeSlot.screen_id == Screen.id,
                                or_(
                                and_(
                                TheaterTimeSlot.start_date <= start_date,
                                TheaterTimeSlot.end_date >= end_date,
                                TheaterTimeSlot.start_time <= end_time,
                                TheaterTimeSlot.end_time >= start_time
                                ),
                                TheaterTimeSlot.id.is_(None)
                                )
                                )).filter(
                                not_(TheaterTimeSlot.id.isnot(None))
                                ).all()

        print(theaters_and_screens)
        theater_list = []
        for theatre in theaters_and_screens:
            available_screens = [screen for screen in theatre.screens if not is_screen_booked(screen, start_date, end_date, start_time, end_time)]
            screens_data = []
            for screen in available_screens:
                screen_data = {
                    'id': screen.id,
                    'number': screen.number,
                    'technology': screen.technology,
                    'seat_capacity': screen.seat_capacity,
                    'premium': screen.premium
                    }
                screens_data.append(screen_data)

            theater_data = {
                'id': theatre.id,
                'name': theatre.name,
                'city': theatre.city,
                'screens': screens_data
                }
            theater_list.append(theater_data)
        print(theater_list)

        return make_response(jsonify(theater_list))





class AddTimeSlot(Resource):
       

    @jwt_required()
    def delete(self, slot_id):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)
    
        current_user_id = get_jwt_identity()
        role_str = request.headers.get('Role')
        role = json.loads(role_str)
        if role != 'admin':
            return make_response(jsonify({"message": "Forbidden access"}), 403)

        timeslot = TheaterTimeSlot.query.filter_by(id=slot_id).first()
        print(timeslot)
        db.session.delete(timeslot)
        db.session.commit()
        return make_response(jsonify({"message": "Timing deleted successfully"}), 200)

    @jwt_required()
    def put(self, slot_id):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)
    
        current_user_id = get_jwt_identity()
        role_str = request.headers.get('Role')
        role = json.loads(role_str)
        if role != 'admin':
            return make_response(jsonify({"message": "Forbidden access"}), 403)
        print('in here!!')
        data = request.get_json()
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')
        print(start_time_str)

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()


        timeslot = get_timeslot_by_id(slot_id)

        print(timeslot)
        timeslot.start_date = start_date
        timeslot.end_date = end_date
        timeslot.start_time = start_time
        timeslot.end_time = end_time

        db.session.commit()
        return make_response(jsonify({"message": "Timing updated successfully"}), 200)

    @jwt_required()
    def post(self):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)
        
        current_user_id = get_jwt_identity()
        role_str = request.headers.get('Role')
        role = json.loads(role_str)

        if role != 'admin':
            return make_response(jsonify({"message": "Forbidden access"}), 403)


        try:
            data = request.get_json()
            movie_id = data.get('movieID')
            start_date_str = data.get('start_date')
            end_date_str = data.get('end_date')
            start_time_str = data.get('start_time')
            end_time_str = data.get('end_time')
            theater_screen_dict = data.get('theater_screen_dict')

            print(theater_screen_dict)
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()

            for theater_id in theater_screen_dict.keys():
                screen_ids = theater_screen_dict[theater_id]
                print("screen ids",screen_ids)
                for screen_id in screen_ids:
                    mov = TheaterTimeSlot.query.filter_by(start_date=start_date, end_date=end_date, start_time = start_time, end_time = end_time, theater_id = theater_id, screen_id = screen_id ).first()
                    if mov:
                        return make_response(jsonify({'message': 'Data cannot be inserted as one of the timeslots is already occupied for the timeframe'}),200)
                    else:
                        timing = TheaterTimeSlot(
                            theater_id=theater_id,
                            screen_id=screen_id,
                            movie_id=movie_id,
                            start_date=start_date,
                            end_date=end_date,
                            start_time=start_time,
                            end_time=end_time,
                        )
                        print(timing)
                        db.session.add(timing)
                        db.session.commit()
            return make_response(jsonify({"message": "Timings added successfully"}), 201)
        except Exception as e:
            pass
            return make_response(jsonify({"error": "Failed to add timings"}), 500)
    



