import discord
from discord.ext import commands
import datetime
import math
from random import randint
import sqlite3
from datetime import datetime, tzinfo, timedelta
from tzlocal import get_localzone
import pytz
from config import config, channels




class User(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.command(aliases=['час'])
	#команда для виводу часу по GMT+2
	async def time (self, ctx):
		tz = pytz.timezone('Europe/Kiev')
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

	async def event(self, ctx, action=None):
		permissions = False
		user = ctx.message.author
		author_roles = user.roles
		for role in author_roles:
			if str(role) == 'leader' or str(role) == 'admin' or str(role) == 'guard': 
				permissions = True
				break
		tz = pytz.timezone('Europe/Kiev')
		current_datetime = datetime.now(tz)
		channel = self.client.get_channel(720915216174415963)
		if action == 'start':
			if current_datetime.weekday() == 4 or current_datetime.weekday() == 6:
				await channel.send(f'@everyone  Івент розпочався')
				for member in self.client.get_all_members():
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


	@commands.command()
	
	async def mafia(self, ctx, arg1 = None, arg2 = None, arg3 = None):
		if arg1 == 'game':
			if arg2 == 'calculation' or arg2 == 'make':
				if arg3 == None:
					await ctx.message.channel.send(f'{ctx.message.author.mention} вкажіть кількість гравців без ведучого')
				elif int(arg3) % 1 != 0:
					await ctx.message.channel.send(f'{ctx.message.author.mention} вкажіть кількість гравців цілим цислом!')
				elif int(arg3) < 5:
					await ctx.message.channel.send(f'{ctx.message.author.mention} потрібно більше гравців!')
				else:
					from config import mafia
					players = dict(
						count = int(arg3),
						mafias = None,
						sherifs = None,
						doctors = None,
						pytanas = None,
						civils = None
						)
	
					#calculation counts for roles
					players['mafias'] = math.floor(players['count'] / mafia['minPlayers']['mafia'])
					mafias = players['mafias']
					players['sherifs'] = math.floor(players['count'] / mafia['minPlayers']['sherif'])
					sherifs = players['sherifs']
					players['doctors'] = math.floor(players['count'] / mafia['minPlayers']['doctor'])
					doctors = players['doctors']
					players['pytanas'] = math.floor(players['count'] / mafia['minPlayers']['pytana'])
					pytanas = players['pytanas']
					players['civils'] = players['count'] - mafias - sherifs - doctors - pytanas
					civils = players['civils']

					await ctx.message.author.send(f'Кількість мафії: {mafias} Кількість шерифів: {sherifs} Кількість лікарів: {doctors} Кількість повій: {pytanas} Кількість мирних: {civils}')
					if arg2 == 'make':
						if ctx.message.author.voice != None:
							print(ctx.message.author.voice)
							await ctx.message.channel.send(f'{ctx.message.author.mention}')
						else:
							await ctx.message.channel.send(f'{ctx.message.author.mention} для облаштування гри потрібно, аби ви були в голосовому каналі')





		
			
				
				
		


def setup(client):
	client.add_cog(User(client))