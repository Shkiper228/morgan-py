import discord
from discord.ext import commands
import datetime
import math
from random import randint
import sqlite3
from datetime import datetime, tzinfo, timedelta
from tzlocal import get_localzone
import pytz
from config import config, channels, reminders
from discord.utils import get
import asyncio





class User(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.Cog.listener()

	async def on_ready(self):
		while True:

			channel = self.client.get_channel(channels['test'])

			tz = pytz.timezone('Europe/Kiev')
			current_datetime = datetime.now(tz)
			current_wday = current_datetime.weekday
			current_day = current_datetime.day
			current_month = current_datetime.month
			current_year = current_datetime.year

			current_minute = current_datetime.minute
			current_hour = current_datetime.hour

			i = 0
			print(f'Кількість записів {len(reminders)}')
			while i < len(reminders):
				record = reminders[i]
				print(record)

				if record['date'] != None:
					print(record['date'])
					date = datetime.strptime(record['date'], '%d.%m.%Y')

					year = date.year
					month = date.month
					day = date.day

					if current_month == month and current_day == day:
						if record['time'] != None:

							time = datetime.strptime(record['time'], '%H:%M')

							hour = time.hour
							minute = time.minute
							print(current_minute)
							print(minute)
	
							if current_hour == hour and current_minute == minute:
								await channel.send(record['alert'])

				else:
					if record['time'] != None:
						time = datetime.strptime(record['time'], '%H:%M')

						hour = time.hour
						minute = time.minute

						if current_hour == hour and current_minute == minute:
							await channel.send(record['alert'])

							
					print('У записі немає дати')


				i = i + 1

			await asyncio.sleep(60)



	@commands.command()
	
	async def timer(self, ctx, time = 60):
		await ctx.message.channel.send(f'Принято. За {time} секунд спрацює таймер!')
		await asyncio.sleep(time)
		await ctx.message.channel.send(f'{ctx.message.author.mention} Таймер завершився!')


def setup(client):
	client.add_cog(User(client))