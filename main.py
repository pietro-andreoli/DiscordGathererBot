import discord
from mtgsdk import Card
from configparser import ConfigParser
import os.path
support_email = ""
# TODO: Cache requests and record how often theyre requested. After certain amount of time, delete cached requests of those with very low numbers
# TODO: Unit tests.
# Represents a client connection that connects to Discord. This class is used to interact with the Discord WebSocket
# and API.
client = discord.Client()
# Garbage that should be taken out soon
channels = client.get_all_channels()
# The variable holding the open config file.
cfg = None
# Parser for navigating ini file for server print settings.
cfg_parser = None
# Dictionary that uses connected server IDs as keys, and channel IDs in a list as values.
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
    msg = message.content
    card_requests = []
    parsing = True
    while parsing:
        opening_brackets = msg.find('[[')
        closing_brackets = msg.find(']]')
        if opening_brackets == -1 or closing_brackets == -1:
            print("done with request")
            break
        if closing_brackets < opening_brackets:
            break
        curr_parse = "\"" + msg[opening_brackets + 2:closing_brackets] + "\""
        card_requests.append(curr_parse)
        print(curr_parse)
        msg = msg[closing_brackets + 2:]
        # print("new request")
        # print(msg)
    return card_requests


def open_config():
    global cfg
    cfg = open("cfg.ini", 'r+')


def create_config():
    global cfg
    cfg = open("cfg.ini", 'w+')
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


async def fetch_card(requests, message):
    for card in requests:
        if card == '\"\"' or card=="":
            print("problem with: "+card)
            continue
        temp = Card.where(name=card).all()
        print(card)
        print(temp)
        if len(temp) == 0:

            temp = Card.where(name=card[1:-1]).all()
            if len(temp) > 0:
                await client.send_message(message.channel, "The card " + card + "cant be found. This is the closest "
                                          + "I could find... sorry :frowning:")
        if len(temp) == 0:
            await client.send_message(message.channel, "The card " + card + "cant be found."
                                + "\nIf you believe this is an error please email " + support_email)
        else:
            # card_set = 1
            for card_set in range(0, len(temp)):
                try:
                    print(temp[card_set])
                    request_output = ""
                    print(cfg_parser.options("Print Options"))
                    for option, value in cfg_parser.items("Print Options"):
                        print("did this work 1")
                        if value == 'True':
                            print("Option:" +option)
                            attr = getattr(temp[card_set], option)
                            # TODO This will mess things up when user turns on Loyalty printing and requests a card without loyalty. Find a better way to check if an attribute is missing
                            if attr == None or attr == "None":
                                raise ValueError
                            print('did this work 3')
                            if option == "image_url":
                                print(value)
                            request_output += str(attr)+"\n"
                            print('did this work 4')
                    print(request_output)
                    await client.send_message(message.channel, request_output)
                    break;
                except:
                    print("Couldnt find a card at position " + str(card_set))
#Parses the message and finds all requests for cards.
#message - variable that holds the message that is to be parsed

#card_library = Card.all()




@client.event
async def on_ready():
    print('Logged in as: ')
    print(client.user.name)
    print(client.user.id)
    print('-------------')
    global cfg
    global cfg_parser
    global server_database
    global servers
    # Gets all servers the bot is a member of, stores their id. In addition to this, the server IDs are used as the keys
    # for a dictionary. The loop stores the IDs in a list and uses that list as the value of the key in the dictionary.
    # The first element in each list is the default channel for that server.
    for serv in client.servers:
        # Recording the servers ID for later use.
        servers.append(serv.id)
        # Setting up the server dictionary with the key.
        server_database[serv.id] = []
        # Loops through all the channels the server has.
        for channel in serv.channels:
            # Adds the channel to the list. If its the default channel, put it first in the list.
            if channel.is_default:
                server_database[serv.id].insert(0, channel.id)
            else:
                server_database[serv.id].append(channel.id)
    # TODO: THIS CODE SHOULD BE REMOVED WHEN THE ABOVE FOR LOOK IS IMPLEMENTED PROPERLY
    default_channel = None
    for i in channels:
        if i.is_default:
            default_channel = i
            break
    # TODO: remove default_channel support from this and replace with the new dictionary method.
    if os.path.isfile("./cfg.ini"):
        open_config()
        await client.send_message(default_channel, "Fblthp armed and ready.")
        cfg_parser = ConfigParser()
        cfg_parser.read('cfg.ini')
        print(cfg_parser.get("Print Options", "Name"))
    else:
        await client.send_message(default_channel, 'Hello and thank you for using Fblthp, Gatherer Adept. We\'re going'
                                  + " to do some setup.\n"
                                  + "\nTo request a card, simply wrap the card name in double square brackets. "
                                  + "\nRight now a card fetch will look like the following."
                                  + "\n[[Opt]]")
        #temp = Card.where(name="\"Opt\"").all()
        #card_set = 0
        #await client.send_message(default_channel, "**\"" + temp[card_set].name + "\"**\n"
        #                          + temp[card_set].mana_cost + "\n" + temp[card_set].type + "\n"
        #                          + temp[card_set].rarity + "\n" + temp[card_set].text + "\n\n"
        #                          + temp[card_set].image_url)
        create_config()
        cfg.close()

@client.event
async def on_message(message):
    if "good bot" in message.content:
        await client.send_message(message.channel, "Thanks :smile: :heart:")
    #Check if message has potential for  having a card request. Done by checking the number of open and close brackets
    if message.content.count('[[') > 0 and  message.content.count(']]') > 0:
        #Parse the input, find all the card requests
        requests = find_card_request(message)
        await client.send_message(message.channel, 'Request received...')
        await fetch_card(requests, message)





client.run('MzYyNDIyNzg0MzUxMTQxODg5.DKycFw.cEEp9aDXGD_FZ_tBXs64mrLw9dU')