from flask import current_app, request, jsonify, Response, make_response
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
import json
from models import db
from models import Users,Roles,roles_users, Theatre, Movie, Screen, TheaterTimeSlot, Booking, Ratings
from config import UPLOAD_FOLDER
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy import desc 
from datetime import datetime, timedelta, date 
from security import datastore
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from data_access import get_home_movies, get_movies_by_end_date, get_movies_by_title
from config import WEBHOOK_URL
import requests
from json import dumps
from jinja2 import Template

current_date = date.today()


def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions




class movieAPI(Resource):
    @jwt_required()
    def put(self):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)
        print('##########')
        
        data = request.get_json()
        user_id = data.get('user_id')
        movie_id = data.get('movie_id')
        rating_value = data.get('rating')

        print(user_id, movie_id, rating_value)

        usr_rating = Ratings.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if usr_rating:
            usr_rating.rating = rating_value
            db.session.commit()

        else:    
            new_rating = Ratings(user_id=user_id, movie_id=movie_id, rating=rating_value)
            db.session.add(new_rating)
            db.session.commit()

        return {'message': 'Rating added successfully'}, 201




    def get(self):
        print("##############################")
        movies = get_movies_by_end_date(current_date)
        print(movies)

        serialized_movies = []
        for movie in movies:
            serialized_movie = {
                'id': movie.id,
                'title': movie.title,
                'boxart': movie.boxart,
                'director': movie.director,
                'description': movie.description,
                'cast': movie.cast,
                'duration': movie.duration,
                'language': movie.language,
                'rate': movie.rate,
                'genre': movie.genre,
                'start_date': movie.start_date,
                'end_date': movie.end_date,
                'date_added': movie.date_added
            }
            serialized_movies.append(serialized_movie)
        return make_response(jsonify(serialized_movies),200)


    @jwt_required()
    def post(self):
        
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)
        
        current_user_id = get_jwt_identity()
        role_str = request.headers.get('Role')
        role = json.loads(role_str)

        if role != 'admin':
            return make_response(jsonify({"message": "Forbidden access"}), 403)

        #data = request.get_json()

        title = request.form['title']
        #boxart = data.get('boxart')
        director = request.form['director']
        description = request.form['description']
        cast = request.form['cast']
        language = request.form['language']
        duration = request.form['duration']
        rate = request.form['rate']
        genre = request.form['genre']
        startdate = request.form['start_date']
        enddate = request.form['end_date']
        boxart = request.files["boxart"]

        start_date = datetime.strptime(startdate, '%Y-%m-%d').date()
        end_date = datetime.strptime(enddate, '%Y-%m-%d').date()

        if (not title or not duration or not start_date or not end_date or not director or not description
            or not cast or not rate or not genre or not language):
            return make_response(jsonify({'message': 'Invalid input data'}), 400)
        
        check = get_movies_by_title(title)
        print(check)
        if check:
            return {
                'message': 'Movie already exists',
            }, 400

        print(os.path.join(os.getcwd(), UPLOAD_FOLDER))

        if boxart and allowed_file(boxart.filename):
            filename = secure_filename(boxart.filename) + '-' + str(uuid.uuid4())
            boxart.save(os.path.join(UPLOAD_FOLDER, filename))

        movie = Movie(title = title, director = director, boxart = filename, description = description, 
                        cast = cast, rate = rate, genre = genre, language = language, duration = duration,
                        start_date = start_date, end_date = end_date)
        db.session.add(movie)
        db.session.commit() 

        googlespace_msg(title)

        return make_response(jsonify({'message': "Movie Added Successfully"}), 200)   


def googlespace_msg(title):
    msg = Template("🎟️ Hello TicketShow Users! 🎟️ We just now added a new movie {{ title }}!! Make sure to visit our website and book your tickets for today's showtimes. 🎬🍿 Visit us at: 'http://localhost:8080/' See you at the movies! 🎥🎞️ Best regards, The TicketShow Team")
    render_msg = msg.render(title = title)

    url = WEBHOOK_URL
    app_message = {'text': render_msg}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    requests.post(url, headers=message_headers, data = dumps(app_message))


