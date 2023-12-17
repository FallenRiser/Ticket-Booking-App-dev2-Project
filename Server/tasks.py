from workers import celery
from celery.schedules import crontab
from flask import render_template
from flask import current_app as app
from jinja2 import Template
import datetime as dt
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from data_access import get_all_users
import smtplib
from models import db, Users, Movie, Booking
from workers import celery
import requests


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
       sender.add_periodic_task(
        5.0, 
        daily_email_reminder.s(), 
        name='add every day'
    )
       sender.add_periodic_task(
        5.0, 
        send_report.s(), 
        name='add every month'
    )   

"""     sender.add_periodic_task(
        5.0, 
        email.s(), 
        name='add every day'
    ) """

 
"""
     sender.add_periodic_task(
        crontab(hour=13, minute=0, day_of_month='1'), 
        send_report.s(), 
        name='add every month'
    ) """


@celery.task()
def hello():
    print('this is a repeating message')
    return 'this is a repeating message'

@celery.task()
def daily_email_reminder():
    with app.app_context():
        print('this is a repeating reminder message')
        requests.post(url='http://127.0.0.1:5000/api/email')
        return 'this is a repeating reminder message'

@celery.task()
def send_report():

    print('this is a report message')
    requests.get(url='http://127.0.0.1:5000/api/monthly-report')
    return 'this is a report message'



