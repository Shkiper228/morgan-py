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

	)

def mafia_unset():
	mafia_game = dict(
	isSet = False,
	players = [],

	)

class User(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ['mafia'])
	
	async def __mafia(self, ctx, action = None, count = None, guiding = None):

		#import
		from config import mafia

		#ініціалізація
		channel = ctx.message.channel
		author = ctx.message.author
		mention = author.mention
		try:
			players_count = int(count)

		except:
			await channel.send(embed = discord.Embed(description = f'{mention} Введіть коректну кількість гравців!', color = 0x4D4D4D))


		if players_count > 200:
			await channel.send(embed = discord.Embed(description = f'{mention} Введена кількість гравців занадто велика!', color = 0x4D4D4D))
			return



		if action == 'calculation':
			print(action)

			count_role = []
			random_numbers = []
			sequence_role = []


			total_count = 0

			s = 0
			r = 0
			m = 1
			while r < len(mafia['sequence']):
				sequence_role.append([])
				if mafia['sequence'][r] != 'civils':
					count_role.append(math.floor(players_count / mafia['minPlayers'][r]))
					total_count = total_count + count_role[r]

				else:
					count_role.append(players_count - total_count)


				j = 0
				while j < count_role[r]:
					sequence_role[r].append(m)
					j = j + 1
					m = m + 1

				r = r + 1


			m = 0
			while m < players_count:
				n = randint(1, players_count)
				perm = True

				j = 0
				while j < len(random_numbers):
					if n == random_numbers[j]:
						perm = False

					j = j + 1

				if perm:
					random_numbers.append(n)
				else:
					continue

				m = m + 1


			m = 0
			r = 0
			string = ''
			while r < len(mafia['sequence']):

				j = 0
				while j < len(sequence_role[r]):
					string = string + f'Гравець під номером {random_numbers[m]} є: {mafia["sequence"][r]}\n'
					j = j + 1
					m = m + 1

				r = r + 1


			string = string + f'Ряд випадкових чисел {random_numbers}\n Розшифрування ролей {sequence_role}'
			await author.send(embed = discord.Embed(description = string))
			print(f'Кількість гравців {count_role}')
			print(f'Ряд випадкових чисел {random_numbers}')
			print(f'Розшифрування ролей {sequence_role}')



		elif action == 'make':
			print(action)
		else:
			await channel.send(embed = discord.Embed(description = f'{mention} Такої дії не існує! \n Можливі дії: calculation(не робоча) і make(теж неробоча)', color = 0x4D4D4D))




def setup(client):
	client.add_cog(User(client))