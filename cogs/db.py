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

	@commands.Cog.listener()
	
	async def on_ready(self):
		connection = sqlite3.connect('Morgan.db')
		cursor = connection.cursor()

		cursor.execute(CREATE TABLE IF NOT EXISTS users (
				name TEXT,
				id INT,
				lvl INT,
				guild TEXT
			))

		for guild in self.client.guilds:
			for member in guild.members:
				member_name = str(member)
				if  member_name.find("\'") != -1:
					index = member_name.find("\'")
					print(index)
					member_name = member_name[0:index] + "''" + member_name[index+1:len(member_name)]		
				if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
					cursor.execute(f"INSERT INTO users VALUES('{member_name}', {member.id}, 0, 1)")
					connection.commit()
				else:
					pass



def setup(client):
	client.add_cog(User(client))