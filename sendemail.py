import sys

import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import string
from string import Template
import codecs

import requests
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime, 

import models
from app import db


def add_one_month(dt0):
    dt2 = dt0 + timedelta(days=31)
    return dt2

def create_message_html(sender, to, subject, msgHtml, msgPlain):
    msgHtml = msgHtml.encode('utf8')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_string())}

def build_message(sender_name, sender_email, recipient_email):
    #build components of message
    subject = Template('Invitation: Meeting @ $date 2:30pm - 3:30pm (CDT) ($sender_name)')
    new_date = add_one_month(datetime.today()).strftime('%a %b %d, %Y')
    subject = subject.safe_substitute(date=new_date, sender_name=sender_name)
    
    #build html calendar invite
    html = Template(codecs.open('templates/email_template.html','r', encoding='utf8').read())
    html = html.safe_substitute(date=new_date, sender_name=sender_name, sender_email=sender_email, recipient_email=recipient_email);

    return create_message_html(sender_email, recipient_email, subject, html, "")

#send calendar invite to target email, from sender
def send_email(sender_name, sender_email, recipient_email, service):
    #build message
    message = build_message(sender_name, sender_email, recipient_email)
    #try sending with service
    try:
        message_response = service.users().messages().send(userId='me', body=message).execute()
        return 'Message Id: %s sent from %s to %s' % (message_response['id'], sender_email, recipient_email)
    except googleapiclient.errors.HttpError, error:
        return 'An error occurred: %s' % error





