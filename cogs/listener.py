import discord
from discord.ext import commands
import datetime
from random import randint
import sqlite3
from datetime import datetime, tzinfo, timedelta
from tzlocal import get_localzone
import pytz
from config import config, channels
from os import listdir
import asyncio

class User(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.author = 506215900836265995


	@commands.Cog.listener()
	async def on_ready(self):
		print('Connect success!!!')
		channel = self.client.get_channel(channels['test'])
		#await channel.send('Успішний запуск')



		channel = self.client.get_channel(channels['info'])
		#await channel.send(embed = discord.Embed(title = '1'))
		info_msg = await channel.fetch_message(843190334263787570)
		#old_msg = await channel.fetch_message(channel.last_message_id)
		#await old_msg.delete()
		info_count = len(listdir('info'))

		required_reactions = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']



		await info_msg.clear_reactions()
		
		r = 0
		while True:
			await info_msg.add_reaction(required_reactions[r])
			r = r + 1

			if r > info_count:
				break

		
		info_file = open('info/' + str(listdir('info')[0]), encoding = 'utf-8')
		info_str = info_file.readlines()

		embed = discord.Embed(title = str(listdir('info')[0])[0:-4])

		i = 0
		for line in info_str:
			i = i + 1
			embed.add_field(name=f'_-|{i}|-_', value = line)

		info_file.close()

		await info_msg.edit(embed = embed)


	@commands.Cog.listener()
	#сповіщення про нового учасника сервера
	async def on_member_join(self, member ):
		channel = self.client.get_channel(channels['new_users'])
		role = discord.utils.get(member.guild.roles, id = 704691487857704980)
		await member.add_roles( role )
		await channel.send(embed = discord.Embed(description = f'{member.display_name} приєднався до нас!', color = 0x4D4D4D))

	@commands.Cog.listener()
	#сповіщення про вихід учасника сервера
	async def on_member_remove(self,  member ):
		channel = self.client.get_channel(channels['console'])
		await channel.send(embed = discord.Embed(description = f'`{member.display_name}` покинув нас!', color = 0x4D4D4D))	




	@commands.Cog.listener()

	async def on_message(self, message):
		print(f'[{message.author.name}#{message.author.discriminator}] {message.content}')
		banRoles = ['bot']
		from config import helloWords
		msg = message.content.lower()
		author = message.author
		permission = True

		#client-triger
		if message.author.bot != True:
			for role in message.author.roles:
				if str(role) in banRoles:
					permission = False

			if permission:
				#hello-word say
				if msg in helloWords:
					await message.channel.send(f'{helloWords[randint(0, len(helloWords) - 1)]}')
				#random reaction
				if randint(0, 100) <= 2:
					emojis = message.guild.emojis
					emoji = emojis[randint(0, len(emojis) - 1)]
					await message.add_reaction(emoji)
				#add-ban ds servers for link
				if msg.find('https://discord.gg/') != -1:
					server_links_list = await message.guild.invites()

					i = 0 
					while i < len(server_links_list):
						print(server_links_list[i].url.lower())
						if msg.find(server_links_list[i].url.lower()) != -1:
							return
						i += 1

					self.owner = message.guild.owner
					await self.owner.send(f'{message.author} Рекламував посторонній сервер діскорд на твоєму сервері. Краще заблокуй його у себе')
					await message.author.send(f'Тебе було автоматично забанено на ``{message.guild.name}`` за рекламу посторонніх діскорд серверів')
					await message.author.ban(reason = 'Реклама дс серверів', delete_message_days = 0)
					await message.channel.purge(limit = 1)
				"""
				if msg.find('https://discord.gg/') != -1 and msg.find('https://discord.gg/9caqe3aw8p') == -1:
					self.owner = message.guild.owner
					await self.owner.send(f'{message.author} Рекламував посторонній сервер діскорд на твоєму сервері. Краще заблокуй його у себе')
					await message.author.send(f'Тебе було автоматично забанено на ``{message.guild.name}`` за рекламу посторонніх діскорд серверів')
					await message.author.ban(reason = 'Реклама дс серверів', delete_message_days = 0)
					await message.channel.purge(limit = 1)
				"""
		else:
			if author.name + '#' + author.discriminator == 'Server Monitoring#8312':
				print('bump!')
				print(message.embeds[0].colour)
				color = str(message.embeds[0].colour)
				if color == '#43b581':
					author = message.embeds[0].description[67:-11]
					print('success bump')
					await asyncio.sleep(4*60*60)
					await message.channel.send(f'{author} 4 години пройшло. Попроси інших, аби бампанули')

	@commands.Cog.listener()

	async def on_raw_reaction_add(self, reaction):
		if reaction.member.bot == False and reaction.message_id == 843190334263787570:
			channel = self.client.get_channel(channels['info'])
			info_msg = await channel.fetch_message(843190334263787570)
			info_count = len(listdir('info'))


			if str(reaction.emoji) != '0️⃣':

				info_file = open('info/' + str(listdir('info')[int(str(reaction.emoji)[0]) - 1]), encoding = 'utf-8')
				info_str = info_file.readlines()
	
				embed = discord.Embed(title = str(listdir('info')[int(str(reaction.emoji)[0]) - 1])[0:-4])
	
				i = 0
				for line in info_str:
					i = i + 1
					embed.add_field(name=f'_-|{i}|-_', value = line)
	
				info_file.close()
			
			else:
				i = 1
				content = ''
				for page in listdir('info'):
					content = content + str(i) + ' - ' + str(page[0:-4]) + '\n'

					i = i + 1

				embed = discord.Embed(description = content, title = 'Зміст')

			await info_msg.edit(embed = embed)
			embed = None
	
			await info_msg.remove_reaction(emoji = reaction.emoji,member = reaction.member)


def setup(client):
	client.add_cog(User(client))