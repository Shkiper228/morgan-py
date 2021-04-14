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




class User(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	
	async def mafia(self, ctx, action = None, count = None, guiding = None):

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


			await author.send(embed = discord.Embed(description= f'Ряд випадкових чисел {random_numbers}\n Розшифрування ролей {sequence_role}'))
			print(f'Кількість гравців {count_role}')
			print(f'Ряд випадкових чисел {random_numbers}')
			print(f'Розшифрування ролей {sequence_role}')



		elif action == 'make':
			print(action)
		else:
			await channel.send(embed = discord.Embed(description = f'{mention} Такої дії не існує! \n Можливі дії: calculation(не робоча) і make(теж неробоча)', color = 0x4D4D4D))




			"""
			if arg2 == 'calculation' or arg2 == 'make':
				if arg3 == None:
					await ctx.message.channel.send(f'{ctx.message.author.mention} вкажіть кількість гравців без ведучого')
				elif int(arg3) % 1 != 0:
					await ctx.message.channel.send(f'{ctx.message.author.mention} вкажіть кількість гравців цілим цислом!')
				elif int(arg3) < 5:
					await ctx.message.channel.send(f'{ctx.message.author.mention} потрібно більше гравців!')
				else:
					from config import mafia
					players_count = int(arg3)
					count_role = [0,0,0,0,0]
					#calculation counts for roles
					total_count = 0
					r = 0
					while r < len(mafia['sequence']):
						if mafia['sequence'][r] != 'civils':
							count_role[r] = math.floor(players_count / mafia['minPlayers'][r])
							count_withoutCivils = total_count + count_role
						else:
							count_role[r] = players_count - count_withoutCivils
							
							
						print(str(players[r]) + str(mafia['sequence'][r]))
						r = r + 1
					
					channel = ctx.message.author.voice.channel
						
					print(len(channel.members))
					if channel != None:
						if len(channel.members) - 1 >= players_count:
							guiding = ctx.message.guild.get_member_named(arg4)
							if arg4 == None:
								guiding = ctx.message.author

							print('Ведучий ' + str(guiding))

							numbers = []

							m = 0
							while m < players_count:
								member = channel.members[m]
								if member != guiding and member != ctx.message.guild.owner and member.bot != True:
									nick = str(m) + ' ' + member.display_name
									await member.edit(nick = nick)
									print(member.display_name)
								elif member == ctx.message.guild.owner:
									await member.send('Добавте на початку свого нік-нейма будь-ласка, число ' + str(m))
								m = m + 1


							i = 0
							print(f'кількість людей в голосовому {len(channel.members)}')
							while i < players_count:
								n = randint(1, players_count)
								j = 0
								perm = True
								while j < i:
									if n == numbers[j]:
										perm = False
									j = j + 1
								if perm:
									i = i + 1
									numbers.append(n)
								else:
									continue

							print('Випадковий ряд чисел ' + str(numbers))
								
							code = [
								[],
								[],
								[],
								[],
								[]
								]

							n = 1
							i = 0
							while i < len(players):
								j = 0
								while j < players[i]:
									code[i].append(n)
									n = n + 1
									j = j + 1
								i = i + 1
									
							print('Шифр ролей' + str(code))
								






								
							m = 0
							i = 0
							string = ''
							while i < players_count:
								player_member = channel.members[m]
								player_numeric = numbers[i]
								if player_member == guiding:
									m = m + 1
									continue

								a = 0
								while a < len(code):
									j = 0
									while j < len(code[a]):
										if code[a][j] == player_numeric:
											string = string + f"{player_member} - {mafia['sequence'][a]}" + "\n"
										j = j + 1
									a = a + 1
								m = m + 1
								i = i + 1 
							print(string)
							await guiding.send(string)
									



						else:
							await ctx.message.channel.send(f'{ctx.message.author.mention} вас мало')
					else:
						await ctx.message.channel.send(f'{ctx.message.author.mention} для облаштування гри потрібно, аби ви були в голосовому каналі')
	"""




def setup(client):
	client.add_cog(User(client))