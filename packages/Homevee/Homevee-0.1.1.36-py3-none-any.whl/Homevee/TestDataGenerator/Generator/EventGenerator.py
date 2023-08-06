from Homevee.Manager.EventManager import EventManager
from Homevee.TestDataGenerator.Generator import Generator

class EventGenerator(Generator):
    def __init__(self, admin, db):
        super(EventGenerator, self).__init__(admin, db, "EventGenerator")
        return

    def generate_data(self):
        manager = EventManager()

        manager.add_event(None, "Das ist ein Test-Ereignis", self.db)