import asyncio
import random
from discord import Game
from discord.ext.commands import Bot
from requests import get

BOT_PREFIX = "lt!"
TOKEN = open('token').read().strip("\n")

client = Bot(command_prefix=BOT_PREFIX)

quoteslst = []

def update(lst):
    resp = get("http://talvieno.com/Taiya/uploaded.txt")
    quotes = resp.content.decode('utf-8').split('\n')[:-1]
    ql = []
    for quote in quotes:
        ql.append(quote[quote.find(": ") + 2:])
    print("Quotes list updated. " + str(len(ql)) + " quotes found.")
    return ql

@client.command(pass_context=True)
async def get(context):
    quotedex = int(context.message.content.split('lt!get ')[1])
    if quotedex >= len(quoteslst):
        await client.say("Quote " + str(quotedex) + " does not exist.")
        quoteslst = update(lst)
        return
    await client.say("```" + quoteslst[quotedex] + " (" + str(quotedex) + ")```")
    quoteslst = update(lst)

@client.command()
async def getrandom():
    choice = random.randint(0, len(quoteslst) - 1)
    await client.say("```" + quoteslst[choice] + " (" + str(choice) + ")```")
    quoteslst = update(lst)

@client.command(pass_context=True)
async def search(context):
    words = context.message.content.split('lt!search ', 1)[1].split()
    searched = []
    for quote in quoteslst:
        for word in words:
            if word in quote:
                searched.append(quote)
    if not searched:
        await client.say("No quotes found with keyword(s) '" + " ".join(words) + "'.")
        quoteslst = update(lst)
        return
    choice = random.choice(searched)
    await client.say("```" + choice + " (" + str(quoteslst.index(choice)) + ")```")
    quoteslst = update(lst)

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)

async def list_servers():
    await client.wait_until_ready()
    quoteslst = update(lst)
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_servers())
client.run(TOKEN)