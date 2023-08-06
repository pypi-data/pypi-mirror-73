from Homevee.Manager.RoomManager import RoomManager
from Homevee.TestDataGenerator.Generator import Generator

class RoomGenerator(Generator):
    def __init__(self, admin, db):
        super(RoomGenerator, self).__init__(admin, db, "RoomGenerator")
        return

    def generate_data(self):
        room_manager = RoomManager()
        room_manager.add_edit_room(self.admin, "Schlafzimmer", 1, "bed", self.db)
        room_manager.add_edit_room(self.admin, "Wohnzimmer", 2, "tv", self.db)
        room_manager.add_edit_room(self.admin, "Küche", 3, "fridgefreezer", self.db)
        room_manager.add_edit_room(self.admin, "Büro", 4, "workdesk", self.db)
        room_manager.add_edit_room(self.admin, "Bad", 5, "bath", self.db)
        room_manager.add_edit_room(self.admin, "Keller", 6, "bedroom", self.db)
        room_manager.add_edit_room(self.admin, "Garten", 7, "flower", self.db)