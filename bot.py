import discord
from discord.ext import commands
import datetime
from random import randint
import sqlite3
from datetime import datetime, tzinfo, timedelta
from tzlocal import get_localzone
import pytz
from config import config, channels
from discord.utils import get
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
#команда для приєднання бота до голосового каналу
async def join(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)
	print(voice)

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