import discord
from discord.ext import commands
import datetime
from random import randint
import sqlite3
from datetime import datetime, tzinfo, timedelta
from tzlocal import get_localzone
import pytz
from config import config, channels

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.author = 506215900836265995


	@commands.Cog.listener()
	async def on_ready(self):
		print('Connect success!!!')
		channel = self.client.get_channel(channels['test'])
		#await channel.send('Успішний запуск')


	@commands.Cog.listener()
	#сповіщення про нового учасника сервера
	async def on_member_join(self, member ):
		channel = self.client.get_channel(704690682920697875)
		role = discord.utils.get(member.guild.roles, id = 704691487857704980)
		await member.add_roles( role )
		await channel.send(embed = discord.Embed(description = f'{member.display_name} приєднався до нас!', color = 0x4D4D4D))

	@commands.Cog.listener()
	#сповіщення про вихід учасника сервера
	async def on_member_remove(self,  member ):
		channel = self.client.get_channel(704660113750884433)
		await channel.send(embed = discord.Embed(description = f'``{member.display_name}`` покинув нас!', color = 0x4D4D4D))	




	@commands.Cog.listener()

	async def on_message(self, message):
		print(f'[{message.author}] {message.content}')
		banRoles = ['bot']
		from config import helloWords
		msg = message.content.lower()
		permission = True

		
		if message.author.bot != True:
			for role in message.author.roles:
				if str(role) in banRoles:
					permission = False
	
			if permission:
				if msg in helloWords:
					await message.channel.send(f'{helloWords[randint(0, len(helloWords) - 1)]}')
				if randint(0, 100) <= 2:
					emojis = message.guild.emojis
					emoji = emojis[randint(0, len(emojis) - 1)]
					await message.add_reaction(emoji)


				if msg.find('https://discord.gg/') != -1 and msg.find('https://discord.gg/9caqe3aw8p') == -1:
					print(msg.find('https://discord.gg/9caqe3aw8p'))
					print(msg)
					self.owner = message.guild.owner
					await self.owner.send(f'{message.author} Рекламував посторонній сервер діскорд на твоєму сервері. Краще заблокуй його у себе')
					await message.author.send(f'Тебе було автоматично забанено на ``{message.guild.name}`` за рекламу посторонніх діскорд серверів')
					await message.author.ban(reason = 'Реклама дс серверів', delete_message_days = 0)
					await message.channel.purge(limit = 1)

		


def setup(client):
	client.add_cog(User(client))