import discord
import re
import asyncio
from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog
from configparser import ConfigParser
import os.path
support_email = ""
#TODO: Cache requests and record how often theyre requested. After certain amount of time, delete cached requests of those with very low numbers
client = discord.Client()
channels = client.get_all_channels()
cfg = None
first_time_setup = False
cfg_parser = None

def find_card_request(message):
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
    global first_time_setup
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
                            #TODO This will mess things up when user turns on Loyalty printing and requests a card without loyalty. Find a better way to check if an attribute is missing
                            if attr == None or attr == "None":
                                raise ValueError
                            print('did this work 3')
                            if option == "image_url":
                                print(value)
                            request_output += str(attr)+"\n"
                            print('did this work 4')
                    print(request_output)
                    await client.send_message(message.channel, request_output)
                    #await client.send_message(message.channel, "**\"" + temp[card_set].name + "\"**\n"
                    #                    + temp[card_set].mana_cost + "\n" + temp[card_set].type + "\n"
                    #                    + temp[card_set].rarity + "\n" + temp[card_set].text + "\n\n"
                    #                    + temp[card_set].image_url)
                    print("ayy lmao" + request_output)
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
    global first_time_setup
    global cfg
    global cfg_parser
    default_channel = None
    for i in channels:
        if i.is_default:
            default_channel = i
            break


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