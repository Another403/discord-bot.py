from datetime import datetime
from glob import glob
from asyncio import sleep

from discord import Intents
from discord import Embed, File
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from discord.ext.commands import when_mentioned_or, command, has_permissions
from discord.errors import HTTPException, Forbidden

from apscheduler.triggers.cron import CronTrigger

PREFIX = "e/"
Eternity = [760377763206529034]
available = [884739097808228373, 879748364231671818, 879748443768250379]
thumbnailURL = 'https://cdn.discordapp.com/attachments/884739097808228373/884834873766969425/Six.jpg'
imageURL = 'https://cdn.discordapp.com/attachments/884739097808228373/884834214388842536/9aee883704fd6a1634b35dcdc216b5da.jpg'
botURL = 'https://cdn.discordapp.com/attachments/884739097808228373/884835480938627152/image.png'
COGS = [path.split('\\')[-1][:-3] for path in glob('./lib/cogs/*.py')]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

def get_prefix(bot, message):
	return when_mentioned_or(PREFIX)(bot, message)

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f'{cog} cog ready')

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
	def __init__(self):
		self.ready = False
		self.guild = None

		super().__init__(
			command_prefix = get_prefix,
			owner_ids = Eternity,
			intents = Intents.all()
		)

	def setup(self):
		for cog in COGS:
			self.load_extension(f'lib.cogs.{cog}')
			print(f'{cog} cog loaded')

		print("setup completed")

	def run(self, version):
		self.VERSION = version

		print('Getting things ready...')
		self.setup()

		with open('./lib/bot/token', 'r', encoding='utf-8') as tf:
			self.token = tf.read()
		print('Processing...')
		super().run(self.token, reconnect = True)

	async def process_commands(self, message):
		ctx = await self.get_context(message, cls = Context)

		if ctx.command is not None and ctx.guild is not None:
			if self.ready:
				await self.invoke(ctx)
			else:
				await ctx.channel.send('Starting up, please wait a few seconds.')

	async def rules_reminder(self):
		await self.stdout.send("Remember to adhere to the rules.")

	async def on_connect(self):
		print('Down for Eternity')

	async def on_disconnect(self):
		print('Time to rest now')

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("System error, please try again later.")
		channel = self.get_channel(884973942614401044)
		await channel.send("Error, system failed.")
		raise

	async def on_command_error(self, ctx, exc):
		if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
			pass

		elif isinstance(exc, MissingRequiredArgument):
			await ctx.send('One or more required elements were missing.')

		elif isinstance(exc, CommandOnCooldown):
			await ctx.send(f'Renewing proccess, {str(exc.cooldown.type).split(".")[-1]} protocol. Please wait {exc.retry_after:,.2f} secsbefore trying again')

		elif hasattr(exc, 'original'):
			# if isinstance(exc.original, HTTPException):
			#	await ctx.channel.send('Unable to send information.')

			if isinstance(exc.original, Forbidden):
				await ctx.channel.send('No permission given.')

			else :
				raise exc.original

		else:
			raise exc

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(1021103269021503519)
			self.stdout = self.get_channel(1021123170532589709)
			self.cogs_ready = Ready()

			await self.stdout.send('Hello, my name is Rivery')
			
			embed = Embed(title = "Online", description = "Rivery is on his way.", colour = 0xFF0000, timestamp = datetime.utcnow())
			fields = [("Name", "Rivery", True),
					  ("Age", "17", True),
					  ("Roles", "Bot - Moderator", False)]
			for name, val, inline in fields:
				embed.add_field(name = name, value = val, inline = inline)
			embed.set_author(name = "Eternity", icon_url = botURL)
			embed.set_footer(text = 'A brief description of Rivery')
			embed.set_thumbnail(url = thumbnailURL)
			embed.set_image(url = imageURL)
			await self.stdout.send(embed = embed)

			while not self.cogs_ready.all_ready():
				await sleep(0.5)
			
			print("Let's go")

		else:
			print("Reconnected")

	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)

bot = Bot()