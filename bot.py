import asyncio
import random
from discord import Game
from discord.ext.commands import Bot
from requests import get

BOT_PREFIX = "lt!"
TOKEN = open('token').read().strip("\n")

client = Bot(command_prefix=BOT_PREFIX)

resp = get("http://talvieno.com/Taiya/uploaded.txt")
quotes = resp.content.decode('utf-8').split('\n')[:-1]
quoteslst = []
for quote in quotes:
    quoteslst.append(quote[quote.find(": ") + 2:])

@client.command(pass_context=True)
async def get(context):
    await client.say("```" + quoteslst[int(context.message.content.split('lt!get ')[1])] + "```")

@client.command()
async def getrandom():
    choice = random.randint(0, len(quoteslst) - 1)
    await client.say("```" + quoteslst[choice] + " (" + str(choice) + ")```")
    
@client.command()
async def getlast():
	await client.say("```" + quoteslst[-1] + "```") #https://stackoverflow.com/questions/930397/getting-the-last-element-of-a-list-in-python
	quoteslst = update(lst)
	
@client.command(pass_context=True)
async def search(context):
    words = context.message.content.split('lt!search ', 1)[1].split()
    searched = []
    for quote in quoteslst:
        for word in words:
            if word in quote:
                searched.append(quote)
    choice = random.choice(searched)
    await client.say("```" + choice + " (" + str(quoteslst.index(choice)) + ")```")

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_servers())
client.run(TOKEN)
