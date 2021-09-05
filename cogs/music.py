from discord.ext import commands
from discord import Message
from discord import FFmpegPCMAudio
import random
import discord


class Music(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.stations = self.get_stations()

	def get_stations(self):
		ifile = open(".\src\\radio-garden.txt","r",encoding="utf8")
		lines = ifile.readlines()
		stations = {}

		for i in range(2,len(lines)):
			if "group-title" in lines[i]:
				pos = lines[i].find("group-title=")
				info = lines[i][pos+12:].strip().split(",")
				country = info[0].strip().replace('"','')
				station_name = info[1].strip()
				link = lines[i+1].strip()
				if country not in stations:
					stations[country] = [(station_name, link)]
				else:
					stations[country].append((station_name,link))
		ifile.close()
		return stations

	async def playMe(self, channel, url):
		global player
		try:
			player = await channel.connect()
		except Exception as e:
			print(e)
		player.play(FFmpegPCMAudio(url))

	@commands.command()
	async def randomStation(self, ctx: commands.Context):
		"""Listen to a random radio station."""
		country = random.choice(list(self.stations.keys()))
		station = random.choice(self.stations[country])
		answer = discord.Embed(title="Random Station",
                                       description=f"""`Station` : **{station[0]}**\n`Country` : **{country}**\n`Link` : **{station[1]}**""",
                                       colour=0xff0000)
		await ctx.message.channel.send(embed=answer)
		channel = ctx.message.author.voice.channel
		await self.playMe(channel, station[1])
		

	#create a player that plays a internet radio stream
	@commands.command()
	async def play(self, ctx: commands.Context, url:str):
		"""Listen to a URL stream"""
		channel = ctx.message.author.voice.channel
		answer = discord.Embed(title="Playing URL Stream",
                                       description=f"""`URL` : **{url}**\n""",
                                       colour=0xff0000)
		await ctx.message.channel.send(embed=answer)
		await self.playMe(channel, url)

	@commands.command()
	async def stop(self, ctx):
		"""Stop the music player."""
		player.stop()
    
def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))