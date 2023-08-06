from Homevee.TestDataGenerator.Generator import Generator


class ServerDataGenerator(Generator):
    def __init__(self, admin, db):
        super(ServerDataGenerator, self).__init__(admin, db, "ServerDataGenerator")
        return

    def generate_data(self):
        self.db.set_server_data("REMOTE_ID", "VX6FLAYZN")
        self.db.set_server_data("REMOTE_ACCESS_TOKEN", "+4mT6OzDRMQgZY4VX+cQGxnuSzFF4SjNFM+p/L90LdirFP6X0lIPfU8fCtfgUdoA3N+lpepN82UOgvZ/7lwV6BNYdYvNyD9duCFbNtwMpr+x+4WD5Ze0udQGvviN4W5FN4SFZ2eFh9fa2+DQdc1BBRXJKDwDpNPFPpJ1rmKsw1Y=")
        self.db.set_server_data("USE_REMOTE_CONTROL", "true")
        self.db.set_server_data("CLOUD_ACCESS_KEY", "q+89tj4odwWtNBklWjKQ8ZgH0qZKH3JFdMJiUdi1NF8=")