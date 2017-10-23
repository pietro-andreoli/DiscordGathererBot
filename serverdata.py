class ServerData:
    """A class to hold all necessary data of one server the bot is a memeber of."""

    def __init__(self, server_id="", channels=[], config=None):
        self.server_id = server_id
        self.channel_list = channels
        self.config_file = config

    @property
    def server_id(self):
        return self.__server_id

    @server_id.setter
    def server_id(self, server_id):
        self.__server_id = server_id

    @property
    def channel_list(self):
        return self.__channel_list

    @channel_list.setter
    def channel_list(self, channels):
        self.__channel_list = channels

    @property
    def config_file(self):
        return self.__config_file

    @config_file.setter
    def config_file(self, config_file):
        self.__config_file = config_file

    def get_default_channel(self):
        return self.channel_list[0]