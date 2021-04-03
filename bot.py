import discord
from discord.ext import commands
import datetime
from random import randint
import sqlite3
from threading import Thread
from datetime import datetime
from datetime import date
from time import sleep
from discord.utils import get
from config import config
from config import channels

import os

client = commands.Bot( command_prefix = config['prefix'], intents = discord.Intents.all())

#connection = sqlite3.connect('server.db')
#cursor = connection.cursor()

#індикація запуску

"""
	cursor.execute(CREATE TABLE IF NOT EXISTS users (
		name TEXT,
		id INT,
		cash BIGINT,
		lvl INT
		))
	
	connection.commit()
	for guild in client.guilds:
		for member in guild.members:
			member_name = str(member)
			if  member_name.find("\'") != -1:
				index = member_name.find("\'")
				print(index)
				member_name = member_name[0:index] + "''" + member_name[index+1:len(member_name)]		
			if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
				cursor.execute(f"INSERT INTO users VALUES('{member_name}', {member.id}, 0, 1)")
				connection.commit()
			else:
				pass


	
	db = sqlite3.connect('morgan.db')
	sql = db.cursor()

	sql.execute()
"""





@client.command(pass_context = True)
#команда для виводу часу по GMT+2
async def time (ctx):
	current_datetime = datetime.now()
	time = f'{current_datetime.hour + 2} : {current_datetime.minute} : {current_datetime.second}'
	await ctx.send(embed = discord.Embed(description = f'{ctx.message.author.mention} дійсний час по GMT +2 --> {time}', color = 0x4D4D4D))

@client.command(pass_context = True)
#команда для гри в камінь-нодиці-папір
async def ssp (ctx, course = None):
	user = ctx.message.author

	course_index = None
	course_list = ['камінь', 'ножиці', 'папір']
	course_bot = random.randint(0, 2)
	
	for index, x in enumerate(course_list):
		if course == x:
			course_index = index
			break
	if course == None:
		await ctx.send(embed = discord.Embed(description = f'{user.mention} Це команда для гри в камінь-ножиці-папір!\nНапишіть в чат команду "$ssp" і назву дії(камінь, ножиці, папір).\nНаприклад: $ssp камінь', color = 0x4D4D4D))
	elif course_index != None:
		if course_index == course_bot:
			await ctx.send(embed = discord.Embed(description = f'{user.mention} {course_list[course_bot]}\nНічия!', color = 0x4D4D4D))
		elif course_index - course_bot == 1 or course_index - course_bot == -2:
			await ctx.send(embed = discord.Embed(description = f'{user.mention} {course_list[course_bot]}\nПеремога бота!', color = 0x4D4D4D))
		elif course_bot - course_index == 1 or course_bot - course_index == -2:
			await ctx.send(embed = discord.Embed(description = f'{user.mention} {course_list[course_bot]}\nПереміг {user.display_name}!', color = 0x4D4D4D))
	else:
		await ctx.send(f'{user.mention} Назва ходу була введена неправильно!!!')

@client.command(pass_context = True)
#команда для видалення багатьох повідомлень в даному текстовому каналі
async def clear(ctx, count = 0):
	permissions = False
	user = ctx.message.author
	author_roles = user.roles
	for role in author_roles:
		if str(role) == 'leader' or str(role) == 'admin' or str(role) == 'guard':
			permissions = True
			break

	if permissions == True:
		await ctx.channel.purge(limit = count + 1)
	else:
		await ctx.channel.send(f'_{user.mention}, у вас немає ролей, які дозволяють виконувати цю команду!_')

