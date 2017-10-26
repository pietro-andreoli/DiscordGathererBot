commands = {}


def gather_commands():
    print()


async def cmd_help(client, channel):
    help_file = open("helpcommand.txt", 'r')
    help_file.close()
    await client.send_message(channel, help_file.read())


