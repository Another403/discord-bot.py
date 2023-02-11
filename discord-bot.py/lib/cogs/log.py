from datetime import datetime
from discord import Forbidden, Embed
from discord.ext.commands import Cog
from discord.ext.commands import command

channel = 996087117056851988

class Log(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		self.log_channel = self.bot.get_channel(channel)
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up('log')

	@Cog.listener()
	async def on_user_update(self, before, after):
		if before.name != after.name:
			embed = Embed(title = "Member update",
						  description = "Detected changes in username",
						  colour = self.log_channel.guild.get_member(after.id).colour,
						  timestamp = datetime.utcnow())

			fields = [('Before', before.name, False),
					  ('After', after.name, False)]

			for name, value, inline in fields:
				embed.add_field(name = name, value = value, inline = inline)

			await self.log_channel.send(embed = embed)

		if before.avatar_url != after.avatar_url :
			embed = Embed(title = "Member update",
						  description = "Detected changes in avatar",
						  colour = self.log_channel.guild.get_member(after.id).colour,
						  timestamp = datetime.utcnow())

			embed.set_thumbnail(url = before.avatar_url)
			embed.set_image(url = after.avatar_url)

			await self.log_channel.send(embed = embed)

		if before.discriminator != after.discriminator:
			embed = Embed(title = "Member update",
						  description = "Detected changes in discriminator",
						  colour = self.log_channel.guild.get_member(after.id).colour,
						  timestamp = datetime.utcnow())

			fields = [('Before', before.discriminator, False),
					  ('After', after.discriminator, False)]

			for name, value, inline in fields:
				embed.add_field(name = name, value = value, inline = inline)

			await self.log_channel.send(embed = embed)

	@Cog.listener()
	async def on_member_update(self, before, after):
		if before.display_name != after.display_name:
			embed = Embed(title = "Member update",
						  description = "Detected changes in nickname",
						  colour = after.colour,
						  timestamp = datetime.utcnow())

			fields = [('Before', before.display_name, False),
					  ('After', after.display_name, False)]

			for name, value, inline in fields:
				embed.add_field(name = name, value = value, inline = inline)

			await self.log_channel.send(embed = embed)
	'''
	@Cog.listener()
	async def on_message_edit(self, before, after):
		if not after.author.bot:
			if before.content != after.content:
				embed = Embed(title = "Message update",
							  description = "Message edited",
							  colour = 0x20A9DC,
							  timestamp = datetime.utcnow())

				fields = [('Before', before.content, False),
						  ('After', after.content, False)]

				for name, value, inline in fields:
					embed.add_field(name = name, value = value, inline = inline)

				await self.log_channel.send(embed = embed)



	@Cog.listener()
	async def on_message_delete(self, before, after):
		if not after.author.bot:
			pass
	'''

def setup(bot):
	bot.add_cog(Log(bot))