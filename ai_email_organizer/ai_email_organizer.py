from rxconfig import config
import reflex as rx
from .components import gmail_api
from .state.gmail_api import State
from .components import llm

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


def login_button() -> rx.Component:
    return rx.hstack(
        State.count,
        rx.chakra.input(placeholder="Start Summarizing right now --->"),
        rx.button("Login", on_click=State.set_number, size="4"),
    )


def index() -> rx.Component:
    data = gmail_api.email()
    llm.llm(data)
    return rx.center(
        # rx.theme_panel(),
        rx.vstack(
            rx.heading("Welcome to Gmail AI Summarizer!", size="9"),
            rx.text("Get started by editing ", rx.code(filename)),
            login_button(),
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
