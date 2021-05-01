import discord, os, asyncio, requests, json
from dotenv import load_dotenv
from discord.ext import commands

bot = commands.Bot(command_prefix=['rose ', 'Rose '])

dict = {}

def get_quotes():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' - ' + json_data[0]['a']
    return quote

def printX(todolist):
    s=""
    for i in todolist:
        s=s+'|'+str(i.tasknum)+':'+i.taskname+'-'+str(i.tasktime)+'|'+'\n'
    return s

class WorkEntry:
    def __init__(self,num,name,time):
        self.tasknum=num
        self.taskname=name
        self.tasktime=time

todolist=[]
#edit ho rha kya?
@bot.event
async def on_ready():
    print('Logged in as {0.user.name} ID: {0.user.id}'.format(bot))
    activity = discord.Game(name='Rose', type=0)
    await bot.change_presence(activity=activity)
    author=''
    try:
        with open('config.txt', 'r') as f:
            for line in f:
                if ':' not in line:
                    dict[line]=[]
                    author=line
                    continue
                temp_list=line.split(':')
                if temp_list[2][-1] == '\n':
                    temp_list[2] = temp_list[2][:-1]
                dict[author].append(WorkEntry(int(temp_list[0]),temp_list[1],int(temp_list[2])))
    except Exception as e:
        print(e)

@bot.command()
async def ping(message):
    await message.channel.send(f'My ping is {round(bot.latency*1000)}ms')

@bot.command()
async def prt(message):
    author=message.author
    await message.channel.send("Current list of tasks is:")
    await message.channel.send(printX(dict[author]))


@bot.command()
async def todo(message, work: str='Generic', work_time: int=10):
    author = message.author
    if author in dict:
        todolistx=dict[author]
    else:
        todolistx=[]
        dict[author]=todolistx
    todolistx.append(WorkEntry(len(todolist)+1, work,work_time))
    await message.channel.send(f'work: {work}\ntime: {work_time}')

#wrting in txt file
    try:
        with open('config.txt', 'w') as f:
            for i in dict:
                f.write(str(i)+'\n')
                for j in dict[i]:
                    f.write(f'{j.tasknum}:{j.taskname}:{j.tasktime}\n')
    except Exception as e:
        print(e)

@bot.command(aliases=['del', 'rem'])
async def done(message, task_num: int):
    author=message.author
    del todolist[task_num-1]
    for i in range(task_num-1,len(dict[author])):
        dict[author][i].tasknum-=1

    await message.channel.send(f'Done task {task_num}\n')

    try:
        with open('config.txt', 'w') as f:
            for i in dict[author]:
                f.write(f'{i.tasknum}:{i.taskname}:{i.tasktime}\n')
    except Exception as e:
        print(e)

@bot.command(aliases=['start'])
async def doing(message, task_num: int):
    author=message.author
    time = dict[author][task_num-1].tasktime

    await asyncio.sleep(time)
    await message.channel.send(f'Congratz, your task is done')

    quote = get_quotes()
    await message.channel.send(quote)

    await done(message, task_num)

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot.run(TOKEN)
