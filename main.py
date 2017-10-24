import discord
from mtgsdk import Card
from configparser import ConfigParser
import os.path
import atexit
from serverdata import ServerData
support_email = ""
# TODO: Cache requests and record how often theyre requested. After certain amount of time, delete cached requests of those with very low numbers
# TODO: Unit tests.
# TODO: Handle when the bot is added to a server. (create the ini file and such)
# Represents a client connection that connects to Discord. This class is used to interact with the Discord WebSocket
# and API.
client = discord.Client()
# Garbage that should be taken out soon
channels = client.get_all_channels()
# The variable holding the open config file.
cfg = None
# Parser for navigating ini file for server print settings.
cfg_parser = None
# Dictionary that uses connected server IDs as keys, and ServerData objects as values.
server_database = {}
# All the servers the bot is a member of.
servers = []


def find_card_request(message):
    """
    Parse a message from the user and look for any card requests.
    A card request is a set of double square brackets separated by a string that should be the card name.


    :param: message: The message object the user sent.
    :return: The list of card names that are being requested.
    """
    # Getting the content of the message and storing it for parsing.
    msg = message.content
    # Holds the names of all cards found to be requested.
    card_requests = []
    # Loop condition.
    parsing = True
    # Parses through message looking for any requests. Each iteration parses a single request.
    while parsing:
        # Gets position of the first occurrence of opening a request.
        opening_brackets = msg.find('[[')
        # Gets position of the first occurrence of closing a request.
        closing_brackets = msg.find(']]')
        # Checking for absence of open or close symbols.
        if opening_brackets == -1 or closing_brackets == -1:
            print("False Request. Could not locate an opening or a closing symbol.")
            break
        # Checking for brackets being out of order
        if closing_brackets < opening_brackets:
            print("False Request. Opening symbol occurs after closing symbol.")
            break
        # Retrieve the string encapsulated by the request symbols. Adds quotes around the string to assist in fetching
        # the card from the database later.
        curr_parse = "\"" + msg[opening_brackets + 2:closing_brackets] + "\""
        # Adds the current cards name to the request list.
        card_requests.append(curr_parse)
        print(curr_parse)
        # Truncate the message to the character after the closing bracket that was parsed for the next iteration.
        msg = msg[closing_brackets + 2:]
    # return the cards that were found.
    return card_requests


def create_config():
    """
    Creates a configuration file.
    This function needs to be updated to support multiple servers.
    :return:
    """
    global cfg
    # Creates an ini file with writing permission.
    cfg = open("cfg.ini", 'w+')
    # Writes the following string to the file. This will control what is and isnt printed ofr a card fetch.
    cfg.write("[Fetch Options]\n"
              "Open Wrap Character: [[\n"
              "Closed Wrap Character: ]]\n"
              "[Print Options]\n"
              "Name: True\n"
              "Mana_Cost: True\n"
              "CMC: False\n"
              "Colors: False\n"
              "Type: True\n"
              "Supertypes: False\n"
              "Subtypes: False\n"
              "Types: False\n"
              "Rarity: True\n"
              "Text: True\n"
              "Flavor: False\n"
              "Artist: False\n"
              "Number: False\n"
              "Power: False\n"
              "Toughness: False\n"
              "Loyalty: False\n"
              "Multiverse_ID: False\n"
              "Variations: False\n"
              "Watermark: False\n"
              "Border: False\n"
              "Timeshifted: False\n"
              "Release_Date: False\n"
              "Printings: False\n"
              "Original_Text: False\n"
              "Original_Type: False\n"
              "Image_Url: True\n"
              "Set:False\n"
              "Set_Name: False\n"
              "ID: False\n"
              "Legalities: False\n"
              "Rulings: False\n"
              "Foreign_Names: False\n")


