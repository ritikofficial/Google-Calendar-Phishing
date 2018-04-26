import google_api
import os
import oauth2client
from oauth2client import client, tools
import httplib2

import sys

import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from collections import defaultdict
import datetime
import base64
import webbrowser
import requests

# /api/password
# name
# email

def create_headers_dict(message):
    # transform headers into dict rather than list to make it easier to work with
    headers_dict = {}
    for header in message['payload']['headers']:
        headers_dict[header['name']] = header['value']

    return headers_dict

def find_reset_links(messages):
    """get db from database not service, cant use subject anymore"""
    links = []
    for message in messages:
        headers_dict = create_headers_dict(message)    
        if 'reset' in headers_dict['Subject']:
            body64 = message['payload']['body']['data']
            print body64
            msg = base64.b64decode(body64).split()
            # look for links
            for s in msg:
                if 'http' in s:
                    links.append(s)

    return links

def request_resets(email):
    uname = email.split('@')[0]
    r = requests.post("https://www.reddit.com/api/password", data={'name': uname, 'email': email})
    print r
    print r.content

def open_reset_links(service, email):
    # request_resets(email)
    
    links = []
    while True:
        messages = google_api.get_messages(service) 
        links = find_reset_links(messages)
        if len(links) > 0:
            break
        sleep(20)

    print links
    # for link in links:
        # webbrowser.open(link)

if __name__ == '__main__':
    home_dir = os.path.expanduser('~')
    credential_path = os.path.join(home_dir, '.credentials', 'credential-calendarphishingtest123.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    http = credentials.authorize(httplib2.Http())

    gmail_service = discovery.build('gmail', 'v1', http=http)

    open_reset_links(gmail_service, 'contactthree003@gmail.com')
