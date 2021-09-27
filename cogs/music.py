from discord.ext import commands
from discord import Message
from discord import FFmpegPCMAudio
#from stations_adapter import get_stations as new_get_stations
#from stations_adapter import db_connect
#from stations_adapter import *
import random
import discord
import time, sqlite3

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._conn = self.db_connect(".\stations\internet_radio_database.db")
        self.available_locations = self.get_available_stations_locations()

    def db_connect(self, dbName):
        conn = None
        try:
            conn = sqlite3.connect(dbName)
            
        except sqlite3.Error as e:
            print("Uh Oh!: ", e)
        return conn 


    def get_available_stations_locations(self):
        
        stations_per_location = """SELECT places.locationID, places.title, places.country, 
                                   COUNT(stations.locationID) as number_of_stations FROM places LEFT JOIN stations on
                                   (places.locationID = stations.locationID) GROUP BY places.locationID HAVING number_of_stations > 0 ORDER BY number_of_stations;
        """
        c = self._conn.cursor()
        c.execute(stations_per_location)
        places = c.fetchall()
        print(places)
        return places

    def get_stations(self, locationID):
        query = f"""SELECT stations.stationID, stations.title, stations.url, places.title as city, places.country FROM stations 
                     LEFT JOIN places ON (stations.locationID = places.locationID) WHERE stations.locationID='{locationID}'; """
    
        c = self._conn.cursor()
        stations = c.execute(query).fetchall()
        return stations

    @commands.command()
    async def randoStation(self, ctx):
        print(random.choice(self.available_locations)[0])
        locationID = random.choice(self.available_locations)[0]
        stations = self.get_stations(locationID)
        station = random.choice(stations)
        answer = discord.Embed(title="Random Station",
                                            description=f"""`Station` : **{station[1]}**\n `City` : **{station[3]}**\n `Country` : **{station[4]}**\n`Link` : **{station[2]}**""",
                                            colour=0xff0000)
        
        await ctx.message.channel.send(embed=answer)
        channel = ctx.message.author.voice.channel
        await self.playMe(ctx, channel, station[2])
       
    async def playMe(self, ctx, channel, url):
        global player

        if not self.is_connected(ctx):
            try:
                player = await channel.connect() #Voice Client 
            except Exception as e:
                print(e)
        
        if player.is_playing():
            player.stop()
      
        player.play(FFmpegPCMAudio(url))

    def is_connected(self, ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    #create a player that plays a internet radio stream
    @commands.command()
    async def play(self, ctx: commands.Context, url:str):
        """Listen to a URL stream"""
        channel = ctx.message.author.voice.channel
        answer = discord.Embed(title="Playing URL Stream",
                                       description=f"""`URL` : **{url}**\n""",
                                       colour=0xff0000)
        await ctx.message.channel.send(embed=answer)
        await self.playMe(ctx, channel, url)

    @commands.command()
    async def stop(self, ctx):
        """Stop the music player."""
        player.stop()

    @commands.command()
    async def leave(self, ctx):
        """Tell the bot to leave the voice channel"""
        if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send('Your not in the same channel as me.')
    
def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))