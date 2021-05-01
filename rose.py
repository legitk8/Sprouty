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

@bot.event
async def on_ready():
    print('Logged in as {0.user.name} ID: {0.user.id}'.format(bot))
    activity = discord.Game(name='Rose', type=0)
    await bot.change_presence(activity=activity)
    try:
        with open('config.txt', 'r') as f:
            for line in f:
                temp_list=line.split(':')
                if temp_list[2][-1] == '\n':
                    temp_list[2] = temp_list[2][:-1]
                todolist.append(WorkEntry(int(temp_list[0]),temp_list[1],int(temp_list[2])))
    except Exception as e:
        print(e)

@bot.command()
async def ping(message):
    await message.channel.send(f'My ping is {round(bot.latency*1000)}ms')

@bot.command()
async def prt(message):
    for i in todolist:
        await message.channel.send(f'{i.tasknum} {i.taskname} {i.tasktime}')


@bot.command()
async def todo(message, work: str='', work_time: int=45):
    todolist.append(WorkEntry(len(todolist)+1, work,work_time))
    await message.channel.send(f'work: {work}\ntime: {work_time}')
    author = message.author

#wrting in txt file
    try:
        with open('config.txt', 'w') as f:
            for i in todolist:
                f.write(f'{i.tasknum}:{i.taskname}:{i.tasktime}\n')
    except Exception as e:
        print(e)

@bot.command(aliases=['del', 'rem'])
async def done(message, task_num: int):
    del todolist[task_num-1]
    for i in range(task_num-1,len(todolist)):
        todolist[i].tasknum-=1

    await message.channel.send(f'Deleted task {task_num}\n')
    author = message.author

    try:
        with open('config.txt', 'w') as f:
            for i in todolist:
                f.write(f'{i.tasknum}:{i.taskname}:{i.tasktime}\n')
    except Exception as e:
        print(e)

@bot.command()
async def timer(message, timer: int=5):
    await asyncio.sleep(timer)
    await message.channel.send(f'{timer} secs are over')

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot.run(TOKEN)
