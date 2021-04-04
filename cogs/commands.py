import discord
from discord.ext import commands
import datetime
from random import randint
import sqlite3
from threading import Thread
from datetime import datetime, tzinfo, timedelta
from tzlocal import get_localzone
from time import sleep
from discord.utils import get
from config import config, channels

class User(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.command(aliases=['час'])
	#команда для виводу часу по GMT+2
	async def time (self, ctx):
		tz = get_localzone()
		current_datetime = datetime.now(tz)

		time = f'{current_datetime.hour} : {current_datetime.minute} : {current_datetime.second}'
		await ctx.send(embed = discord.Embed(description = f'{ctx.message.author.mention} дійсний місцевий час --> {time}', color = 0x4D4D4D))

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


	@commands.command()
	#команда для видалення багатьох повідомлень в даному текстовому каналі
	async def clear(self, ctx, count = 0):
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


	@commands.command()
	#команда для остримання безкінечного посилання на сервер
	async def link(self, ctx):
		link = 'https://discord.gg/9CAQe3aW8P'
		await ctx.send(f'{ctx.message.author.mention} лови посилання на сервер! {link}')


	@commands.command()

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


	@commands.command()

	async def ban(self, ctx, target: discord.Member):
		for role in ctx.author.roles:
			if str(role) == 'leader':
				await target.ban()
	

	@commands.command()
	
	async def unban(self, ctx, target: discord.Member):
		for role in ctx.author.roles:
			if str(role) == 'leader':
				await target.unban()


	@commands.command()
	
	async def kick(self, ctx, target: discord.Member):
		for role in ctx.author.roles:
			if str(role) == 'leader':
				await target.kick()
			
				
				
		


def setup(client):
	client.add_cog(User(client))