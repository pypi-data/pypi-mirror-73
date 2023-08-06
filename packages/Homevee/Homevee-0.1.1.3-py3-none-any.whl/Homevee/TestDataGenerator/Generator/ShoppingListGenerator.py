from Homevee.Manager.ShoppingListManager import ShoppingListManager
from Homevee.TestDataGenerator.Generator import Generator

class ShoppingListGenerator(Generator):
    def __init__(self, admin, db):
        super(ShoppingListGenerator, self).__init__(admin, db, "ShoppingListGenerator")
        return

    def generate_data(self):
        manager = ShoppingListManager()

        manager.add_edit_shopping_list_item(self.admin, "", 1, "Avocado", self.db)
        manager.add_edit_shopping_list_item(self.admin, "", 2, "Äpfel", self.db)
        manager.add_edit_shopping_list_item(self.admin, "", 1, "Milch", self.db)
        manager.add_edit_shopping_list_item(self.admin, "", 3, "Semmeln", self.db)
        manager.add_edit_shopping_list_item(self.admin, "", 1, "Deo", self.db)