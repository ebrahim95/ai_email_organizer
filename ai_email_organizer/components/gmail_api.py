import reflex as rx
import base64
import os.path
import email as femail
from pprint import pprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ..state.gmail_api import State
from bs4 import BeautifulSoup


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def login():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=50000)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def email():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=50000)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    message_list_append: list[list[str, str, str]] = []
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        message_list = (
            service.users().messages().list(userId="me", maxResults="10").execute()
        )
        messages = message_list.get("messages", [])

        if not messages:
            print("No messages found.")
            return

        print("Messages:")
        for message in messages:
            return_message_snippet = (
                service.users().messages().get(userId="me", id=message["id"]).execute()
            )
            """ alternative way to get message"""
            # get body message from the email
            # encoded_text = return_message_snippet["payload"]["body"].get("data", 0)
            # print(encoded_text)
            # if encoded_text != 0:
            #     text = base64.urlsafe_b64decode(encoded_text.encode("utf-8")).decode(
            #         "utf-8"
            #     )
            #     gmail_message.store_message(text)
            payload = return_message_snippet["payload"]
            headers = payload["headers"]
            parts = payload.get("parts", 0)
            data = parts[0]["body"].get("data", 0) if parts != 0 else 0

            # pprint(payload, depth=1)
            # print("\n")
            # print(
            #     "----------------------------------------------------------------------------------"
            # )
            # print("\n")

            for who in headers:
                if who["name"] == "Subject":
                    subject = who["value"]
                if who["name"] == "From":
                    sender = who["value"]

            if data != 0:
                decoded = BeautifulSoup(
                    base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8"),
                    "lxml",
                ).getText()
                who = "From:" + str(sender)
                subject = "Subject:" + str(subject)
                # print("From", sender)
                # print("Subject", subject)
                # print(decoded)
                # print(
                #     "----------------------------------------------------------------------------------"
                # )
                message_list_append.append([who, subject, decoded])
            #     State.store_message([who, subject, decoded])
            #     State.set_number()
            # print(State.count)
        return message_list_append
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
