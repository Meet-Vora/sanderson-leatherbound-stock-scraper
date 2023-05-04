import base64
import email
from email.message import EmailMessage

import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from data_wrapper import get_email

# If modifying these scopes, delete the file token_emailer.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.send']

def send_email(content_listings, subject):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    creds = None
    # The file token_emailer.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_emailer.pickle'):
        with open('token_emailer.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            # flow.redirect_uri = 'http://localhost:59344/'
            creds = flow.run_local_server(port=59344)
        # Save the credentials for the next run
        with open('token_emailer.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        email_message = ""
        for listing in content_listings:
            email_message += str(listing) + "\n\n"
        message.set_content(email_message)
        message['To'] = get_email()
        message['From'] = get_email()
        message['Subject'] = subject

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        # create and send message
        create_message = { 'raw': encoded_message }
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print('Message Id: {}'.format(send_message["id"]))

    except HttpError as error:
        print('An error occurred: {error}')
        send_message = None

    return send_message
