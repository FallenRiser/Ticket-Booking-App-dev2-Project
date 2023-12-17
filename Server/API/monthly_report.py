""" from flask import current_app, request, jsonify, make_response, render_template
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
import json
from models import db
from models import Users,Roles,roles_users, Theatre, Movie, Screen, TheaterTimeSlot, Booking, Ratings
from API.validation import UserError, PropertyExistError, TheatreError
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import timedelta
import datetime as datetime
from security import datastore
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request
from sqlalchemy import and_, or_, not_
import matplotlib.pyplot as plt
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart,MIMEBase 
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from email.mime.application import MIMEApplication
from weasyprint import HTML
from jinja2 import Template
import base64


class MonthlyReport(Resource):

    def generate_theatre_spending_graph(self, bookings_data):
        print(bookings_data)
        bookings_df = pd.DataFrame(bookings_data)
        print(bookings_df)
        theatre_spending = bookings_df.groupby("theatre_name")["amount"].sum()

        plt.figure(figsize=(10, 6))
        theatre_spending.plot(kind="bar")
        plt.title("Monthly Theatre Spending")
        plt.xlabel("Theatre")
        plt.ylabel("Amount Spent")
        plt.tight_layout()

        graph_image_path = "/mnt/c/users/sheth/Desktop/MAD2proj/Server/static/theatre_spending_graph.png"
        plt.savefig(graph_image_path)
        plt.close()

        with open(graph_image_path, "rb") as image_file:
            base64_image_data = base64.b64encode(image_file.read()).decode("utf-8")

        return graph_image_path, base64_image_data

    def generate_report_and_email(self, user_report):
        
        user = user_report
        print(user)

        graph_image_path, base64_image_data = self.generate_theatre_spending_graph(user['bookings'])
        email = user['user_email']

        template_str = <!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Monthly Entertainment Review - Cover Page</title>
<style>
table, th, td {
        border: 1px solid black;
        font-size: 14px; padding: 5px; border-collapse: collapse;
      }
body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
}
.cover-container {
    text-align: center;
    padding: 0px 0;
}
h1 {
    color: #333;
    font-size: 28px;
}
p {
    color: #777;
    font-size: 18px;
}

.summary-container {
    max-width: 1300px;
    margin: 0;
    padding: 0px;
    }

    h2 {
    color: #555;
    font-size: 20px;
    }

    img.graph {
    max-width: 100%;
    height: auto;
    }
</style>
</head>
<body>
<div class="cover-container">
<h1>Monthly Entertainment Review</h1>
<p>Ticket Show</p>
</div>
<div class="summary-container">
<h1>Monthly Entertainment Review</h1>
<h2>Hello, {{ user.user_name }}!</h2>

<h2>User Information</h2>
<p>Date Joined: {{ user.date_joined }}</p>

<h2>Tickets Booked This Month</h2>
<p>Total Tickets: {{ user.total_tickets_bought }}</p>

<h2>Theatres Mostly Visited This Month</h2>
{% for theatre in user.most_visited_theatre %}
<p>{{ theatre }}</p>
{% endfor %}

<h2>Max Spent on one day</h2>
<p>{{ user.max_spent }} ₹</p>

<h2>Monthly Bookings</h2>
<table>
    <tr>
    <th>Movie Date</th>
    <th>Movie Name</th>
    <th>Movie Time</th>
    <th>Theatre Name</th>
    <th>Screen Number</th>
    <th>Your Rating</th>
    <th>Tickets</th>
    <th>Amount Spent</th>
    </tr>
    {% for booking in user.bookings %}
    <tr>
    <td>{{ booking.movie_date }}</td>
    <td>{{ booking.movie_title }}</td>
    <td>{{ booking.movie_time }}</td>
    <td>{{ booking.theatre_name }} - {{ booking.theatre_city }}</td>
    <td>{{ booking.screen_number }} - {{ booking.screen_tech }}</td>
    <td>{{ booking.rating }}</td>
    <td>{{ booking.tickets_bought }}</td>
    <td>{{ booking.amount }} ₹</td>
    </tr>
    {% endfor %}
</table>

<h2>Total Money Spent on Theatres</h2>
<img class="graph" src='data:image/png;base64,{{ base64_image_data }}' alt="Theatre Spending Graph">
</div>
</body>
</html>

        template = Template(template_str)

        pdf_report_path = "/mnt/c/users/sheth/Desktop/MAD2proj/Server/static/monthly_report.pdf"
        report_html = render_template(template,base64_image_data=base64_image_data ,user=user)
        HTML(string=report_html).write_pdf(pdf_report_path)

        SMTP_SERVER_HOST = "localhost"
        SMTP_SERVER_PORT = 1025
        SENDER_ADDRESS = "service@TicketShow.com"
        SENDER_PASSWORD = ""

        msg = MIMEMultipart()
        msg["From"] = SENDER_ADDRESS
        msg["To"] = email
        msg["Subject"] = "Monthly Entertainment Report"


        with open(pdf_report_path, "rb") as pdf_file:
            pdf_attachment = MIMEApplication(pdf_file.read(), name="monthly_report.pdf")
            pdf_attachment['Content-Disposition'] = f'attachment; filename="{pdf_report_path}"'
            msg.attach(pdf_attachment)

        html_part = MIMEText(report_html, "html")
        msg.attach(html_part)    

        with open(graph_image_path, "rb") as image_file:
            graph_image = MIMEImage(image_file.read(), name="theatre_spending_graph.png")
            graph_image.add_header('Content-Disposition', 'attachment', filename='theatre_spending_graph.png')
            msg.attach(graph_image)

   
        s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
        s.login(SENDER_ADDRESS, SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()

        return "Report generated and emailed successfully!"

    def get(self):
        report_data = get_report_data()

        for user_report in report_data:
            self.generate_report_and_email(user_report)

        return "Reports generated and emailed successfully!"


def get_report_data():
        today = datetime.date.today()
        one_month_ago = today - timedelta(days=30)
        users = Users.query.all()

        report_data = []
        

        for user in users:
            amount_spent = 0
            total_tickets_bought = 0
            booking_list = []
            bookings = Booking.query.filter(Booking.user_id == user.id, Booking.booking_date >= one_month_ago, Booking.booking_date <=today ).all()

            most_visited_theatre ={}
            max_spent = 0

            for book in bookings:
                amount_spent += book.total_amount
                if book.total_amount > max_spent:
                    max_spent = book.total_amount

                total_tickets_bought += book.num_tickets
                booking_time = book.booking_time
                booking_date = book.booking_date

                movie = Movie.query.filter(Movie.id == book.movie_id).first()

                title = movie.title
                duration = movie.duration
                language = movie.language

                theatre = book.theater_id
                screen = book.screen_id

                theatre_qur = Theatre.query.filter_by(id = theatre).first()

                theatre_name = theatre_qur.name
                theatre_city = theatre_qur.city

                if theatre_name in most_visited_theatre:
                    most_visited_theatre[theatre_name] += 1
                else:
                    most_visited_theatre[theatre_name] = 1

                screen_qur = Screen.query.filter_by(id = screen).first()

                screen_no = screen_qur.number
                screen_tech = screen_qur.technology

                ratng = Ratings.query.filter_by(user_id = user.id, movie_id = movie.id).first()
                if not ratng:
                    rating = 0
                else:    
                    rating = ratng.rating

                data = {
                    'theatre_name': theatre_name,
                    'theatre_city': theatre_city,
                    'screen_number': screen_no,
                    'screen_tech': screen_tech,
                    'movie_title': title,
                    'movie_duration': duration,
                    'movie_language': language,
                    'rating': rating,
                    'tickets_bought': book.num_tickets,
                    'movie_time': booking_time,
                    'movie_date': booking_date,
                    'amount': book.total_amount,
                }

                booking_list.append(data)

            most_visit_theatres = [key for key, value in most_visited_theatre.items() if value == max(most_visited_theatre.values())]


            user_report = {
                'user_id': user.id,
                'user_name': user.username,
                'user_email': user.email,
                'date_joined': user.date_joined,
                'total_spent': amount_spent,
                'total_tickets_bought': total_tickets_bought,
                'bookings': booking_list,
                'most_visited_theatre': most_visit_theatres,
                'max_spent': max_spent,
            }

            report_data.append(user_report)
        return report_data

 """