class MovieHome(Resource):

    
    def post(self):
        today = datetime.now().date()
        latest_movies = get_home_movies()
        print(latest_movies)
        home_movies = []
        for movie in latest_movies:
            home_movie = {
                'id': movie.id,
                'title': movie.title,
                'boxart': movie.boxart,
                'director': movie.director,
                'description': movie.description,
                'cast': movie.cast,
                'duration': movie.duration,
                'language': movie.language,
                'rate': movie.rate,
                'genre': movie.genre,
                'start_date': movie.start_date,
                'end_date': movie.end_date,
                'date_added': movie.date_added
            }
            home_movies.append(home_movie)
        print(home_movies)
        return make_response(jsonify(home_movies),200)  

    def get(self,movie_id):
        print(movie_id)
        movie = Movie.query.get(movie_id)
        print(movie)
        rtng = Ratings.query.filter_by(movie_id = movie_id).all()

        r_avg = 0
        count = 0
        for r in rtng:
            r_avg += r.rating  
            count += 1 

        if r_avg > 0:
            rating = r_avg / count
        else:
            rating = 0    
        print('rating',rating)

        serialized_movie = {
            'id': movie.id,
            'title': movie.title,
            'boxart': movie.boxart,
            'director': movie.director,
            'description': movie.description,
            'cast': movie.cast,
            'duration': movie.duration,
            'language': movie.language,
            'rate': movie.rate,
            'genre': movie.genre,
            'start_date': movie.start_date,
            'end_date': movie.end_date,
            'date_added': movie.date_added,
            'rating': rating
        }
        return make_response(jsonify(serialized_movie),200)
    
    @jwt_required()
    def put(self,movie_id):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)
        
        current_user_id = get_jwt_identity()
        role_str = request.headers.get('Role')
        role = json.loads(role_str)

        if role != 'admin':
            return make_response(jsonify({"message": "Forbidden access"}), 403)

        movie = Movie.query.get(movie_id)

        if not movie:
            return make_response(jsonify({"message": "Movie not found"}), 404)
 
        format_string = '%B %d, %Y'

        title = request.form['title']
        #boxart = data.get('boxart')
        director = request.form['director']
        description = request.form['description']
        cast = request.form['cast']
        language = request.form['language']
        duration = request.form['duration']
        rate = request.form['rate']
        genre = request.form['genre']
        startdate = request.form['start_date']
        enddate = request.form['end_date']
        boxart = request.files.get('boxart')
        print('boxart',boxart)

        parsed_startdate = datetime.strptime(startdate, format_string)
        parsed_enddate = datetime.strptime(enddate, format_string)

        start__date = parsed_startdate.strftime('%Y-%m-%d')
        end__date = parsed_enddate.strftime('%Y-%m-%d')

        if start__date is not None:
            start_date = datetime.strptime(start__date, '%Y-%m-%d').date()
        else:
            start_date = movie.start_date

        if end__date is not None:
            end_date = datetime.strptime(end__date, '%Y-%m-%d').date()
        else:
            end_date = movie.end_date

        if (not title or not duration or not start_date or not end_date or not director or not description
                or not cast or not rate or not genre or not language):
            return make_response(jsonify({'message': 'Invalid input data'}), 400)


        check = Movie.query.filter_by(title=title).first()
        if check and check.id != movie_id:
            return {
                'message': 'Movie already exists',
            }, 400

        
        if boxart and allowed_file(boxart.filename):
            filename = secure_filename(boxart.filename) + '-' + str(uuid.uuid4())
            boxart.save(os.path.join(UPLOAD_FOLDER, filename))
            movie.boxart = filename  
        
        movie.title = title
        print(movie.title)
        movie.director = director
        movie.description = description
        movie.cast = cast
        movie.language = language
        movie.duration = duration
        movie.rate = rate
        movie.genre = genre
        movie.start_date = start_date
        movie.end_date = end_date
        print('#')
        db.session.commit()

        return make_response(jsonify({"message": "Movie updated successfully"}), 200)
    

    @jwt_required()
    def delete(self, movie_id):
        if not verify_jwt_in_request():
            return make_response(jsonify({"message": "Invalid Token"}), 401)

        current_user_id = get_jwt_identity()
        role_str = request.headers.get('Role')
        role = json.loads(role_str)

        if role != 'admin':
            return make_response(jsonify({"message": "Forbidden access"}), 403)


        movie = Movie.query.get(movie_id)

        if not movie:
            return make_response(jsonify({"message": "Movie not found"}), 404)

        try:
            TheaterTimeSlot.query.filter_by(movie_id=movie_id).delete()
            Booking.query.filter_by(movie_id=movie_id).delete()
            Ratings.query.filter_by(movie_id=movie_id).delete()

            db.session.delete(movie)
            db.session.commit()

            return make_response(jsonify({"message": "Movie deleted successfully"}), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': f'Error deleting movie: {str(e)}'}), 500)



        

  
