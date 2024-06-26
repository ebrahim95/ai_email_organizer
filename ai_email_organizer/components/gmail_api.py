import reflex as rx
import base64
import os.path
import re
import email as femail
from pprint import pprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def email(creds=""):
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
    message_list_string: str = ""
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        message_list = (
            service.users().messages().list(userId="me", maxResults="3").execute()
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
                )
                who = "From:" + str(sender)
                subject = "Subject:" + str(subject)

                for a in decoded.findAll("a"):
                    a.extract()

                decoded = decoded.getText(" ", strip=True)

                # use regex to filter out strings
                # delete ( in between )
                result = re.sub(r"\([^)]*\)", " ", decoded)
                # delete \n\r
                result = re.sub(r"\s*[\r\n\xa0\u200c]+\s*", " ", result)
                # delete media queries
                result = re.sub(r"@media[^}]+}", " ", result)
                # delete between {}
                result = re.sub(r"{[^{}]*}", " ", result)
                # delete *-
                result = re.sub(r"[*-]", " ", result)

                # message_list_append.append(who)
                # message_list_append.append(subject)
                # message_list_append.append("message: " + result)
                message_list_string += who + subject + "message: " + result
                message_list_append.append(message_list_string)
        print(message_list_append)
        return message_list_append

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
