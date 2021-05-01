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


cross_zero_numbers = [['#', '#', '#'], ['#', '#', '#'], ['#', '#', '#']]
duelists = [None, None]

class User(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.command(aliases = ['tttcreate', 'tttadd'])
	
	async def __tic_tac_toe_create(self, ctx, duelist1=None, duelist2=None):
		guild = ctx.message.guild
		channel = ctx.message.channel


		duelists[0] = guild.get_member_named(duelist1)
		duelists[1] = guild.get_member_named(duelist2)	 

		print(duelists[0])
		print(duelists[1])
		print(cross_zero_numbers)

		cross_zero_numbers[0][0] = '#'
		cross_zero_numbers[0][1] = '#'
		cross_zero_numbers[0][2] = '#'
		cross_zero_numbers[1][0] = '#'
		cross_zero_numbers[1][1] = '#'
		cross_zero_numbers[1][2] = '#'
		cross_zero_numbers[2][0] = '#'
		cross_zero_numbers[2][1] = '#'
		cross_zero_numbers[2][2] = '#'

		if duelists[0] == None or duelists[1] == None:
			await channel.send(embed = discord.Embed(description = 'Гравці були введені неправильно'))
		else:
			await channel.send(embed = discord.Embed(description = f'Гру створено\n{duelists[0]} - X\n{duelists[1]} - O'))


	@commands.command(aliases = ['tttremove', 'tttdelete', 'tttdestroy'])

	async def __tic_tac_toe_delete(self, ctx):
		guild = ctx.message.guild
		channel = ctx.message.channel


		duelists[0] = None
		duelists[1] = None

		cross_zero_numbers = [['#', '#', '#'], ['#', '#', '#'], ['#', '#', '#']]

		print(cross_zero_numbers)
		await channel.send(embed = discord.Embed(description = 'Гру видалено'))




	@commands.command(aliases = ['cn', 'tictactoe', 'ttt', 'tic-tac-toe', 'cz', 'cross-zero', 'crosszero'])
	
	async def __tic_tac_toe(self, ctx, x=1, y=1):
		channel = ctx.message.channel
		author = ctx.message.author
		char = None

		if duelists[0] == None:
			await channel.send(embed = discord.Embed(description = f'Гра не розпочата. Щоб розпочати гру введіть команду $tttcreate [гравець1] [гравець2]'))
			return

		if author == duelists[0]:
			char = 'X'
		elif author == duelists[1]:
			char = 'O'
		else:
			await channel.send(embed = discord.Embed(description = f'{author.mention} ти не учасник гри'))
			return


		string = ' * -----------> x\n'

		if cross_zero_numbers[y-1][x-1] == '#':
			cross_zero_numbers[y-1][x-1] = char
		elif cross_zero_numbers[y-1][x-1] != '#':
			await channel.send(embed = discord.Embed(description = f'{author.mention} ця клітинка уже зайнята'))
			return



		#matrix
		v = 0
		while v < 3:
			h = 0
			while h < 3:
				if h == 0:
					string = string + ' | '
				string = string + str(cross_zero_numbers[v][h]) + '\t'
				h = h + 1


			string = string + str('\n')
			v = v + 1



		print(cross_zero_numbers)
		await ctx.message.channel.send(f'{string}\\\/ y')




def setup(client):
	client.add_cog(User(client))