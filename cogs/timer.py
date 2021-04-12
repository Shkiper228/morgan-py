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

			current_wday = current_datetime.weekday()
			print('День тижня:' + str(current_wday))
			current_day = current_datetime.day
			current_month = current_datetime.month
			current_year = current_datetime.year

			current_minute = current_datetime.minute
			current_hour = current_datetime.hour

			i = 0
			print(f'Кількість записів {len(reminders)}')
			while i < len(reminders):
				record = reminders[i]
				channel = self.client.get_channel(record['channel'])
				print(record)
				if record['everyone']:
					alert = f"@everyone {record['alert']}" 
				else:
					alert = record['alert']

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
							
							if record['wday'] != None:
								print(current_wday)
								print('День тижня запису' + str(record['wday']))
								if str(current_wday) == record['wday']:
									if current_hour == hour and current_minute == minute:
										await channel.send(alert)

							else:
								if current_hour == hour and current_minute == minute:
									await channel.send(alert)

				else:
					if record['time'] != None:
						time = datetime.strptime(record['time'], '%H:%M')

						hour = time.hour
						minute = time.minute
						if str(current_wday) == record['wday']:

							if current_hour == hour and current_minute == minute:
								await channel.send(alert)


					print('У записі немає дати')


				i = i + 1

			await asyncio.sleep(60)



	@commands.command()
	
	async def timer(self, ctx, time):
		print(time)


		if time == None:
			time = 60
			print(time)
		if time == 'bump':
			time = 4*60*60
			await ctx.message.channel.send(f'Принято. За {time} секунд спрацює таймер!')
			await asyncio.sleep(str(time))
			await ctx.message.channel.send(f'{ctx.message.author.mention} Таймер завершився!')
		else:
			await ctx.message.channel.send(f'Принято. За {time} секунд спрацює таймер!')
			await asyncio.sleep(str(time))
			await ctx.message.channel.send(f'{ctx.message.author.mention} Таймер завершився!')



def setup(client):
	client.add_cog(User(client))