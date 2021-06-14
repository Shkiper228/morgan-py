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
from discord.utils import get
import asyncio


#global
mafia_game = dict(
	isSet = False,
	players = [],
	category = None

	)

def mafia_unset():
	mafia_game = dict(
	isSet = False,
	players = [],
	category = None

	)

class User(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ['mafiatext'])
	
	async def __mafiatext(self, ctx, action = None, *typed_players):
		from config import mafia

		players_count = len(typed_players)
		count_per_role = []
		random_numbers = []
		sequence_role = []
		players = []
		channel = ctx.channel

		if action == 'create':
			"""
	
			ПРОВІРКА

			"""

			#провірка кількості
			if players_count < 5:
				await channel.send('Недостатня кількість гравців')
				return

			#провірка гравців
			i = 0
			while i < players_count: 
				players.append(ctx.message.guild.get_member(int(typed_players[i])))
				if players[i] == None:
					await channel.send(f'Неправильно введено нік гравця №{i + 1}')
					return
				print(f'Гравець номер {i + 1} {players[i].name}') 

				i = i + 1

			
			"""

			КІНЕЦЬ ПРОВІРКИ

			"""


			"""

			СТВОРЕННЯ І НАСТРОЙКА КАТЕГОРІЇ

			"""

			category = await ctx.message.guild.create_category('MAFIA')
			await category.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)

			i = 0
			while i < len(players):
				await category.set_permissions(players[i], send_messages=False, read_messages=True)

				persone_channel = await category.create_text_channel(str(players[i]))
				await persone_channel.set_permissions(players[i], send_messages=True, read_messages=True)
				i = i + 1


			await category.create_text_channel('main')

			print(category.changed_roles)






			total_count = 0
			m = 1
			i = 0
			while i < len(mafia['sequence']): # кількісь циклів = кількість ролей
				sequence_role.append([])
				if mafia['sequence'][i] != 'civils': # якщо роль не є мирним

					count_per_role.append(math.floor(players_count/mafia['minPlayers'][i]))
					total_count = total_count + count_per_role[i]

				else: # решта випадків

					count_per_role.append(players_count - total_count)

				j = 0
				while j < count_per_role[i]: # цикл для формування ключа ролей
					sequence_role[i].append(m)
					j = j + 1
					m = m + 1

				i = i + 1
			i = 0
			print(f'Ключ {sequence_role}')


			i = 0
			while i < players_count:

				number = randint(1, players_count)
				isUnique = True

				j = 0
				while j < len(random_numbers):

					if number == random_numbers[j]:
						isUnique = False

					j = j + 1

				if isUnique:
					random_numbers.append(number)
					i = i + 1

			print(f'рандомний числовий ряд {random_numbers}')


			m = 0 
			i = 0
			while i < len(mafia['sequence']):


				j = 0
				while j < len(sequence_role[i]):

					#player = ctx.message.guild.get_member(players[m])
					#print(player)

					#try:
						#await players[random_numbers[m] - 1].send(f'Ти ---> {mafia["sequence"][i]}')
					#except:
						#print(f'Гравцю {players[random_numbers[m] - 1].mention} не вдалось надіслати повідомлення!')
					
					j = j + 1
					m = m + 1

				i = i + 1

		elif action == 'delete' or action == 'remove':
			mafia_unset()




def setup(client):
	client.add_cog(User(client))