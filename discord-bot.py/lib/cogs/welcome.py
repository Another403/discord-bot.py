from discord.ext.commands import Cog
from discord.ext.commands import command

tsukasa = 760377763206529034

class Welcome(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.welcome_channel = 0
		self.goodbye_channel = 0

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up('welcome')

	@command('set_welcome_channel', aliases = ['swc'])
	async def set_welcome_channel(self, ctx):
		if ctx.author.id == tsukasa:
			self.welcome_channel = self.bot.get_channel(ctx.channel.id)
			await ctx.channel.send(f'Welcome channel set to {ctx.channel.name}')

		else:
			await ctx.channel.send('Not enough permissions, returning nothing.')

	@command('set_goodbye_channel', aliases = ['sgc'])
	async def set_goodbye_channel(self, ctx):
		if ctx.author.id == tsukasa:
			self.goodbye_channel = self.bot.get_channel(ctx.channel.id)
			await ctx.channel.send(f'Goodbye channel set to {ctx.channel.name}')

		else:
			await ctx.channel.send('Not enough permissions, returning nothing.')

	@Cog.listener()
	async def on_member_join(self, member):
		if self.welcome_channel == 0:
			print('no channel provided')
		
		else:
			await self.welcome_channel.send(f'Welcome to **{member.guild.name}**, {member.mention}. Please enjoy your stay.')

	@Cog.listener()
	async def on_member_remove(self, member):
		if self.goodbye_channel == 0:
			print('no channel provided')

		else:
			await self.goodbye_channel.send(f'{member.display_name} has left. Hope to see you again.')

def setup(bot):
	bot.add_cog(Welcome(bot))