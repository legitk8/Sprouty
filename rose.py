import discord, os, asyncio
from dotenv import load_dotenv
from discord.ext import commands

bot = commands.Bot(command_prefix=['rose ', 'Rose '])

@bot.event
async def on_ready():
    print('Logged in as {0.user.name} ID: {0.user.id}'.format(bot))

    activity = discord.Game(name='Rose', type=0)
    await bot.change_presence(activity=activity)

@bot.command()
async def ping(message):
    await message.channel.send(f'My ping is {round(bot.latency*1000)}ms')

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot.run(TOKEN)
