import json

from Homevee.APIModule import APIModule
from Homevee.Helper import translations
from Homevee.Item.Status import *
from Homevee.VoiceAssistant import VoiceAssistant
from Homevee.VoiceAssistant.VoiceReplaceManager import VoiceReplaceManager

ACTION_KEY_VOICE_COMMAND = "voicecommand"
ACTION_KEY_GET_VOICE_REPLACE_ITEMS = "getvoicereplaceitems"
ACTION_KEY_ADD_EDIT_VOICE_REPLACE_ITEM = "addeditvoicereplaceitem"
ACTION_KEY_DELETE_VOICE_REPLACE_ITEM = "deletevoicereplaceitem"

class VoiceAPIModule(APIModule):
    def __init__(self):
        super(VoiceAPIModule, self).__init__()
        self.voice_replace_manager = VoiceReplaceManager()
        return

    def get_function_mappings(self):
        mappings = {
            ACTION_KEY_VOICE_COMMAND: self.voice_command,
            ACTION_KEY_GET_VOICE_REPLACE_ITEMS: self.get_voice_replace_items,
            ACTION_KEY_ADD_EDIT_VOICE_REPLACE_ITEM: self.add_edit_voice_replace_item,
            ACTION_KEY_DELETE_VOICE_REPLACE_ITEM: self.delete_voice_replace_item
        }
        return mappings

    def voice_command(self, user, request, db) -> Status:
        if 'language' in request:
            language = request['language']
        else:
            language = translations.LANGUAGE

        if ('user_last_location' in request and request['user_last_location'] is not None):
            user_last_location = json.loads(request['user_last_location'])
        else:
            user_last_location = None

        response = VoiceAssistant().do_voice_command(user, request['text'], user_last_location, None, db, language)
        return Status(type=STATUS_OK, data=response)

    def get_voice_replace_items(self, user, request, db) -> Status:
        replace_data = self.voice_replace_manager.get_voice_replace_items(user, db)
        return Status(type=STATUS_OK, data={'replacedata': replace_data})

    def add_edit_voice_replace_item(self, user, request, db) -> Status:
        success = self.voice_replace_manager.add_edit_voice_replace_item(user, request['replacewith'], request['itemstoreplace'], db)
        return Status(type=STATUS_OK)

    def delete_voice_replace_item(self, user, request, db) -> Status:
        success = self.voice_replace_manager.delete_voice_replace_item(user, request['replacewith'], db)
        return Status(type=STATUS_OK)