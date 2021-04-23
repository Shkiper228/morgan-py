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


cross_zero_numbers = [[None, None, None], [None, None, None], [None, None, None]]

class User(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ['cn', 'tictactoe', 'ttt', 'tic-tac-toe', 'cz', 'cross-zero', 'crosszero'])
	
	async def __tic_tac_toe(self, ctx, x = 1, y = 1):
		string = ''

		if cross_zero_numbers[x-1][y-1] == None:
			cross_zero_numbers[x-1][y-1] = 'X' 

		v = 0
		while v < 3:
			h = 0
			while h < 3:
				string = string + str(cross_zero_numbers[v][h]) + '\t'
				h = h + 1

			string = string + str('\n')
			v = v + 1

		await ctx.message.channel.send(string)




def setup(client):
	client.add_cog(User(client))