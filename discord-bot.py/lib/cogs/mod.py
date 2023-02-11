from pickle import TRUE
from typing import Optional
from datetime import datetime, timedelta

from discord import Embed, Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions

guild = 1021103269021503519

class Mod(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.guild = self.get_guild(guild)

	@command(name = 'kick')
	@bot_has_permissions(kick_members = True)
	@has_permissions(kick_members = True)
	async def kick_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No specific reason."):
		self.log_channel = ctx.channel

		if not len(targets):
			await ctx.send('Missing required argument, returning -1.')
		else:
			for target in targets:
				await target.kick(reason = reason)
	
				embed = Embed(title = "Member got kicked",
							  colour = 0x225500,
							  timestamp = datetime.utcnow())

				embed.set_thumbnail(url = target.avatar_url)

				fields = [("Member: ", f'{target.display_name}', False),
						  ("Kicked by: ", ctx.author.display_name, False),
						  ("Reason: ", reason, False)]

				for name, value, inline in fields:
					embed.add_field(name = name, value = value, inline = inline)

				await self.log_channel.send(embed = embed)
				
	@kick_members.error
	async def kick_members_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Error 7, not enough permissions.")

	@command(name = 'ban')
	@bot_has_permissions(ban_members = True)
	@has_permissions(ban_members = True)
	async def ban_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No specific reason."):
		self.log_channel = ctx.channel
		if not len(targets):
			await ctx.send('Missing required argument, returning -1.')
		else:
			for target in targets:
				await target.ban(reason = reason)
				
				embed = Embed(title = 'Member got kicked',
							  colour = 0x225500,
							  timestamp = datetime.utcnow())

				embed.set_thumbnail(url = target.avatar_url)

				fields = [('Member: ', f'{target.display_name}', False),
						  ("Banned by:", ctx.author.display_name, False),
						  ('Reason:', reason, False)]

				for name, value, inline in fields:
					embed.add_field(name = name, value = value, inline = inline)

				await self.log_channel.send(embed = embed)

	@ban_members.error
	async def ban_members_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Error 7, not enough permissions.")

	@command(name = 'delmess', aliases = ['purge', 'clear'])
	@bot_has_permissions(manage_messages = True)
	@has_permissions(manage_messages = True)
	async def clear_messages(self, ctx, limit: Optional[int] = 1):
		if limit >= 100:
			await ctx.send('Too much information to clear, try again with a smaller amount.')
			return

		with ctx.channel.typing():
			await ctx.message.delete()
			deleted = await ctx.channel.purge(limit = limit, after = datetime.utcnow() - timedelta(seconds = 1))

			await ctx.send(f'{len(deleted):,} messages has been executed.')

	@command(name = 'count_members', aliases = ['countm', 'members'])
	async def count_members(self, ctx):
		await ctx.send(f'{len(self.guild.members):,} has joined our family.')

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up('mod')

def setup(bot):
	bot.add_cog(Mod(bot))