async def fluff_messages(message):
    if "good bot" in message.content or "Good bot" in message.content:
        await client.send_message(message.channel, "Thanks :smile: :heart:")
    if "bad bot" in message.content or "Bad bot" in message.content:
        await client.send_message(message.channel, "Contact my dev, I can only do as well as he programs :cry:")
    if "send nudes" in message.content or "Send nudes" in message.content:
        await client.send_message(message.channel, "You can see whats hiding underneath here :wink: \nhttps://github.co"
                                                   "m/topfight/DiscordGathererBot")


def create_config(file_name):
    """
    Creates a configuration file.
    This function needs to be updated to support multiple servers.
    :return:
    """
    global cfg
    # Creates an ini file with writing permission.
    cfg = open(file_name, 'w+')
    # Writes the following string to the file. This will control what is and isnt printed ofr a card fetch.
    cfg.write("[Fetch Options]\n"
              "Open Wrap Character: [[\n"
              "Closed Wrap Character: ]]\n"
              "[Print Options]\n"
              "Name: True\n"
              "Mana_Cost: True\n"
              "CMC: False\n"
              "Colors: False\n"
              "Type: True\n"
              "Supertypes: False\n"
              "Subtypes: False\n"
              "Types: False\n"
              "Rarity: True\n"
              "Text: True\n"
              "Flavor: False\n"
              "Artist: False\n"
              "Number: False\n"
              "Power: False\n"
              "Toughness: False\n"
              "Loyalty: False\n"
              "Multiverse_ID: False\n"
              "Variations: False\n"
              "Watermark: False\n"
              "Border: False\n"
              "Timeshifted: False\n"
              "Release_Date: False\n"
              "Printings: False\n"
              "Original_Text: False\n"
              "Original_Type: False\n"
              "Image_Url: True\n"
              "Set:False\n"
              "Set_Name: False\n"
              "ID: False\n"
              "Legalities: False\n"
              "Rulings: False\n"
              "Foreign_Names: False\n")


async def card_fetch_line_of_defense_two(card_name, channel, card_list):
    """
    This function is called when wanting to get the card details. But first you need to make sure the search for the
    card yielded a valid result.

    :param: card_name: String holding the name of the card to search.
    :param: channel: Channel object to send the message to.
    :param: card_list: List of Card objects.
    :return:
    """
    print(card_name)
    # If the list is empty then that means the card could not be found.
    if len(card_list) == 0:
        # Try searching without the quotes. This will look for a card with (supposedly) the closest name.
        card_list = Card.where(name=card_name[1:-1]).all()
        # If the list has contents then a card was found.
        if len(card_list) > 0:
            # Tell the user it could not find the card and that this is the best guess.
            await client.send_message(channel, "The card " + card_name + "cant be found. This is the closest "
                                      + "I could find... sorry :frowning:")
    # If the list is empty then that means the card could not be found.
    if len(card_list) == 0:
        # Tell the user that the card could not be found.
        await client.send_message(channel, "The card " + card_name + "cant be found."
                                  + "\nIf you believe this is an error please email " + support_email)
    else:
        await get_card_details(card_list, channel)

        
async def fetch_card(requests, channel):
    """
    Uses the MTGSDK api to fetch cards with the names stored in requests. Then prints details about the card depending
    on the options turned to True in the ini file for the appropriate server.
    :param: requests: List of strings holding the card names in quotes.
    :param: message: The original message.
    :return: None
    """

    # Loops through request list.
    for card in requests:
        # Checks if the request is an empty string or the string "".
        if card == '\"\"' or card == "":
            print("Fetch Error: Card request is empty.")
            # Skip this request and move on to the next.
            continue
        # Fetch a card with the exact name as requested. It gets the exact name by having the quotes surrounding it
        # (added previously). temp becomes a list consisting of the requested card in each set it was printed in.
        temp = Card.where(name=card).all()
        await card_fetch_line_of_defense_two(card, channel, temp)




