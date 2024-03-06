import reflex as rx


class State(rx.State):
    count: int = 0
    logged_in: bool

    # message list
    message_list: list[list[str, str, str]] = []

    def store_message(self, string_list):
        self.message_list.append(string_list)

    def set_number(self):
        self.count = self.count + 1

    def set_boolean(self, status):
        self.logged_in = status
