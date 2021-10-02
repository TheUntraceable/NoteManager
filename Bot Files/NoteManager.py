import motor.motor_asyncio
from json import load # Don't worry I'm not using JSON as a db.
import os


from discord.ext import commands
from discord import Intents


intents = Intents()
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix="nm!",intents=intents,case_insensitive=True)

bot.cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo:mongo@127.0.0.1:27017/")
bot.db = bot.cluster["notes"]["notes"]

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

with open("config.json") as f:
    config = load(f)

bot.load_extension("jishaku")

bot.run(config["token"])