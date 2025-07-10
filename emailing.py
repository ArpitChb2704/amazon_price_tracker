import os
import base64
import pickle
import json
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64 as b64

# Gmail API Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Decode and save credentials.json
if os.getenv("GMAIL_CREDENTIALS_BASE64"):
    with open("credentials.json", "wb") as f:
        f.write(base64.b64decode(os.getenv("GMAIL_CREDENTIALS_BASE64")))

# Decode and save token.pickle
if os.getenv("GMAIL_TOKEN_BASE64"):
    with open("token.pickle", "wb") as f:
        f.write(base64.b64decode(os.getenv("GMAIL_TOKEN_BASE64")))

def send_email(to, message_text, subject="Amazon Price Alert"):
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = 'me'
        message['subject'] = subject

        raw_message = {'raw': b64.urlsafe_b64encode(message.as_bytes()).decode()}

        send_message = service.users().messages().send(userId="me", body=raw_message).execute()
        print(f'✅ Email sent to {to}, ID: {send_message["id"]}')
    except HttpError as error:
        print(f'❌ An error occurred: {error}')
