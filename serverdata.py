class ServerData:
    """A class to hold all necessary data of one server the bot is a member of."""

    def __init__(self, server_id="", channels=[], config=None, parser=None):
        self.server_id = server_id
        self.channel_list = channels
        self.config_file = config
        self.parser = parser

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
        channels = list(channels)
        new_list = []
        for i in range(0, len(channels)):
            if channels[i].is_default:
                new_list.insert(0, channels[i])
                if i < len(channels):
                    new_list = new_list + channels[i+1:]
                break
            else:
                new_list.append(channels[i])
        self.__channel_list = new_list

    @property
    def config_file(self):
        return self.__config_file

    @config_file.setter
    def config_file(self, config_file):
        self.__config_file = config_file

    def get_default_channel(self):
        return self.channel_list[0]

    @property
    def parser(self):
        return self.__parser

    @parser.setter
    def parser(self, parser):
        self.__parser = parser
