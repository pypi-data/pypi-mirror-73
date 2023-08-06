from Homevee.APIModule import APIModule
from Homevee.Item.ChatMessage import ChatMessage
from Homevee.Item.Status import *
from Homevee.Manager.ChatManager import ChatManager

ACTION_KEY_GET_CHAT_MESSAGES = "getchatmessages"
ACTION_KEY_GET_CHAT_IMAGE = "getchatimage"
ACTION_KEY_SEND_CHAT_MESSAGE = "sendchatmessage"

class ChatAPIModule(APIModule):
    def __init__(self):
        super(ChatAPIModule, self).__init__()
        self.chat_manager = ChatManager()
        return

    def get_function_mappings(self):
        mappings = {
            ACTION_KEY_GET_CHAT_MESSAGES: self.get_chat_messages,
            ACTION_KEY_GET_CHAT_IMAGE: self.get_chat_image,
            ACTION_KEY_SEND_CHAT_MESSAGE: self.send_chat_message
        }
        return mappings

    def get_chat_messages(self, user, request, db) -> Status:
        messages = self.chat_manager.get_chat_messages(user, request['time'], request['limit'], db)
        return Status(type=STATUS_OK, data={'messages': ChatMessage.list_to_dict(messages)})

    def get_chat_image(self, user, request, db) -> Status:
        data = self.chat_manager.get_chat_image(user, request['imageid'], db)
        return Status(type=STATUS_OK, data=data)

    def send_chat_message(self, user, request, db) -> Status:
        data = self.chat_manager.send_chat_message(user, request['data'], db)
        return Status(type=STATUS_OK, data=data)