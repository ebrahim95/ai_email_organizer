import reflex as rx
import re
from pprint import pprint
from googleapiclient.errors import HttpError
from simplegmail import Gmail
from simplegmail.query import construct_query
from bs4 import BeautifulSoup


def remove_r_n_mine(string):
    # result = re.sub(r"\s*[\r\n\xa0\u200c]+\s*", " ", string)
    # return result
    soup = BeautifulSoup(string, "lxml")
    regex_filter = re.sub(r"\s*[\r\n\xa0\u200c]+\s*", " ", soup.get_text())

    return regex_filter


#
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def email():
    gmail = Gmail()
    message_list_append: list[list[str, str, str]] = []
    message_list_string: str = ""
    try:
        # Unread messages in your inbox
        query_params = {
            "newer_than": (1, "day"),
        }
        messages = gmail.get_messages(query=construct_query(query_params))

        for message in messages:
            message_list_string += "To: " + remove_r_n_mine(message.recipient)
            message_list_string += "From: " + remove_r_n_mine(message.sender)
            message_list_string += "Subject: " + remove_r_n_mine(message.subject)
            message_list_string += "Date: " + remove_r_n_mine(message.date)
            message_list_string += "Preview: " + remove_r_n_mine(message.snippet)

            if message.plain is not None:
                message_list_string += "Message Body: " + remove_r_n_mine(
                    message.plain
                )  # or message.html

            # use regex to filter
            message_list_append.append(message_list_string)
        return message_list_append

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
