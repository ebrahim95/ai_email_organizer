import reflex as rx
from pprint import pprint
from googleapiclient.errors import HttpError
from simplegmail import Gmail
from simplegmail.query import construct_query


gmail = Gmail()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def email(creds=""):
    gmail = Gmail()
    message_list_append: list[list[str, str, str]] = []
    message_list_string: str = ""
    try:
        # Unread messages in your inbox
        query_params = {
            "newer_than": (2, "day"),
        }
        messages = gmail.get_messages(query=construct_query(query_params))

        # Print them out!
        for message in messages:
            message_list_string += "To: " + message.recipient
            message_list_string += "From: " + message.sender
            message_list_string += "Subject: " + message.subject
            message_list_string += "Date: " + message.date
            message_list_string += "Preview: " + message.snippet

            if message.plain is not None:
                message_list_string += (
                    "Message Body: " + message.plain
                )  # or message.html

        return message_list_append

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
