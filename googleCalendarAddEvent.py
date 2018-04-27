
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='9eg8v70ea9nmondpdua3ppicrs@group.calendar.google.com',
                                      maxResults=100, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

#
if not events:
    print('No upcoming events found.')
for event in events:
    print('*'*100)
    service.events().delete(calendarId='9eg8v70ea9nmondpdua3ppicrs@group.calendar.google.com', eventId=event['id']).execute()
    #start = event['start'].get('dateTime', event['start'].get('date'))
    #print(start, event['summary'])
