from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(service, event):
    start_time = datetime.datetime.combine(event['date'], datetime.datetime.strptime(event['time'], '%H:%M').time())
    end_time = start_time + datetime.timedelta(hours=1)  # Assume 1-hour duration

    event_body = {
        'summary': f"{event['description']} (Year {event['year']})",
        'description': f"Event for Year {event['year']} students",
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Your_Timezone',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Your_Timezone',
        },
    }

    event = service.events().insert(calendarId='primary', body=event_body).execute()
    print(f"Event created: {event.get('htmlLink')}")

def main():
    service = get_calendar_service()
    schedule = parse_schedule('path_to_your_excel_file.xlsx')  # Use your existing parse_schedule function
    
    for event in schedule:
        create_event(service, event)

if __name__ == '__main__':
    main()