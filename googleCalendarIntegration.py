from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import parser

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    
    # Check if token.json exists (this stores user's access and refresh tokens)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the credentials using the refresh token
            creds.refresh(Request())
        else:
            # If no valid credentials, we prompt the user to log in and get new credentials
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  # Use the credentials.json file from Google Cloud
            creds = flow.run_local_server(port=8080)
        
        # Save the credentials for future use to avoid re-authentication every time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Calendar API service
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(service, event):
    # Create a datetime object for the event start and end times
    start_time = event['date'].replace(hour=18)

    
    end_time = start_time + datetime.timedelta(hours=1)  # Assume the event lasts 1 hour

    # Create the event body to send to Google Calendar API
    event_body = {
        'summary': f"{event['description']} (Year {event['studentYear']})",
        'description': f"Event for Year {event['studentYear']} students",
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Europe/Lisbon',  # Set your time zone here
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Europe/Lisbon',
        },
    }

    # Insert the event into the user's primary calendar
    event = service.events().insert(calendarId='primary', body=event_body).execute()
    print(f"Event created: {event.get('htmlLink')}")

def main():
    # Get the authenticated calendar service
    service = get_calendar_service()
    
    # Assuming `parser.getScheduleByStudentYear(1)` returns a list of events in the following format:
    # {'description': 'Event Name', 'year': 1, 'date': <datetime.date object>, 'time': '14:00'}
    schedule = parser.getScheduleByStudentYear(2)  # Replace this with your actual parser function
    
    # Iterate through the schedule and create each event in Google Calendar
    for event in schedule:
        create_event(service, event)

if __name__ == '__main__':
    main()
