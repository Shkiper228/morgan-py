import discord
from discord.ext import commands

client = commands.Bot( command_prefix = '!', intents = discord.Intents.all())

config = {
	'token': 'NjgxOTI5OTMxOTM2MzY2Njk2.XlVmvQ.uhW5wYzgeDQpGIlLLXvgsF5--4g',
	'name': 'Morgan',
	'ID': 681929931936366696,
	'prefix': '$',
	'time_zone': 2
}

channels = {
	'console': client.get_channel(704660113750884433),
	'new_users': client.get_channel(704690682920697875),
	'advertisement': client.get_channel(720915216174415963)
}

helloWords = [
	'привіт',
	'привет',
	'здоров'
]

mafia = dict(
	minPlayers = [
		5, 	#mafia
		5, 	#sherif
		5,	#doctor
		7 	#putana
		],
	sequence = [
		'mafia',
		'sherif',
		'doctor',
		'putana',
		'civils'
	]

	)
	
