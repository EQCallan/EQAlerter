import discord
import asyncio

from os import listdir
from os.path import isfile, join

# classes
from DepCheck import *
from CharacterList import *

#### MAIN PROGRAM ####

# dependency checks
DepCheck.verifyOS()
DepCheck.verifyLogging()

### USER DEFINED SETTINGS ###

# eq installation directory
EQHOME = 'C:/Users/Public/Daybreak Game Company/Installed Games/EverQuest'

## Discord specific settings - only needed if using Discord Bot version ##
## Obtain via 'developer mode' in Discord and by right clicking on the channel, then choose copy id ##
# general chat channel ID on discord server
GUILDCHAT_ID = '<INSERT DISCORD CHANNEL ID>'

# Discord Bot TOKEN - DO NOT SHARE!
# Obtained from your Discord applications page under your registered Bot for this application
TOKEN = '<INSERT YOUR BOT TOKEN>'

### END USER DEFINED SETTINGS ###

# program banner
# TODO: NEED FUNKY ASCII ART HERE
print("\n\nStarting The EverQuest Guild Chat Relay - Discord Bot Version\n")
print("Press Ctrl+C to exit\n")

# get character info
ALLFILES = [u for u in listdir(EQHOME) if isfile(join(EQHOME, u))]
sub = "UI_"
UIFILES = [s for s in ALLFILES if sub in s]

# create linked list of characters and generate menu
CHARLIST = LinkedList()

count = 0
for i in UIFILES:
    count = count + 1
    tmp = i.split("_")
    CHARNAME = tmp[1]
    CHARSERVER = tmp[2].split(".")
    CHARSERVER = CHARSERVER[0]
    CHARLIST.add(CHARNAME, CHARSERVER)

iterator = iter(CHARLIST)
count = 0
for c in CHARLIST:
    print("%d: %s" % (count, next(iterator)))
    count = count + 1

# ask user to pick character to control from list
CHARNUM = input("\n\nEnter the number of the character's log file that you would like to monitor from the list: ")
CHARACTER = CHARLIST.getName(CHARNUM)
SERVER = CHARLIST.getServer(CHARNUM)

# generate logfile path
LOGPATH = "Logs/eqlog_%s_%s.txt" % (CHARACTER, SERVER)
LOGFILE = EQHOME+LOGPATH
print(LOGFILE)
DepCheck.verifyLogFile(CHARACTER, LOGFILE)

# start up the bot and log in to discord
client = discord.Client()

# start up the bot
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('----------')
    await client.send(discord.Object(id=GUILDCHAT_ID), 'Hello, my name is GuildBot.  I am here to proxy guild chat messages to this channel.  Type !help for more info.', tts=False)

# some bot commands for testing and information
@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    # bot info
    elif message.content.startswith('!help'):
        await client.send(message.channel, 'Hello, my name is GuildBot.  I am here to proxy guild chat messages to this channel. My creator is Nuggethead.', tts=False)

# loop through log file
@client.event
async def readline(f):
    while True:
        data = f.readline()
        if data:
            return data
        await asyncio.sleep(.5)

# begin parsing log file for triggers and perform actions
@client.event
async def logfile_loop():

    # open log file for reading
    with open(LOGFILE, 'r+') as f:

        # move to the end of the file
        f.truncate()


        #### PARSE FOR TRIGGERS AND GENERATE ALERT IN DISCORD ####
        while True:
            line = await readline(f)
            # print(line)  # for debugging

            if line:

                # guild chat - send to discord
                if ('tells the guild') in line:
                    await client.send(discord.Object(id=GUILDCHAT_ID), line, tts=False)

                # guild chat - send to discord
                if ('say to your guild') in line:
                    await client.send(discord.Object(id=GUILDCHAT_ID), line, tts=False)

                # guild chat - send to discord
                if ('Your guildmate') in line:
                    await client.send(discord.Object(id=GUILDCHAT_ID), line, tts=False)
            # end outer if

# run logfile loop
client.loop.create_task(logfile_loop())

# run the bot using the TOKEN defined in Config.py
client.run(TOKEN)
