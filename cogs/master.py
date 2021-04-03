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

class User(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.Cog.listener()
	async def on_ready(self):
			print('Connect success!!!')
			channel = self.client.get_channel(704660113750884433)
			await channel.send('Успішний запуск')


	@commands.Cog.listener()
	#сповіщення про нового учасника сервера
	async def on_member_join(self, member ):
		channel = self.client.get_channel(704690682920697875)
		role = discord.utils.get(member.guild.roles, id = 704691487857704980)
		await member.add_roles( role )
		await channel.send(embed = discord.Embed(description = f'{member.display_name} приєднався до нас!', color = 0x4D4D4D))

	@commands.Cog.listener()
	#сповіщення про вихід учасника сервера
	async def on_member_remove(self,  member ):
			channel = self.client.get_channel(704660113750884433)
			await channel.send(embed = discord.Embed(description = f'``{member.display_name}`` покинув нас!', color = 0x4D4D4D))	




	@commands.Cog.listener()

	async def on_message(self, message):
		banRoles = ['bot']
		from config import helloWords
		msg = message.content.lower()
		permission = True
	
		for role in message.author.roles:
			if str(role) in banRoles:
				permission = False

		if permission:
			if msg in helloWords:
				await message.channel.send(f'{helloWords[randint(0, len(helloWords) - 1)]}')
			if randint(0, 100) <= 10:
				await message.add_reaction('😀')




	@commands.command(aliases=['час'])
	#команда для виводу часу по GMT+2
	async def time (self, ctx):
		current_datetime = datetime.now()
		time = f'{current_datetime.hour + 2} : {current_datetime.minute} : {current_datetime.second}'
		await ctx.send(embed = discord.Embed(description = f'{ctx.message.author.mention} дійсний час по GMT +2 --> {time}', color = 0x4D4D4D))

	@commands.command()
	#команда виводу загальної публічної інформації сервера
	async def info(self, ctx):

		guild = ctx.message.guild

		server_created = guild.created_at.strftime('%d.%m.%y %H:%M:%S')
		server_created_datetime = guild.created_at


		await ctx.send(embed = discord.Embed(
			description = (f'Сервер було створено: {server_created}\n Творець сервера: {guild.owner.display_name}'), 
			title = 'ЗАГАЛЬНА ІНФОРМАЦІЯ ПРО СЕРВЕР', 
			color = 0x4D4D4D))
			
				
				
		


def setup(client):
	client.add_cog(User(client))