async def get_card_details(card_options, channel):
    """
    Gets the details of a card using a list of query results stored in card_options. Uses the details specified in the
    ini file for the server.
    :param: card_options: List of Card objects
    :param: message: The original message sent
    :return:
    """
    # Loop through the list of cards.
    for card_set in range(0, len(card_options)):
        # Try to print the desired card details. A ValueError is raised if there are any problems with getting
        # the desired information.
        try:
            print(card_options[card_set])
            # Holds the result of the fetch.
            request_output = ""
            # cfg_parser.items("Print Options") gets the option-value pair from the ini file under the header
            # "Print Options".
            # Ex - The following would be in an ini file: card_name = True. option -> 'card_name' value -> True
            # TODO: Find ways to make this more modular.
            for option, value in cfg_parser.items("Print Options"):
                # If the option has been turned on, then print the detail related to this option.
                if value == 'True':
                    print("Option:" + option)
                    # gets the value of the option from the card.
                    attr = getattr(card_options[card_set], option)
                    # Checks if the value could not be found.
                    # TODO This will mess things up when user turns on Loyalty printing and requests a card without loyalty. Find a better way to check if an attribute is missing
                    if attr is None or attr == "None":
                        # Raise a value error.
                        print("PROBLEM HERE")
                        print(attr)
                        raise ValueError
                    # Append the attribute to the message to be printed.
                    request_output += str(attr) + "\n"
            print(request_output)
            # Send the message to the requester.
            await client.send_message(channel, request_output)
            # Stop the loop as we have successfully sent the message.
            break
        # A ValueError is raised whenever there is trouble retrieving an attribute from a card.
        except ValueError:
            print("Couldnt find a card at position " + str(card_set))


async def open_config(server):
    """
    Opens the config for a server using the ID in the object for that server
    :param: server: ServerData object for the server.
    :return:
    """
    global cfg_parser
    global cfg
    cfg_path = "./"+server.server_id+".ini"
    cfg_name = cfg_path[2:]
    if os.path.isfile(cfg_path):
        # open_config()
        # await client.send_message(server.get_default_channel(), "Fblthp armed and ready.")
        cfg_parser = ConfigParser()
        cfg_parser.read(cfg_name)
    else:
        create_config(cfg_name)
        cfg.close()
        cfg_parser = ConfigParser()
        cfg_parser.read(cfg_name)
        await client.send_message(server.get_default_channel(), 'Hello and thank you for using Fblthp, Gatherer Adept. '
                                  + 'We\'re going'
                                  + " to do some setup.\n"
                                  + "\nTo request a card, simply wrap the card name in double square brackets. "
                                  + "\nRight now a card fetch will look like the following."
                                  + "\n[[Opt]]")

@client.event
async def on_ready():
    """
    Overriding the on_ready() function in discord library.
    :return: None
    """
    print('Logged in as: ')
    print(client.user.name)
    print(client.user.id)
    print('-------------')
    global cfg
    global cfg_parser
    global server_database
    global servers
    # Gets all servers the bot is a member of, stores their id. In addition to this, the server IDs are used as the keys
    # for a dictionary. The loop stores the server IDs and channels in a ServerData object and uses that as the value of
    # the key in the dictionary.
    for curr_server in client.servers:
        # Recording the servers ID for later use.
        servers.append(curr_server.id)
        # Setting up the server dictionary with the key.
        server_database[curr_server.id] = ServerData(curr_server.id, curr_server.channels)
        print(server_database[curr_server.id].channel_list)
        await open_config(server_database[curr_server.id])



@client.event
async def on_message(message):
    await fluff_messages(message)

    # Check if message has potential for  having a card request. Done by checking the number of open and close brackets
    if message.content.count('[[') > 0 and message.content.count(']]') > 0:
        # Parse the input, find all the card requests
        requests = find_card_request(message)
        await client.send_message(message.channel, 'Request received...')
        await fetch_card(requests, message.channel)


def on_exit():
    print("closing")
    global cfg
    #cfg.close()


atexit.register(on_exit)
client.run('MzYyNDIyNzg0MzUxMTQxODg5.DKycFw.cEEp9aDXGD_FZ_tBXs64mrLw9dU')
