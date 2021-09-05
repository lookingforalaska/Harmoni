from discord.ext import commands
from discord import Message
from dotenv import load_dotenv
from os import getenv
import discord


description = '''Simple Bot to stream internet Radio.'''
intents = discord.Intents.default()
intents.members = True
extensions = ['cogs.music']
bot = commands.Bot(command_prefix='?', description=description, intents=intents)
for extension in extensions:
	bot.load_extension(extension)



@bot.event
async def on_ready():
    print("INFO".center(40,"="))
    print("Discord Version: ",discord.__version__)
    print('Logged in as ',end='')
    print(bot.user.name + ": " + str(bot.user.id))
    print("="*40)
    print("Connected to..")
    servers = list(bot.guilds)
    cnt = len(servers)
    for i in range(cnt):
        print(str(i) + " " + str(servers[i]) + " : " + str(servers[i].id))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='?help'))


def main():
	load_dotenv()
	bot.run(getenv("TOKEN"), bot=True, reconnect=True)
	

main()