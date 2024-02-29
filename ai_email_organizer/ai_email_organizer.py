"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
import reflex as rx
from .components import gmail_api

docs_url = "https://reflex.dev/docs/getting-started/introduction"

filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    gmail_api.email()
    return rx.center(
        rx.theme_panel(),
        rx.vstack(
            rx.heading("Welcome to Gmail AI Organizer!", size="9"),
            rx.text("Get started by editing ", rx.code(filename)),
            rx.button(
                "Login",
                on_click=lambda: rx.redirect(docs_url),
                size="4",
            ),
            align="center",
            spacing="7",
            font_size="2em",
        ),
        height="100vh",
    )


app = rx.App()
app.add_page(index)
