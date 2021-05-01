import discord, os, asyncio
from dotenv import load_dotenv
from discord.ext import commands

bot = commands.Bot(command_prefix=['rose ', 'Rose '])

class WorkEntry:
    def __init__(self,num,name,time):
        self.tasknum=num
        self.taskname=name
        self.tasktime=time

todolist=[]
s=""

@bot.event
async def on_ready():
    print('Logged in as {0.user.name} ID: {0.user.id}'.format(bot))

    activity = discord.Game(name='Rose', type=0)
    await bot.change_presence(activity=activity)

@bot.command()
async def ping(message):
    await message.channel.send(f'My ping is {round(bot.latency*1000)}ms')

@bot.command()
async def prt(message):
    for i in todolist:
        print(i.taskname)


@bot.command()
async def todo(message, work: str='', work_time: int=45):
    todolist.append(WorkEntry(len(todolist)+1, work,work_time))
    await message.channel.send(f'work: {work}\ntime: {work_time}')
    author = message.author

#wrting in txt file
    try:
        with open('config.txt', 'a') as f:
            f.write(f'{author}:{work}:{work_time}\n')
    except Exception as e:
        print(e)

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot.run(TOKEN)
