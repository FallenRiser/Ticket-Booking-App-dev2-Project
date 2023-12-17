from flask import current_app as app
from jinja2 import Template
from datetime import date
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from data_access import get_all_users
import smtplib
from models import db, Users, Movie, Booking
from flask import current_app, request, jsonify, Response, make_response
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
import json
from config import WEBHOOK_URL
import requests
from json import dumps
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request


class email(Resource):
    def post(self):
        ans = reminder_email()
        ans2 = google_chat()

def google_chat():
    url = WEBHOOK_URL
    app_message = {
        'text': "🎟️ Hello TicketShow Users! 🎟️ Don't miss out on the latest movies and exciting shows! Make sure to visit our website and book your tickets for today's showtimes. 🎬🍿 Visit us at: 'http://localhost:8080/' See you at the movies! 🎥🎞️ Best regards, The TicketShow Team"}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    requests.post(url, headers=message_headers, data = dumps(app_message,))

def reminder_email():
    template_str = '''
    Dear {{user}},
    <p>
    We hope this message finds you well and excited for a cinematic experience! At TicketShow, we're dedicated to bringing you the best entertainment options, and we wouldn't want you to miss out on the latest shows and movies.
    </p>
    <p><strong>
    🎥 Movie Magic Awaits! 🎥
    </strong></p>
    <p>
    From heartwarming comedies to thrilling action-packed adventures, we have a diverse range of movies waiting for you. Make your movie night unforgettable by booking your tickets today. Whether you're planning a solo escapade or a fun family outing, we have something for everyone.
    </p>
    <p><strong>
    🌟 Your Movie Experience Matters 🌟
    </strong></p>
    <p>
    By booking your tickets with TicketShow, you not only treat yourself to an amazing movie experience but also support local theaters and the film industry. Your love for cinema helps us bring more exciting content to the big screen.
    </p>
    <p>
    👉 Book Now: <a href='http://localhost:8080/'><button class="btn btn-danger">Book Now</button></a>
    </p>
    Hurry, seats are filling up fast! Don't miss the chance to immerse yourself in the magic of movies. We can't wait to see you at the theater.

    Best regards,
    The TicketShow Team
    '''
        
    users = get_all_users()
    template = Template(template_str)

    for user in users:
        if user.email_preference == True:
            today = date.today()
            user_bookings_today = Booking.query.filter_by(user_id=user.id, entry_date=today).all()
            if not user_bookings_today:

                address = user.email
                subject = user.username + ", a friendly reminder to contribute to TicketShow"
                rendered_template = template.render(user=user.username)

                send_email(address, subject, rendered_template)


    return 200


def send_email(address, subject, message, attachment=None, images=None, filename=None, subtype=None):
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "service@TicketShow.com"
    SENDER_PASSWORD = ""

    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = address
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))

    if attachment:
        part = MIMEApplication(attachment.read(), _subtype=subtype)
        part.add_header("Content-Disposition", "attachment", filename= filename)
        msg.attach(part)
    
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()