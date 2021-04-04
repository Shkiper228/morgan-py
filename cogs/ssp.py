import discord
from discord.ext import commands
import datetime
from random import randint
import sqlite3
from threading import Thread
from datetime import datetime
from datetime import date
from time import sleep
from discord.utils import get
from config import config
from config import channels

class User(commands.Cog):

	def __init__(self, client):
		self.client = client



	@commands.command()
	#команда для гри в камінь-нодиці-папір
	async def ssp (self, ctx, course = None):
		user = ctx.message.author

		course_index = None
		course_list = ['камінь', 'ножиці', 'папір']
		course_bot = randint(0, 2)
	
		for index, x in enumerate(course_list):
			if course == x:
				course_index = index
				break
		if course == None:
			await ctx.send(embed = discord.Embed(description = f'{user.mention} Це команда для гри в камінь-ножиці-папір!\nНапишіть в чат команду "$ssp" і назву дії(камінь, ножиці, папір).\nНаприклад: $ssp камінь', color = 0x4D4D4D))
		elif course_index != None:
			if course_index == course_bot:
				await ctx.send(embed = discord.Embed(description = f'{user.mention} {course_list[course_bot]}\nНічия!', color = 0x4D4D4D))
			elif course_index - course_bot == 1 or course_index - course_bot == -2:
				await ctx.send(embed = discord.Embed(description = f'{user.mention} {course_list[course_bot]}\nПеремога бота!', color = 0x4D4D4D))
			elif course_bot - course_index == 1 or course_bot - course_index == -2:
				await ctx.send(embed = discord.Embed(description = f'{user.mention} {course_list[course_bot]}\nПереміг {user.display_name}!', color = 0x4D4D4D))
		else:
			await ctx.send(f'{user.mention} Назва ходу була введена неправильно!!!')
					


def setup(client):
	client.add_cog(User(client))