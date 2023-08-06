from Homevee import Homevee
from Homevee.Manager.UserManager import UserManager
from Homevee.TestDataGenerator.Generator.EventGenerator import EventGenerator
from Homevee.TestDataGenerator.Generator.PersonManager import PersonGenerator
from Homevee.TestDataGenerator.Generator.RoomGenerator import RoomGenerator
from Homevee.TestDataGenerator.Generator.ServerDataGenerator import ServerDataGenerator
from Homevee.TestDataGenerator.Generator.ShoppingListGenerator import ShoppingListGenerator
from Homevee.Utils.Database import Database


class TestDataGenerator:
    def __init__(self):
        return

    def generate_test_data(self):
        print("Generating test-data...")

        self.clear_database()

        test_admin_name = "testadmin"
        Homevee().add_user(username=test_admin_name, password="testpw", is_admin=True)

        self.admin_user = UserManager().find_by_username(test_admin_name, self.db)

        self.generate_data()

    def clear_database(self):
        Database.clear()
        self.db = Database()

    def generate_data(self):
        generators = [
            ServerDataGenerator(self.admin_user, self.db),
            RoomGenerator(self.admin_user, self.db),
            EventGenerator(self.admin_user, self.db),
            PersonGenerator(self.admin_user, self.db),
            ShoppingListGenerator(self.admin_user, self.db)
        ]

        for generator in generators:
            generator.generate()

        pass