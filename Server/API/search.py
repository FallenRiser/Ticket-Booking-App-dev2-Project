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


class search(Resource):
    def get(self):
        search_type = request.args.get('type')  
        search_query = request.args.get('q')    

        if search_type == 'movie':
            movies = Movie.query.filter(
                (Movie.title.ilike(f'%{search_query}%')) |
                (Movie.director.ilike(f'%{search_query}%')) |
                (Movie.cast.ilike(f'%{search_query}%'))
            ).all()

            movie_results = [{'id': movie.id, 'title': movie.title, 'director': movie.director, 'cast': movie.cast} for movie in movies]
            return make_response(jsonify(movie_results), 200)

        elif search_type == 'theatre':
           
            theatres = Theatre.query.filter(
                (Theatre.name.ilike(f'%{search_query}%')) |
                (Theatre.city.ilike(f'%{search_query}%')) 
            ).all()

           
            theatre_results = [{'id': theatre.id, 'name': theatre.name, 'city': theatre.city} for theatre in theatres]
            return make_response(jsonify(theatre_results), 200)

        else:
            return make_response(jsonify([]) , 200)