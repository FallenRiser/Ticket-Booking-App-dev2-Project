from flask import current_app as app, send_file
from jinja2 import Template
from datetime import date
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from data_access import get_all_users
import smtplib
from models import db, Users, Movie, Booking, Ratings, TheaterTimeSlot, Theatre
from flask import current_app, request, jsonify, Response, make_response
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
import json
from config import WEBHOOK_URL
import requests
from json import dumps
import unicodecsv as csv
from io import StringIO, BytesIO
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request


class export_csv(Resource):
    def get(self,user_id,theatre_id):
        theatre = Theatre.query.get(theatre_id)
        shows = TheaterTimeSlot.query.filter(TheaterTimeSlot.theater_id == theatre_id,TheaterTimeSlot.end_date > date.today()).all()
        bookings = Booking.query.filter_by(theater_id=theatre_id).count()
        print(bookings)
        movie_ids = [show.movie_id for show in shows]
        print(movie_ids)
        movie_titles = []
        for id in movie_ids:
                    movie_titles = Movie.query.filter(Movie.id.in_(movie_ids)).with_entities(Movie.title).all()

        csv_data = BytesIO()
        csv_writer = csv.writer(csv_data, encoding='utf-8')
        csv_writer.writerow(['Theatre Name', 'City', 'Number of Shows', 'Bookings', 'Movie Titles'])
        csv_writer.writerow([theatre.name, theatre.city, len(shows), bookings, ', '.join([title[0] for title in movie_titles])])

        filename = f'{theatre.name}_details.csv'
        with open(filename, 'wb') as csv_file:
            csv_file.write(csv_data.getvalue())

        send_export_alert(theatre_id, filename, user_id)

def send_export_alert(theatre_id, filename, user_id):
    temp_str = template_str = '''
    Dear user,
    <p>
        The Export Job you requested has been successfully completed. Please check your attachments for the export job.
    </p>

    Best regards,
    The TicketShow Team
    '''
    user = Users.query.filter_by(id = user_id).first()
    email = user.email
    with open(filename, 'rb') as attachment:
        attachment_data = attachment.read()

    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "service@TicketShow.com"
    SENDER_PASSWORD = ""
    message = Template(temp_str)
    message = message.render()
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = email
    msg["Subject"] = 'Theatre Export Alert'
    msg.attach(MIMEText(message, "html"))

    if attachment:
        part = MIMEApplication(attachment_data, _subtype="csv")
        part.add_header("Content-Disposition", "attachment", filename= filename)
        msg.attach(part)
    
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

