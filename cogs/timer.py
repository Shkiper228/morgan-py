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
	
	async def timer(self, ctx, time = 60):
		await ctx.message.channel.send(f'Принято. За {time} секунд спрацює таймер!')
		await asyncio.sleep(time)
		await ctx.message.channel.send(f'{ctx.message.author.mention} Таймер завершився!')


def setup(client):
	client.add_cog(User(client))