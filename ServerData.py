class ServerData:
    """A class to hold all necessary data of one server the bot is a memeber of."""

    def __init__(self, server_id="", channels=[], config=None):
        self.server_id = server_id
        self.channel_list = channels
        self.config_file = config

    def get_id(self):
        return self.server_id

    def get_channels(self):
        return self.channel_list

    def get_config_file(self):
        return self.config_file
