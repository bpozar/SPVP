# -*- coding: utf-8 -*-

from datetime import datetime
import os

from apiclient.discovery import build
from httplib2 import Http
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

def initialize():
    credentials = get_credentials()
    service = build('calendar', 'v3', http=credentials.authorize(Http()))

    return credentials, service

def example_event():
    event = {
      'summary': 'Tomo event 15',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': '2015-06-21T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2015-06-28T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
      'attendees': [
        {'email': 'lpage@example.com'},
        {'email': 'sbrin@example.com'},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'sms', 'minutes': 10},
        ],
      },
    }

    return event

def event_put(event, calendar_name, service):
    return service.events().insert(calendarId=calendar_name, body=event).execute()

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials, service = initialize()

    json_event = example_event()

    event = event_put(json_event, 'primary', service) 
    #service.events().insert(calendarId='primary', body=event).execute()
    print 'Event created: %s' % (event.get('htmlLink'))

    #now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print 'Getting the upcoming 10 events'
    #eventsResult = service.events().list(
    #    calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
    #    orderBy='startTime').execute()
    #events = eventsResult.get('items', [])

    #if not events:
    #    print 'No upcoming events found.'
    #for event in events:
    #    start = event['start'].get('dateTime', event['start'].get('date'))
    #    print start, event['summary'].encode('utf-8')


if __name__ == '__main__':
    main()