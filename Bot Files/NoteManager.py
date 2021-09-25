import asyncpg
import json # Don't worry I'm not using JSON as a db.
import os


from discord.ext import commands
from discord import Intents


intents = Intents()
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix="nm!",intents=intents)

async def create_db() -> None:
    bot.db = await asyncpg.create_pool(dsn="postgres://postgres:postgres@127.0.0.1:5432/")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS notes(notes json[], user_id text PRIMARY KEY, categories text[])")
    print("\nConnection Successful.\n")

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")


bot.loop.run_until_complete(create_db())

with open("config.json") as f:
    config = json.load(f)

bot.load_extension("jishaku")

bot.run(config["token"])