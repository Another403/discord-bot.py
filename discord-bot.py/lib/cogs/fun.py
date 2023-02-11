from random import choice, randint
from typing import Optional

from discord import Member, Embed

from aiohttp import request
from discord.ext.commands import BadArgument
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown

sayHello = ['Have a nice day', 'Nice to meet you', 'My pleasure']

class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name = 'hello', aliases = ['hi', 'h'])
	async def greeting(self, ctx):
		await ctx.channel.send(f'{choice(sayHello)} {ctx.author.mention}')

	@command(name = 'dice', aliases = ['d', 'roll'])
	@cooldown(1, 15, BucketType.user)
	async def roll_dice(self, ctx, dice_string : str):
		dice, val = (int(term) for term in dice_string.split('d'))

		if dice <= 35:
			rolls = [randint(1, val) for i in range(val)]
			await ctx.channel.send(' + '.join([str(r) for r in rolls]) + f' = {sum(rolls)}')
		else:
			await ctx.channel.send('Too many dices, please try a lower test case.')


	@command(name = 'slap', aliases = ['hit, punch'])
	async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = 'no reason'):
		await ctx.channel.send(f'{ctx.author.mention} slapped {member.mention} for {reason}.')

	@slap_member.error
	async def slapMember_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.channel.send('Member not found, maybe they will join us in the future.')

	@command(name = 'echo', aliases = ['say'])
	@cooldown(1, 15, BucketType.guild)
	async def echoMessage(self, ctx, *, message):
		await ctx.message.delete()
		await ctx.channel.send(message)

	@command(name = 'fact')
	@cooldown(3, 60, BucketType.guild)
	async def animal_fact(self, ctx, animal : str):
		URL = f'https://some-random-api.ml/facts/{animal.lower()}'

		alter = 'birb' if animal.lower() == 'bird' else animal.lower()

		image_url = f'https://some-random-api.ml/img/{alter}'

		async with request('GET', image_url, headers = {}) as response:
			if response.status == 200:
				data = await response.json()
				image = data["link"]
			else:
				image = None

		async with request('GET', URL, headers={}) as response:
			if response.status == 200:
				data = await response.json()

				embed = Embed(title = f'{animal.title()} fact', description = data['fact'], colour = 0x19D900)

				if image is not None:
					embed.set_image(url = image)

				await ctx.channel.send(embed = embed)

			else:
				await ctx.channel.send(f'Returned {response.status} status, no further information.')

		
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up('fun')

def setup(bot):
	bot.add_cog(Fun(bot))