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
	
	async def mafia(self, ctx, arg1 = None, arg2 = None, arg3 = None, arg4 = None):
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
					players_count = int(arg3)
					players = [0,0,0,0,0]
					#calculation counts for roles
					i = 0
					while i < len(mafia['sequence']):
						if mafia['sequence'][i] != 'civils':
							players[i] = math.floor(players_count / mafia['minPlayers'][i])
						else:
							civils = players_count
							for count in players:
								civils = civils - count
							players[i] = civils
							
							
						print(str(players[i]) + str(mafia['sequence'][i]))
						i = i + 1
					
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
								while m < players_count + 1:
									member = channel.members[m]
									if member != guiding and member != ctx.message.guild.owner:
										nick = str(m + 1) + ' ' + member.display_name
										await member.edit(nick = nick)
										print(member.display_name)
									elif member == ctx.message.guild.owner:
										await ctx.message.guild.owner.send('Добавте на початку свого нік-нейма будь-ласка, число ' + str(m + 1))

									
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





def setup(client):
	client.add_cog(User(client))