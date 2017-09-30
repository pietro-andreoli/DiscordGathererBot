import discord
import re
import asyncio
from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog
import configparser

support_email = ""

client = discord.Client()
channels = client.get_all_channels()
cfg = None
first_time_setup = False


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
    try:
        cfg = open("cfg.ini", 'r+')

    except OSError:
        first_time_setup = True




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
    default_channel = None
    for i in channels:
        if i.is_default:
            default_channel = i
            break
    await client.send_message(default_channel, "Fblthp armed and ready.")

    #for i in channels:
     #   print(type(i))
    #first_time_setup = False
    #open_config()
    #test=client.get_channel("general")
   # await client.send_message(test, "I'm ready!")
    '''if first_time_setup:
        await client.send_message(message.channel, 'Hello and thank you for using Fblthp, Gatherer Adept. We\'re going'
                                  + " to do some setup.\n"
                                  + "Right now a card fetch will look like the following.")
        temp = Card.where(name="\"Opt\"").all()
        card_set = 0
        await client.send_message(message.channel, "**\"" + temp[card_set].name + "\"**\n"
                                  + temp[card_set].mana_cost + "\n" + temp[card_set].type + "\n"
                                  + temp[card_set].rarity + "\n" + temp[card_set].text + "\n\n"
                                  + temp[card_set].image_url)
'''

@client.event
async def on_message(message):



    if message.content.startswith("good bot"):
        await client.send_message(message.channel, "Thanks :smile: :heart:")
    #Check if message has potential for  having a card request. Done by checking the number of open and close brackets
    # TODO create case for at least one valid request. Ex [[Opt]] [[ should get opt. [[opt]] [[opt]] ]]
    if message.content.count('[[') == message.content.count(']]') and message.content.count('[[') != 0:
        #Parse the input, find all the card requests
        requests = find_card_request(message)
        await client.send_message(message.channel, 'Request received...')
        for card in requests:
            temp = Card.where(name=card).all()
            print(card)
            print(temp)
            if len(temp) == 0:
                await client.send_message(message.channel, "The card " + card + "cant be found. This is the closest "
                                          + "I could find... sorry :frowning:")
                temp = Card.where(name=card[1:-1]).all()
            if len(temp) == 0:
                await client.send_message(message.channel, "The card " + card + "cant be found."
                                          + "\nIf you believe this is an error please email " + support_email)
            else:
                #card_set = 1
                for card_set in range(0, len(temp)):
                    try:
                        print(temp[card_set])
                        await client.send_message(message.channel,  "**\""+temp[card_set].name + "\"**\n"
                                                  + temp[card_set].mana_cost + "\n"+temp[card_set].type + "\n"
                                                  + temp[card_set].rarity + "\n" + temp[card_set].text + "\n\n"
                                                  + temp[card_set].image_url)
                        break;
                    except:
                        print("Couldnt find a card at position "+str(card_set))





client.run('MzYyNDIyNzg0MzUxMTQxODg5.DKycFw.cEEp9aDXGD_FZ_tBXs64mrLw9dU')