from Homevee.Manager.PersonManager import PersonManager
from Homevee.TestDataGenerator.Generator import Generator

class PersonGenerator(Generator):
    def __init__(self, admin, db):
        super(PersonGenerator, self).__init__(admin, db, "PersonGenerator")
        return

    def generate_data(self):
        manager = PersonManager()

        #manager.add_edit_person(self, self.admin, id, name, nickname, address, latitude, longitude, phonenumber, birthdate, self.db)