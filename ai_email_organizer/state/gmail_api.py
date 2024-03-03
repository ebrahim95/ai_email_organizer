import reflex as rx 


class gmail_message(rx.State): 
    # message list 
    message_list: str 

    def store_message(self, string_list): 
        self.message_list += string_list
