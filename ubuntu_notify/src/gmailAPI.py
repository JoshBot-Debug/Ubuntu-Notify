from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GmailApi:
    """
        This class is used to get the latest email if it is unread.
    """

    # If modifying these scopes, delete the file token.pickle.
    __SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


    def __init__(self):
        """ Makes the connection to the Gmail """

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.__SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.__service = build('gmail', 'v1', credentials=creds)


    def getLatestEmail(self) -> dict:
        """ Get the most recent email received if it is unread """

        # Get the latest email that's unread
        response = self.__getContent("me")
        notificationData = {}

        # Format and save the data in a dict. Return the dict.
        if "UNREAD" in response['labelIds'] and "CATEGORY_PROMOTIONS" not in response['labelIds'] and "CATEGORY_SOCIAL" not in response['labelIds']:
            for x in response["payload"]["headers"]:
                if x["name"] == "Delivered-To":
                    notificationData.update({"to": x["value"]})
                if x["name"] == "From":
                    notificationData.update({"from": x["value"]})
                if x["name"] == "Date":
                    notificationData.update({"date": x["value"]})
                if x["name"] == "Subject":
                    notificationData.update({"subject": x["value"]})
            
            return notificationData
        
        return notificationData


    def __getContent(self, user_id: str):
        """ Make the call to the Gmail API """
        try:
            emailID = self.__service.users().messages().list(userId=user_id).execute()["messages"][0]["id"]
            return self.__service.users().messages().get(userId=user_id, id=emailID).execute()
        except Exception as error:
            raise Exception('An error occurred: %s' % error)