from discord import DMChannel
from discord.ext import commands
from datetime import datetime
class Monitoring(commands.Cog):
    def __init__(self,bot : commands.Bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self,message): 
        if message.author.bot:
            return
        
        if message.content.lower().startswith("nm!") and not isinstance(message.channel,DMChannel):
            print(f"[COMMAND] [{message.guild.name} - {message.guild.id} [{datetime.now()}] {message.author} ({message.author.id}) - {message.content.lower()}.\n")
        
            return
        
        elif message.content.lower().startswith("nm!") and isinstance(message.channel,DMChannel):
            print(f"[COMMAND] [IN DM] [{datetime.now()}] {message.author} ({message.author.id}) - {message.content.lower()}.\n")
        
            return
        if isinstance(message.channel, DMChannel):
            print(f"[MESSAGE] [IN DM] [{message.guild.name} - {message.guild.id} [{datetime.now()}] {message.author} ({message.author.id}) - {message.content.lower()}.\n")

    @commands.Cog.listener()
    async def on_connect(self):
        print(f"{self.bot.user} has connected to Discord!\n")

    @commands.Cog.listener()
    async def on_ready(self):

        print(f'{self.bot.user} is ready!\n')

        print(f"ID - {self.bot.user.id}\n")

        print(f"Connected to {len(self.bot.guilds)} servers which have {len(self.bot.users)} members!\n") 

    @commands.Cog.listener()
    async def on_shard_connect(self,shard_id):
        print(f"Shard connected : {shard_id}\n")

    @commands.Cog.listener()
    async def on_disconnect(self):
        print(f"{self.bot.user} has disconnected from Discord!\n")

    @commands.Cog.listener()
    async def on_shard_disconnect(self,shard_id):
        print(f"{shard_id} has disconnected from Discord!\n")

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id):
        print(f"Shard {shard_id} is ready!\n")

    @commands.Cog.listener()
    async def on_resumed(self):
        print(f"{self.bot.user} has reconnected to Discord!\n")

    @commands.Cog.listener()
    async def on_shard_resumed(self, shard_id):
        print(f"{shard_id} has reconnected to Discord!\n")

def setup(bot : commands.Bot):
    bot.add_cog(Monitoring(bot))