from flask import current_app, request, jsonify, make_response
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
import json
from models import db
from models import Users,Roles,roles_users, Theatre, Movie, Screen, TheaterTimeSlot, Booking
from API.validation import UserError, PropertyExistError, TheatreError
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime, timedelta
from security import datastore
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request
from data_access import get_theatre_orderby_city, get_theatre_by_id, TimeSlots_by_screenid, get_screens_by_screenid


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('city')
parser.add_argument('screens')
parser.add_argument('number')
parser.add_argument('technology')
parser.add_argument('seat_capacity')
parser.add_argument('premium')

class theatreAPI(Resource):

    def get(self):
        print("###########IN GET ############")
        theatres = get_theatre_orderby_city()
        print(theatres)
        theatre_list = []
        for theatre in theatres:
            screens_data = []
            for screen in theatre.screens:
                screen_data = {
                    'id': screen.id,
                    'number': screen.number,
                    'technology': screen.technology,
                    'seat_capacity': screen.seat_capacity,
                    'premium': screen.premium
                }
                screens_data.append(screen_data)

            theatre_data = {
                'id': theatre.id,
                'name': theatre.name,
                'city': theatre.city,
                'screens': screens_data
            }
            theatre_list.append(theatre_data)
            print(theatre_list)

        return make_response(jsonify(theatre_list),200)

   
    @jwt_required()
    def post(self):
        try:
            if not verify_jwt_in_request():
                return make_response(jsonify({"message": "Invalid Token"}), 401)

            current_user_id = get_jwt_identity()
            role_str = request.headers.get('Role')
            role = json.loads(role_str)
            
            if role != 'admin':
                return make_response(jsonify({"message": "Forbidden access"}), 403) 
            
            print(role)
            data = request.get_json()
            theatre_name = data.get('name')
            city = data.get('city')
            screens = data.get('screens', [])
            print(theatre_name,city,screens)
            if not theatre_name or not city:
                return make_response(jsonify({"message": "Theatre name and city are required fields"}), 400)

            if Theatre.query.filter_by(name=theatre_name, city=city).first():
                print('already exist error')
                return make_response(jsonify({"message": "Theatre already exists"}), 400)

            theatre = Theatre(name=theatre_name, city=city)
            db.session.add(theatre)
            db.session.commit()

            for screen_data in screens:
                screen_number = screen_data.get('screenNumber')
                technology = screen_data.get('technology')
                seat_capacity = screen_data.get('seatCapacity')
                available_capacity = screen_data.get('seatCapacity')
                premium = screen_data.get('premium')

                if not screen_number or not technology or not seat_capacity:
                    return make_response(jsonify({"message": "Screen number, technology, and seat capacity are required fields"}), 400)

                screen = Screen(number=screen_number, technology=technology, seat_capacity=seat_capacity, available_capacity = available_capacity, premium=premium, theatre_id=theatre.id)
                db.session.add(screen)

            db.session.commit()

            return make_response(jsonify({"message": "Theatre created successfully"}), 201)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': f'Error adding theater: {str(e)}'}), 500)
        

