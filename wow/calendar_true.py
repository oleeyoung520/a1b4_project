from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class calendar_google:

    def __init__(self, SCOPES = ['https://www.googleapis.com/auth/calendar']):
        self.creds = None
        self.SCOPES = SCOPES
        self.jobCalendarId = ''#메일주소

    def get_pickle(self):
        try:
            with open('/home/lab05/A1B4/calendar_lab16/token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
    
        except:
            flow = InstalledAppFlow.from_client_secrets_file('/home/lab05/A1B4/calendar_lab16/token.pickle', self.SCOPES)
            self.creds = flow.run_console()
            with open('/home/lab05/A1B4/calendar_lab16/token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        service = build('calendar', 'v3', credentials = self.creds)

        return service

    def formatTimepoint(self, time):
        return str(time.year)  + '-' + str(time.month) + '-' + str(time.day) + 'T00:00:00'


    def making_due_list(self, contents):
        time_zone = 'Asia/Seoul'
        due_list = []
        print('contents : ',contents)
        # for content in contents:
        time = contents[0]
        summary = contents[1]
        

        due_dict = {
            'summary':summary,
            'start':{
                'dateTime': self.formatTimepoint(time),
                'timeZone': time_zone,
            },

            'end':{
                'dateTime': self.formatTimepoint(time),
                'timeZone': time_zone,
            }

        }

        due_list.append(due_dict)

        return due_list


    def insert_event(self, due_list):
        service = self.get_pickle()
        for due in due_list:
            event = service.events().insert(calendarId = self.jobCalendarId, body = due).execute()
            print('Event created: {}'.format(event.get('htmlLink')))
        return event


    