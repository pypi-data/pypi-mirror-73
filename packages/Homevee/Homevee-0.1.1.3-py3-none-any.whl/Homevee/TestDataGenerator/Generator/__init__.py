from abc import abstractmethod


class Generator:
    def __init__(self, admin, db, label):
        self.admin = admin
        self.db = db
        self.label = label

    def generate(self):
        print("Running "+self.label+"...")

        self.generate_data()

    @abstractmethod
    def generate_data(self):
        raise NotImplementedError