class editTheatre(Resource):
    def get(self,theatre_id):
        print("###########IN GET ############")
                 
        theatre_id = theatre_id
        theatres = Theatre.query.filter_by(id = theatre_id).first()
        print(theatres)
        theatre_list = []
        
        screens_data = []
        for screen in theatres.screens:
            screen_data = {
                'id': screen.id,
                'number': screen.number,
                'technology': screen.technology,
                'seat_capacity': screen.seat_capacity,
                'available_capacity': screen.available_capacity,
                'premium': screen.premium
            }
            screens_data.append(screen_data)

        theatre_data = {
            'id': theatres.id,
            'name': theatres.name,
            'city': theatres.city,
            'screens': screens_data
        }
        theatre_list.append(theatre_data)
        print(theatre_list)

        return make_response(jsonify(theatre_data),200)
    
    @jwt_required()
    def put(self, theatre_id):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        current_user_id = get_jwt_identity()
        role_str = request.headers.get('Role')
        role = json.loads(role_str)

        if role != 'admin':
            return make_response(jsonify({"message": "Forbidden access"}), 403)

        theatre = get_theatre_by_id(theatre_id)
        if not theatre:
            return make_response(jsonify({"message": "Theatre not found"}), 404)

        data = request.get_json()
        theatre_name = data.get('name', theatre.name)
        theatreid = data.get('id')
        city = data.get('city', theatre.city)
        screens = data.get('screens', [])
        theatre.name = theatre_name
        theatre.city = city
        originalscreens = Screen.query.filter_by(theatre_id=theatreid).all()

        for scr in originalscreens:
            if str(scr.id) not in [str(screen_data.get('screenid')) for screen_data in screens if 'screenid' in screen_data]:
                theatre_time_slots = TimeSlots_by_screenid(scr.id)
                if theatre_time_slots is not None:
                    for time_slot in theatre_time_slots:
                        db.session.delete(time_slot)

                booking_rem = Booking.query.filter_by(screen_id=scr.id).all()
                if booking_rem is not None:
                    for entry in booking_rem:
                        db.session.delete(entry)

                db.session.delete(scr)

        for screen_data in screens:
            screen_id = screen_data.get('screenid')
            screen_number = screen_data.get('screenNumber')
            technology = screen_data.get('technology')
            seat_capacity = screen_data.get('seatCapacity')
            available_capacity = screen_data.get('availableCapacity')
            premium = screen_data.get('premium')

            if screen_id:
                screen = get_screens_by_screenid(screen_id)
                if screen:
                    screen.number = screen_number
                    screen.technology = technology
                    screen.seat_capacity = seat_capacity
                    screen.available_capacity = available_capacity
                    screen.premium = premium
                else:
                    return make_response(jsonify({"message": "Screen not found"}), 404)
            else:
                screen = Screen(number=screen_number, technology=technology, seat_capacity=seat_capacity,
                                available_capacity=available_capacity, premium=premium, theatre_id=theatre.id)
                db.session.add(screen)

        db.session.commit()

        return make_response(jsonify({"message": "Theatre updated successfully"}), 200)


    def delete(self, theatre_id):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        current_user_id = get_jwt_identity()
        role_str = request.headers.get('Role')
        role = json.loads(role_str)

        if role != 'admin':
            return make_response(jsonify({"message": "Forbidden access"}), 403)

        try:
            theatre = Theatre.query.get(theatre_id)

            if not theatre:
                return make_response(jsonify({"message": "Theater not found"}), 404)

            screen_ids = [screen.id for screen in theatre.screens]
            Booking.query.filter(Booking.screen_id.in_(screen_ids)).delete()
            TheaterTimeSlot.query.filter(TheaterTimeSlot.screen_id.in_(screen_ids)).delete()

            for screen in theatre.screens:
                db.session.delete(screen)

            db.session.delete(theatre)
            db.session.commit()

            return make_response(jsonify({"message": "Theater, associated screens, bookings, and time slots deleted successfully"}), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': f'Error deleting theater: {str(e)}'}), 500)
 


import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class TheatreStatistics(Resource):
    def get(self, theatre_id):
        enddate = datetime.now()
        end_date = enddate.strftime('%Y-%m-%d')                                  
        startdate = enddate - timedelta(days=7)
        start_date = startdate.strftime('%Y-%m-%d')

        print('startdate enddate', start_date,end_date)
        tickets = Booking.query.filter(
                     Booking.theater_id == theatre_id,
                     Booking.booking_date >= start_date,
                     Booking.booking_date <= end_date
        ).all()
        print(tickets)

        num_tickets_col = []
        for ticket in tickets:
            num_tickets_col.append((ticket.booking_date, ticket.num_tickets))
        
        total_tickets_sold = {row[0]: row[1] for row in num_tickets_col}

        date_ticket_counts = {}

        for ticket in tickets:
            if ticket.booking_date in date_ticket_counts:
                date_ticket_counts[ticket.booking_date] += ticket.num_tickets
            else:
                date_ticket_counts[ticket.booking_date] = ticket.num_tickets

        
        dates = [datetime.today().date() - timedelta(days=x) for x in range(7)]
        ticket_counts = [date_ticket_counts.get(date, 0) for date in dates]
        print('ticket counts',ticket_counts)

        plt.figure(figsize=(10, 6))
        plt.plot(dates, ticket_counts, marker='o')

        plt.xlabel('Date')
        plt.ylabel('Total Tickets Sold')
        plt.title('Total Tickets Sold Over the Last Week')

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))


        plt.gcf().autofmt_xdate()

        plt.grid(True)
        plt.tight_layout()
        graph_image_path = "/mnt/c/users/sheth/Desktop/MAD2proj/Server/static/statistics.png"
        plt.savefig(graph_image_path)
        plt.close()

        return {"total_tickets_sold": ticket_counts, "graph_image_path": graph_image_path}






