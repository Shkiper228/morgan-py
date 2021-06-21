import discord
from discord.ext import commands
from discord.utils import get
from random import randint
from tzlocal import get_localzone
from config import config, channels, number_emoji, mafia
import asyncio
import sqlite3
import pytz
import math
import datetime


#global

def max(array):
	biggest = 0
	i = 0
	while i < len(array):
		if array[i] > biggest:
			biggest = array[i]
		i += 1 

		return biggest




class Player:
	def __init__(self, member, role, personal_channel):
		self.member = member
		self.role = role
		self.personal_channel = personal_channel
		self.isDead = False
		self.last_message = None
		self.moves = []
		self.votes = []

class Mafia_game:
	isSet = False
	players = []
	category = None
	main_channel = None
	count = 0
	count_living = 0
	win = None
	
	isVote = False

	player_markup = ''
	summary_message = []

	numbers_roles = []
	last_moves = []
	last_votes = []

	nigth = 0

	count_per_role = []
	last_votes_per_player = []
	sequence_role = []
	random_numbers = []
	
mafia_game = Mafia_game()


class User(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ['mafiatext'])
	
	async def __mafiatext(self, ctx, action = None, *typed_players):

		mafia_game.count = len(typed_players)
		mafia_game.count_living = mafia_game.count
		channel = ctx.channel

		if mafia_game.isSet == True and action != 'delete' and action != 'remove':
			await channel.send(embed = discord.Embed(description = f'{ctx.message.author.mention} гра уже запущена. Спробуйте почати нову портію пізніше'))
			return

		if action == 'create':
			"""
	
			ПРОВІРКА

			"""

			#провірка кількості
			if mafia_game.count < 5:
				await channel.send('Недостатня кількість гравців')
				return

			#провірка гравців
			i = 0
			while i < mafia_game.count: 
				mafia_game.last_moves.append(None)
				mafia_game.last_votes.append(None)
				mafia_game.numbers_roles.append(None)
				mafia_game.last_votes_per_player.append(0)
				mafia_game.players.append(Player(ctx.message.guild.get_member(int(typed_players[i])), None, None))
				if mafia_game.players[i].member == None:
					await channel.send(f'Неправильно введено нік гравця №{i + 1}')
					return
				print(f'Гравець номер {i + 1} {mafia_game.players[i].member.name}') 

				i = i + 1

			# Якщо все гаразд
			mafia_game.isSet = True


			
			"""

			КІНЕЦЬ ПРОВІРКИ

			"""

			"""

			ПАРСИНГ ГРАВЦІВ

			"""
			
			total_count = 0
			m = 1
			i = 0
			while i < len(mafia['sequence']): # кількісь циклів = кількість ролей
				mafia_game.sequence_role.append([])
				if mafia['sequence'][i] != 'civils': # якщо роль не є мирним

					mafia_game.count_per_role.append(math.floor(mafia_game.count/mafia['minPlayers'][i]))
					total_count = total_count + mafia_game.count_per_role[i]

				else: # решта випадків

					mafia_game.count_per_role.append(mafia_game.count - total_count)

				j = 0
				while j < mafia_game.count_per_role[i]: # цикл для формування ключа ролей
					mafia_game.sequence_role[i].append(m)
					j = j + 1
					m = m + 1

				i = i + 1
			i = 0
			print(f'Ключ {mafia_game.sequence_role}')


			i = 0
			while i < mafia_game.count:

				number = randint(1, mafia_game.count)
				isUnique = True

				j = 0
				while j < len(mafia_game.random_numbers):

					if number == mafia_game.random_numbers[j]:
						isUnique = False

					j = j + 1

				if isUnique:
					mafia_game.random_numbers.append(number)
					i = i + 1

			print(f'рандомний числовий ряд {mafia_game.random_numbers}')


			m = 0 
			i = 0
			while i < len(mafia['sequence']):

				# Розприділення ролей
				j = 0
				while j < len(mafia_game.sequence_role[i]):
					mafia_game.players[mafia_game.random_numbers[m] - 1].role = mafia['sequence'][i]
					print(f'В грі бере участь {mafia_game.players[mafia_game.random_numbers[m] - 1].member.name} і у нього роль: {mafia_game.players[mafia_game.random_numbers[m] - 1].role}')

					
					j = j + 1
					m = m + 1

				i = i + 1
			"""

			ПАРСИНГ ГРАВЦІВ

			"""
			"""

			СТВОРЕННЯ І НАСТРОЙКА КАТЕГОРІЇ

			"""

			mafia_game.category = await ctx.message.guild.create_category('MAFIA')
			await mafia_game.category.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False, manage_messages=False)
			mafia_game.main_channel = await mafia_game.category.create_text_channel('main')


			i = 0
			while i < mafia_game.count:
				print('work')
				mafia_game.players[i].personal_channel = await mafia_game.category.create_text_channel(str(mafia_game.players[i].member), reason = 'Гра в мафію')
				await mafia_game.players[i].personal_channel.set_permissions(mafia_game.players[i].member, send_messages=True, read_messages=True, add_reactions=False, manage_messages=False)

				#await mafia_game.players[i].personal_channel.send(f'`{mafia_game.players[i].member.name}` ваша роль --->>  `{mafia_game.players[i].role}`')
				i = i + 1


			i = 0
			while i < len(mafia_game.players):
				await mafia_game.category.set_permissions(mafia_game.players[i].member, send_messages=True, read_messages=True, manage_messages=False)
				i += 1
			"""

			КІНЕЦЬ СТВОРЕННЯ І НАСТРОЙКИ КАТЕГОРІЇ

			"""	

			"""

			НУЛЬОВИЙ ДЕНЬ

			"""

			await mafia_game.main_channel.send(embed = discord.Embed(description = f'Розпочато _`нульовий день`_. Можете просто поспілкуватись тут\nЧерез 2 хвилини вам повідомиться _`роль`_ і почнеться _`перша ніч`_'))
			mafia_game.player_markup 
			i = 0
			while i < mafia_game.count:
				mafia_game.player_markup += f'{number_emoji[i + 1]} ---> _`{mafia_game.players[i].member.name}`_\n'
				i += 1
			await mafia_game.main_channel.send(embed = discord.Embed(description = mafia_game.player_markup))
			await asyncio.sleep(120)
			await mafia_game.main_channel.send(embed = discord.Embed(description = f'Початок _`першої ночі`_\nУдачі вам вижити!'))

			#сповіщення ролі
			i = 0
			while i < mafia_game.count:
				mafia_game.last_moves[i] = None
				mafia_game.numbers_roles[i] = None
				await mafia_game.players[i].personal_channel.send(f'`{mafia_game.players[i].member.name}` ваша роль --->>  `{mafia_game.players[i].role}`')
				i = i + 1



			"""

			КІНЕЦЬ НУЛЬОВОГО ДНЯ

			"""

			"""

			КОНВЕЄР

			"""

			while mafia_game.win == None:
				mafia_game.nigth += 1
				if mafia_game.nigth != 1:
					await mafia_game.main_channel.send(embed = discord.Embed(description = f'Розпочалась ніч _`№{mafia_game.nigth}`_'))
				#формування повідомлення з вибором
				i = 0
				while i < mafia_game.count :

					if mafia_game.players[i].role == mafia['sequence'][0] and mafia_game.players[i].isDead == False:
						await mafia_game.players[i].personal_channel.send(mafia_game.players[i].member.mention)
						mafia_game.players[i].last_message = await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = f'Розпочалась ніч _`№{mafia_game.nigth}`_\nВиберіть свою жертву за допомогою реакції на повідомленні'))
						await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = mafia_game.player_markup))

						p = 0
						while p < mafia_game.count:
							if mafia_game.players[p].isDead == False and mafia_game.players[p] != mafia_game.players[i] and mafia_game.players[p].role != mafia_game.players[i].role:
								await mafia_game.players[i].last_message.add_reaction(number_emoji[p + 1])
							p += 1
							
					if mafia_game.players[i].role == mafia['sequence'][1] and mafia_game.players[i].isDead == False:
						await mafia_game.players[i].personal_channel.send(mafia_game.players[i].member.mention)
						mafia_game.players[i].last_message = await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = f'Розпочалась ніч _`№{mafia_game.nigth}`_\nВиберіть, кого ви хочете провірити, за допомогою реакції на повідомленні'))
						await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = mafia_game.player_markup))

						p = 0
						while p < mafia_game.count:
							if mafia_game.players[p].isDead == False and mafia_game.players[p] != mafia_game.players[i] and mafia_game.players[p].role != mafia_game.players[i].role:
								await mafia_game.players[i].last_message.add_reaction(number_emoji[p + 1])
							p += 1
					
					if mafia_game.players[i].role == mafia['sequence'][2] and mafia_game.players[i].isDead == False:
						await mafia_game.players[i].personal_channel.send(mafia_game.players[i].member.mention)
						mafia_game.players[i].last_message = await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = f'Розпочалась ніч _`№{mafia_game.nigth}`_\nВиберіть, кого варто вилікувати, за допомогою реакції на повідомленні'))
						await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = mafia_game.player_markup))

						p = 0
						while p < mafia_game.count:
							if mafia_game.players[p].isDead == False and mafia_game.players[p] != mafia_game.players[i] and mafia_game.players[p].role != mafia_game.players[i].role and mafia_game.nigth < 2:
								await mafia_game.players[i].last_message.add_reaction(number_emoji[p + 1])
							elif mafia_game.players[p].isDead == False and mafia_game.players[p] != mafia_game.players[i] and mafia_game.players[p].role != mafia_game.players[i].role and mafia_game.players[i].moves[mafia_game.nigth - 2] != i:
								await mafia_game.players[i].last_message.add_reaction(number_emoji[p + 1])
							elif mafia_game.players[p] == mafia_game.players[i] and i not in mafia_game.players[i].moves:
								await mafia_game.players[i].last_message.add_reaction(number_emoji[p + 1])
							p += 1

					if mafia_game.players[i].role == mafia['sequence'][3] and mafia_game.players[i].isDead == False:
						await mafia_game.players[i].personal_channel.send(mafia_game.players[i].member.mention)
						mafia_game.players[i].last_message = await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = f'Розпочалась ніч №{mafia_game.nigth}\nВиберіть, кому ви хочете зробити алібі, за допомогою реакції на повідомленні'))
						await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = mafia_game.player_markup))

						p = 0
						while p < mafia_game.count:
							if mafia_game.players[p].isDead == False and mafia_game.players[p] != mafia_game.players[i] and mafia_game.players[p].role != mafia_game.players[i].role:
								await mafia_game.players[i].last_message.add_reaction(number_emoji[p + 1])
							p += 1

					if mafia_game.players[i].role == mafia['sequence'][4] and mafia_game.players[i].isDead == False:
						mafia_game.players[i].last_message = await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = f'Розпочалась ніч №{mafia_game.nigth}\nБажаємо вижити вам)'))
						await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = mafia_game.player_markup))

					i += 1

				wheAllDidMove = False
				while wheAllDidMove == False:
					wheAllDidMove = True
					i = 0
					while i < mafia_game.count:
						mafia_game.last_votes_per_player[i] = 0
						mafia_game.last_votes[i] = None
						mafia_game.last_moves[i] = None
						
						if len(mafia_game.players[i].moves) < mafia_game.nigth and mafia_game.players[i].role != mafia['sequence'][4]:
							print(f'Кількість ходів гравця {mafia_game.players[i].member.name}: {len(mafia_game.players[i].moves)} кількість ночей {mafia_game.nigth}')
							wheAllDidMove = False
						i += 1
					print('\n')
					await asyncio.sleep(10)

				await mafia_game.main_channel.send(embed = discord.Embed(description = f'_`Усі гравці`_ зробили хід!\nПідраховуються результати цієї ночі'))

				#Обробка ходів

				#Запис ходів
				i = 0
				while i < mafia_game.count:
					if mafia_game.players[i].role == mafia['sequence'][0]:
						mafia_game.last_moves[0] = mafia_game.players[i].moves[mafia_game.nigth - 1]


					if mafia_game.players[i].role == mafia['sequence'][1]:
						mafia_game.last_moves[1] = mafia_game.players[i].moves[mafia_game.nigth - 1]


					if mafia_game.players[i].role == mafia['sequence'][2]:
						mafia_game.last_moves[2] = mafia_game.players[i].moves[mafia_game.nigth - 1]


					if mafia_game.players[i].role == mafia['sequence'][3]:
						mafia_game.last_moves[3] = mafia_game.players[i].moves[mafia_game.nigth - 1]

					i += 1

				print(f'ходи гравців за останню ніч {mafia_game.last_moves}')



				mafia_game.summary_message.append('')
				if mafia_game.last_moves[0] == mafia_game.last_moves[2]:

					mafia_game.summary_message[mafia_game.nigth - 1] += f'Ніхто не помер\n'

				else: 
					mafia_game.players[mafia_game.last_moves[0]].isDead = True

					j = 0
					while j < len(mafia['sequence']):
						if mafia_game.players[mafia_game.last_moves[0]].role == mafia['sequence'][j]:
							mafia_game.count_living -= 1
							mafia_game.count_per_role[j] -= 1
						j += 1

					print(f'Кількість гравців за роллю {mafia_game.count_per_role}')
					
					await mafia_game.players[mafia_game.last_moves[0]].personal_channel.set_permissions(mafia_game.players[mafia_game.last_moves[0]].member, send_messages=False, read_messages=False)
					await mafia_game.main_channel.set_permissions(mafia_game.players[mafia_game.last_moves[0]].member, send_messages=False, read_messages=True)

					mafia_game.summary_message[mafia_game.nigth - 1] += f'Помер гравець _`{mafia_game.players[mafia_game.last_moves[0]].member.name}`_\n'

				if mafia_game.count_living >= mafia['minPlayers'][3]:
					mafia_game.summary_message[mafia_game.nigth - 1] += f'Повія сходила до гравця _`{mafia_game.players[mafia_game.last_moves[3]].member.name}`_ _(це значить, що висталяти на голосування цього гравця не можна)_'

				await mafia_game.main_channel.send(embed = discord.Embed(description = f'`Цієї ночі:`\n{mafia_game.summary_message[mafia_game.nigth - 1]}'))
				


				if mafia_game.count_per_role[0] >= mafia_game.count_living - mafia_game.count_per_role[0]:
					mafia_game.win = mafia['sequence'][0]


				elif mafia_game.count_per_role[0] == 0:
					mafia_game.win = mafia['sequence'][4]

				if mafia_game.win == None:
					await mafia_game.main_channel.send(embed = discord.Embed(description = f'Через 15 секунд наступить день'))

					await asyncio.sleep(15)
				else:
					await mafia_game.main_channel.send(embed = discord.Embed(description = f'Виграли _`{mafia_game.win}`_'))

					winning = '_`Ролі гравців`_\n'
					i = 0
					while i < mafia_game.count:
						winning += f'{number_emoji[i + 1]} ---> _`{mafia_game.players[i].member.name}`_ ---> _`{mafia_game.players[i].role}`_\n'

						i += 1

					await mafia_game.main_channel.send(embed = discord.Embed(description = winning))
					await asyncio.sleep(60)
					return





				"""

				ДЕНЬ І ГОЛОСУВАННЯ

				"""

				mafia_game.isVote = True

				vote_message = await mafia_game.main_channel.send(embed = discord.Embed(description = f'Настав день №{mafia_game.nigth}\nВи можете проголосувати за вигнання одного з гравців.\nОбговоріть свій вибір з іншими впродовж паузи на день (3 хвилини)'))
				await mafia_game.main_channel.send(embed = discord.Embed(description = mafia_game.player_markup))
				i = 0
				while i < mafia_game.count:
					if mafia_game.count_per_role[3] == 0:
						if mafia_game.players[i].isDead == False:
							await vote_message.add_reaction(number_emoji[i + 1])
							i += 1
							continue

					if mafia_game.players[i].isDead == False and mafia_game.last_moves[3] != i:
						await vote_message.add_reaction(number_emoji[i + 1])

					i += 1

				await asyncio.sleep(180)

				mafia_game.isVote = False

				# Обробка результатів голосування

				without_vote = mafia_game.count_living
				i = 0
				while i < mafia_game.count:
					without_vote -= mafia_game.last_votes_per_player[i]
					print(f'За гравця {mafia_game.players[i].member.name} проголосувало {mafia_game.last_votes_per_player[i]} гравців')

					i += 1

				max_count_votes = 0
				a = 0
				while a < len(mafia_game.last_votes_per_player):
					if max_count_votes < mafia_game.last_votes_per_player[a]:
						max_count_votes = mafia_game.last_votes_per_player[a]

					a += 1
				print(f'Найбільше голосування на гравця {max_count_votes}')				
				print(f'Утрималось {without_vote} гравців')
				if without_vote > max_count_votes:
					await mafia_game.main_channel.send(embed = discord.Embed(description = 'Цього дня більшість утрималась і ми не вигнали нікого'))
				else:
					kicked_player_index = mafia_game.last_votes_per_player.index(max_count_votes)
					await mafia_game.main_channel.send(embed = discord.Embed(description = f'Цього дня методом голосування було вигнано гравця {mafia_game.players[kicked_player_index].member.name}'))
					mafia_game.players[kicked_player_index].isDead = True
					mafia_game.count_living -= 1

					i = 0
					while i < len(mafia['sequence']):
						if mafia_game.players[kicked_player_index].role == mafia['sequence'][i]:
							mafia_game.count_per_role[i] -= 1
						i += 1



				"""

				КІНЕЦЬ ДНЯ І ГОЛОСУВАННЯ

				"""

				if mafia_game.count_per_role[0] >= mafia_game.count_living - mafia_game.count_per_role[0]:
					mafia_game.win = mafia['sequence'][0]


				elif mafia_game.count_per_role[0] == 0:
					mafia_game.win = mafia['sequence'][4]


				if mafia_game.win == None:
					await mafia_game.main_channel.send(embed = discord.Embed(description = f'Через 15 секунд розпочнеться наступна ніч'))

					await asyncio.sleep(15)
				else:
					await mafia_game.main_channel.send(embed = discord.Embed(description = f'Виграли _`{mafia_game.win}`_'))

					winning = '_`Ролі гравців`_\n'
					i = 0
					while i < mafia_game.count:
						winning += f'{number_emoji[i + 1]} ---> _`{mafia_game.players[i].member.name}`_ ---> _`{mafia_game.players[i].role}`_\n'

						i += 1

					await mafia_game.main_channel.send(embed = discord.Embed(description = winning))
					await asyncio.sleep(60)
					return


				if mafia_game.isSet == False:
					return







		
			"""

			КІНЕЦЬ КОНВЕЄРУ

			"""		

		elif action == 'delete' or action == 'remove':

			if mafia_game.isSet == False:
				await ctx.message.channel.send(embed = discord.Embed(description = f'{ctx.message.author.mention} зараз немає існуючої партії гри в мафію\nАби створити гру потрібно ввести команду:\n `$mafiatext create *id 1-o гравця* *id 2-o гравця* *id 3-o гравця* *id 4-o гравця* *id 5-o гравця* ... *id 9-o гравця*`'))
				return
			# Провірка доступу
			perm = False
			i = 0
			while i < mafia_game.count:
				if mafia_game.players[i].member == ctx.message.author:
					perm = True

				i += 1

			if perm == False:
				await ctx.message.channel.send(embed = discord.Embed(description = f'{ctx.message.author.mention} зараз включена партія гри, в якій ви не берете участі\nВи повинні бути учасником партії, аби мати право її видалити'))
				return
			print('Видаляю гру')
			c = 0

			while c < len(mafia_game.players) + 1:
				if c < len(mafia_game.players):
					await mafia_game.players[c].personal_channel.delete(reason = 'Гра в мафію')
				else:
					await mafia_game.main_channel.delete(reason = 'Гра в мафію')
				c += 1

			await mafia_game.category.delete(reason = 'Гра в мафію')

			mafia_game.isSet = False
			mafia_game.players = []
			mafia_game.category = None
			mafia_game.main_channel = None
			mafia_game.count = 0
			mafia_game.count_living = 0
			mafia_game.win = None

			mafia_game.isVote = False

			mafia_game.player_markup = ''
			mafia_game.summary_message = []

			mafia_game.numbers_roles = []
			mafia_game.last_moves = []
			mafia_game.last_votes = []

			mafia_game.nigth = 0

			mafia_game.count_per_role = []
			mafia_game.last_votes_per_player = []
			mafia_game.sequence_role = []
			mafia_game.random_numbers = []

		
	@commands.Cog.listener()

	async def on_raw_reaction_add(self, reaction):
		guild = self.client.get_guild(reaction.guild_id)
		channel = guild.get_channel(reaction.channel_id)


		

		if channel.category == mafia_game.category and reaction.member.bot == False:
			i = 0
			while i < mafia_game.count:
				if mafia_game.players[i].isDead == True:
					return
				if mafia_game.players[i].member == reaction.member: #гравець який поставив реакцію
					print('знайдено гравця, який проголосував/походив')

					if  channel == mafia_game.players[i].personal_channel and len(mafia_game.players[i].moves) < mafia_game.nigth:

						j = 0
						while j < mafia_game.count:
							if str(reaction.emoji) == number_emoji[j + 1]:
								print('знайдено гравця, до якого походили')

								mafia_game.players[i].moves.append(j)
								if mafia_game.players[i].role == mafia['sequence'][0]:
									await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = f'Ви замахнулись на життя гравця _`{mafia_game.players[j].member.name}`_\nЯкщо його не вилікує _`doctor`_, то він помре'))
	
	
								if mafia_game.players[i].role == mafia['sequence'][1]:
									if mafia_game.players[j].role == 'mafia':
										await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = f'Гравець _`{mafia_game.players[j].member.name}`_ є мафією'))
									else:
										await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = f'Гравець _`{mafia_game.players[j].member.name}`_ є мирним'))
	
								if mafia_game.players[i].role == mafia['sequence'][2]:
									await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = f'Ви вилікували гравця _`{mafia_game.players[j].member.name}`_'))
	
	
								if mafia_game.players[i].role == mafia['sequence'][3]:
									await mafia_game.players[i].personal_channel.send(embed = discord.Embed(description = f'Ви провели ніч з гравцем _`{mafia_game.players[j].member.name}`_'))


								print(f'Гравець {mafia_game.players[i].member.name} вибрав {mafia_game.players[i].moves[mafia_game.nigth - 1]}')

							j += 1


					elif channel == mafia_game.main_channel:
						if mafia_game.last_votes[i] != None:
							print(f'{mafia_game.players[i].member.name} намагався повторно проголосувати')
							return

						if mafia_game.isVote == False:
							print(f'{mafia_game.players[i].member.name} намагався проголосувати, коли голосування було закрите')
							return

						j = 0
						while j < mafia_game.count:
							print('Шукаємо гравця')
							if str(reaction.emoji) == number_emoji[j + 1] :
								print('знайдено гравця, за якого проголосували')
								mafia_game.players[i].votes.append(j)
								mafia_game.last_votes[i] = j
								mafia_game.last_votes_per_player[j] += 1
								

								print(f'гравeць {mafia_game.players[i].member.name} проголосував за {mafia_game.players[j].moves[mafia_game.nigth - 1]}')

								print(f'Голосування гравця {mafia_game.players[i].votes}')
							print(f'Голосування за гравцями {mafia_game.last_votes_per_player}')

							j += 1
				i += 1


def setup(client):
	client.add_cog(User(client))