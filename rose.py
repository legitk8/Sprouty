import discord, os, asyncio, requests, json, random
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
					line = line[:-1]
					dict[line]=[]
					author=line
					continue
				temp_list=line.split(':')
				if temp_list[2][-1] == '\n':
					temp_list[2] = temp_list[2][:-1]
				dict[author].append(WorkEntry(int(temp_list[0]),temp_list[1],int(temp_list[2])))
	except Exception as e:
		print(e)

# @bot.event
# async def on_command_error(message, error):
# 	if isinstance(error, commands.BadArgument):
# 		await message.channel.send('Please enter again with the right arugements')
# 	if isinstance(error, commands.CommandNotFound):
# 		await message.channel.send('Command not found')

@bot.command()
async def ping(message):
	await message.channel.send(f'My ping is {round(bot.latency*1000)}ms')

@bot.command()
async def prt(message):
	author=str(message.author)
	await message.channel.send(f"Task list of {message.author.mention}:")
	await message.channel.send(printX(dict[author]))


@bot.command()
async def todo(message, work: str='Generic', work_time: int=10):
	author=str(message.author)
	if author in dict:
		todolistx=dict[author]
	else:
		todolistx=[]
		dict[author]=todolistx
	todolistx.append(WorkEntry(len(todolistx)+1, work,work_time))
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
	if task_num > 0:
		author=str(message.author)
		del dict[author][task_num-1]
		for i in range(task_num-1,len(dict[author])):
			dict[author][i].tasknum-=1

		await message.channel.send(f'Done task {task_num}\n')

		try:
			with open('config.txt', 'w') as f:
				for i in dict:
					f.write(str(i)+'\n')
					for j in dict[i]:
						f.write(f'{j.tasknum}:{j.taskname}:{j.tasktime}\n')
		except Exception as e:
			print(e)
	else:
		await message.channel.send('Please enter the right task number')

@bot.command(aliases=['start'])
async def doing(message, task_num: int):
	if task_num > 0:
		author=str(message.author)
		time = dict[author][task_num-1].tasktime

		await asyncio.sleep(time)*60
		await message.channel.send(f'Congratz,{message.author.mention} your task is done')

		quote = get_quotes()
		await message.channel.send(quote)

		await done(message, task_num)
	else:
		await message.channel.send('Please enter the right task number')

#loop which asks the users for input, checks user's input and prints board after updating it
@bot.command()
async def battleship(message,ship_size=3, dimension=5):
	author=message.author
	channel = message.channel
	mygame=""
	SHIP_SIZE=ship_size
	DIMENSION=dimension
	board=[]
	boardx=[]

	#initialising our board with appropriate row and column names

	for i in range(DIMENSION+1):
		board_row=[]
		for j in range(DIMENSION+1):
			if j==0:
				if i==0:
					board_row.append(" ")
				else:
					board_row.append(i-1)
			elif i==0:
				board_row.append(chr(ord('A')+j-1))
			else:
				board_row.append(" ")
		board.append(board_row)

	#initialising another board where the info of our ship will be stored

	for i in range(DIMENSION+1):
		board_rowx=[]
		for j in range(DIMENSION+1):
			if j==0:
				if i==0:
					board_rowx.append(" ")
				else:
					board_rowx.append(i-1)
			elif i==0:
				board_rowx.append(chr(ord('A')+j-1))
			else:
				board_rowx.append(" ")
		boardx.append(board_rowx)

	#printing our board for the first time, this is the first thing shown when our program is executed
	mygame+= "\n"+ " "*(DIMENSION+1)+"Welcome to Battleship!\n\n"
	for i in range(DIMENSION+1):
		for j in range(DIMENSION+1):
			if i==0:
				mygame+=str(board[i][j])+"   "
			else:
				mygame+=str(board[i][j])+" | "
		mygame+="\n"
		mygame+="  +"+"---+"*DIMENSION+"\n"

	#computer assigns coordinates for the location of our ship using a random function

	x=random.randint(0,1)
	if x==1:
		y=random.randint(1,DIMENSION)
		z=random.randint(1,DIMENSION-SHIP_SIZE+1)
		for i in range(SHIP_SIZE):
				boardx[y][z+i]='*'
	else:
		y=random.randint(1,DIMENSION-SHIP_SIZE+1)
		z=random.randint(1,DIMENSION)
		for i in range(SHIP_SIZE):
			boardx[y+i][z]="*"

	continue_game=0
	cnt=0            #for counting the total number of tries taken (only unique attempts and attempts with valid inputs are counted)
	strike=0         #counts the total number of correct strikes on ship

	while(continue_game==0):
		mygame=""
		await message.channel.send("\n  Guess the coordinates of the hidden ship (eg.rose game A6):  ")

		def check(m):
			return (channel == m.channel) and (author == m.author)
		try:
			game_input = await bot.wait_for('message', check=check, timeout=20)
		except asyncio.TimeoutError:
			await channel.send('Timed Out')
		else:
			guess=list(game_input.content)
			if len(guess)==2 and ord('A')-1<ord(guess[0])<ord('A')+DIMENSION and guess[1].isdigit() and 0<=int(guess[1])<DIMENSION:
				row_coordinate= int(guess[1])+1
				col_coordinate= ord(guess[0])- ord('A') + 1
				if board[row_coordinate][col_coordinate]=="X" or board[row_coordinate][col_coordinate]=="#":
					mygame+="  This coordinate has been tried previously. Please try again"+"\n"
					continue;
				if boardx[row_coordinate][col_coordinate]=='*':
					strike=strike+1
					board[row_coordinate][col_coordinate]='X'
				else:
					board[row_coordinate][col_coordinate]='#'
			else:
				mygame+="  Invalid input, please enter the desired coordinate properly"+"\n"
				continue;

			for i in range(DIMENSION+1):
				for j in range(DIMENSION+1):
					if i==0:
						mygame+=str(board[i][j])+"   "
					else:
						mygame+=str(board[i][j])+" | "
				mygame+="\n"
				mygame+="  +"+"---+"*DIMENSION+"\n"

			cnt=cnt+1
			if strike==SHIP_SIZE:
				continue_game=1
				mygame+="\n  Congratulations! You Won!\n""  You took "+str(cnt)+" turns to finish the game."+"\n"
			await message.channel.send(f'```{mygame}```')





load_dotenv()
TOKEN = os.getenv('TOKEN')

bot.run(TOKEN)
