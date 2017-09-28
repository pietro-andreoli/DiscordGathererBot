import discord
import re
import asyncio
from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog

client = discord.Client()
@client.event
async def on_ready():
    print('Logged in as: ')
    print(client.user.name)
    print(client.user.id)
    print('-------------')

@client.event
async def on_message(message):
    #Check if message has potential for  having a card request. Done by checking the number of open and close brackets
    if message.content.count('[[') == message.content.count(']]'):
        find_card_request(message)


client.run('MzYyNDIyNzg0MzUxMTQxODg5.DKycFw.cEEp9aDXGD_FZ_tBXs64mrLw9dU')

#Parses the message and finds all requests for cards.
#message - variable that holds the message that is to be parsed
def find_card_request (message):
    msg = message.content
    card_requests = []
    parsing = True
    while parsing:
        opening_brackets = msg.find('[[')
        closing_brackets = msg.find(']]')
        if opening_brackets == -1 or closing_brackets == -1:
            break
        curr_parse = msg[opening_brackets+1:closing_brackets]
        card_requests.append(curr_parse)
        msg = msg[closing_brackets+1:-1]
#test