@client.command(pass_context = True)
#команда для приєднання бота до голосового каналу
async def join(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else: 
		voice = await channel.connect()

@client.command(pass_context = True)
#команда для від'єднання бота від голосового каналу
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.disconnect()
	else: 
		voice = await channel.connect()

@client.command(pass_context = True)
#команда виводу загальної публічної інформації сервера
async def info(ctx):

	guild = ctx.message.guild

	server_created = guild.created_at.strftime('%d.%m.%y %H:%M:%S')
	server_created_datetime = guild.created_at


	await ctx.send(embed = discord.Embed(
		description = (f'Сервер було створено: {server_created}\n Творець сервера: {guild.owner.display_name}'), 
		title = 'ЗАГАЛЬНА ІНФОРМАЦІЯ ПРО СЕРВЕР', 
		color = 0x4D4D4D))
	
@client.command(pass_context = True)
#команда для остримання безкінечного посилання на сервер
async def link(ctx):
	link = 'https://discord.gg/9CAQe3aW8P'
	await ctx.send(f'{ctx.message.author.mention} лови посилання на сервер! {link}')

@client.command(pass_context = True)

async def event(ctx, action=None):
	permissions = False
	user = ctx.message.author
	author_roles = user.roles
	for role in author_roles:
		if str(role) == 'leader' or str(role) == 'admin' or str(role) == 'guard': 
			permissions = True
			break
	current_datetime = datetime.now()
	channel = client.get_channel(720915216174415963)
	if action == 'start':
		if current_datetime.weekday() == 4 or current_datetime.weekday() == 6:
			await channel.send(f'@everyone  Івент розпочався')
			for member in client.get_all_members():
				for role in member.roles:
					if str(role) == 'leader' or str(role) == 'admin' or str(role) == 'guard':
						await member.send('Івент щойно розпочався. Приєднуйся до нас!')
		else:
			await ctx.send(f'{user.mention} Сьогодні немає івенту!')
	elif action == 'notif':
		if current_datetime.weekday() == 4:
			await channel.send(f'@everyone Сьогодні о 18:30  по Києву буде івент!')
		elif current_datetime.weekday() == 6:
			await channel.send(f'@everyone Сьогодні о 16:30  по Києву буде івент!')
		else:
			await ctx.send(f'{user.mention} Сьогодні немає івенту!')


@client.command(pass_context = True)

async def ban(ctx, target: discord.Member):
	for role in ctx.author.roles:
		if str(role) == 'leader':
			await target.ban()


@client.command(pass_context = True)

async def unban(ctx, target: discord.Member):
	for role in ctx.author.roles:
		if str(role) == 'leader':
			await target.unban()


@client.command(pass_context = True)

async def kick(ctx, target: discord.Member):
	for role in ctx.author.roles:
		if str(role) == 'leader':
			await target.kick()
			
"""			
@client.event

async def on_message(message):
	banRoles = ['bot']
	from config import helloWords
	msg = message.content.lower()
	permission = True


	if msg in helloWords:
		for role in message.author.roles:
			if str(role) in banRoles:
				permission = False

		if permission:
			await message.channel.send(f'{helloWords[random.randint(0, len(helloWords) - 1)]}')


	if randint(0, 100) >= 95:
		await message.add_reaction('😀')
"""

@client.command()
async def load(ctx, extension):
	if ctx.author.id == 506215900836265995:
		client.load_extension(f'cogs.{extension}')
		await ctx.send('Success load!')
	else:
		await ctx.send('Ви не розробник!')

@client.command()
async def unload(ctx, extension):
	if ctx.author.id == 506215900836265995:
		client.unload_extension(f'cogs.{extension}')
		await ctx.send('Success load!')
	else:
		await ctx.send('Ви не розробник!')	

@client.command()
async def reload(ctx, extension):
	if ctx.author.id == 506215900836265995:
		client.unload_extension(f'cogs.{extension}')
		client.load_extension(f'cogs.{extension}')
		await ctx.send('Success load!')
	else:
		await ctx.send('Ви не розробник!')

for filename in os.listdir('./cogs'):
	if filename.endswith(".py"):
		client.load_extension(f'cogs.{filename[:-3]}')		

#токен
token = open ('token.txt', 'r').readline()
client.run(token)