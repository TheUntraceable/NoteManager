from discord import Embed
from discord.ext import commands
from typing import Optional
class Notes(commands.Cog):
    def __init__(self,bot : commands.Bot):
        self.bot = bot

    @commands.group(name="notes",invoke_without_command=True,case_insensitive=True)
    async def notes(self,ctx : commands.Context) -> None:
        embed = Embed(title="Subcommands.",description="Below there are a list of subcommands.")
        embed.add_field(name=f"`{ctx.prefix}notes create`",value="This creates a note.")

        embed.add_field(name=f"`{ctx.prefix}notes update`",value="This updates the contents of a note.")

        embed.add_field(name=f"`{ctx.prefix}notes view`",value="This shows you all of your notes.")

        embed.add_field(name=f"`{ctx.prefix}notes delete`",value="This deletes a note.")

        await ctx.reply(embed=embed)

    @notes.command(name="create")
    async def create(self,ctx : commands.Context , category : str , * , contents : str):
        await self.open_account(ctx.author.id)
        
        categories = await self.bot.db.fetchval("SELECT categories FROM notes WHERE user_id = $1", str(ctx.author.id))

        if category not in categories:
            return await ctx.reply(f"{category} is not a valid category. The only categories you have are: {' '.join(categories)}")
        

        notes = await self.bot.db.fetchval("SELECT notes FROM notes WHERE user_id = $1", str(ctx.author.id))

        print(type(notes))       

        notes.append({"contents" : contents, "category" : category})

        await self.bot.db.execute("UPDATE notes SET notes = $1 WHERE user_id = $2", notes, str(ctx.author.id))
        
        await ctx.reply(f"Added a note with that contents to {category}")
    @notes.command(name="delete")
    async def delete(self,ctx : commands.Context, id : int):
        await self.open_account(ctx.author.id)
        
        notes = await self.bot.db.fetchval("SELECT notes FROM notes WHERE user_id = $1", str(ctx.author.id))
        
        if len(notes) < id:
            return await ctx.reply("You do not own any notes with that ID!")
        
        for dictionary in notes:
            if dictionary["id"] == id:
                notes.remove(dictionary)
                await self.bot.db.execute("UPDATE notes SET notes = $1 WHERE user_id = $2", notes,str(ctx.author.id)) 
        
        await ctx.reply("Deleted that note.")

    @notes.command(name="update")
    async def update(self, ctx: commands.Context, id : int, contents : str):
        await self.open_account(ctx.author.id)
        notes = await self.bot.db.fetchval("SELECT notes FROM notes WHERE user_id = $1", str(ctx.author.id))
        
        
        if len(notes) < id:
            return await ctx.reply("You do not own any notes with that ID!")

        for dictionary in notes:
            if dictionary["id"] == id:
                
                notes.remove(dictionary)
                await self.bot.db.execute("UPDATE notes SET notes = $1 WHERE user_id = $2", notes,str(ctx.author.id))

                notes.append({"contents" : contents, "category" : dictionary["category"], "id" : dictionary["id"]})
                await self.bot.db.execute("UPDATE notes SET notes = $1 WHERE user_id = $2", notes.append({"contents" : contents, "category" : dictionary["category"], "id" : dictionary["id"]}), str(ctx.author.id))
        
        await ctx.reply("Updated the contents of that note.")

    @notes.command(name="view")
    async def view(self,ctx : commands.Context):
        await self.open_account(ctx.author.id)

        data = await self.bot.db.fetchrow("SELECT * FROM notes WHERE user_id = $1",str(ctx.author.id))
        notes  = data.get("notes")

        m = ""

        for note in notes:
            for key,value in note.items():
                if len(m) < 4000:
                    m += f"**{key}** : {value}\n"
                else:
                    await ctx.author.send(m)

        if len(m) != 0 and m is not None:
            await ctx.author.send(m)
    
    async def open_account(self, user_id : str) -> None:
        data = await self.bot.db.fetch("SELECT * from notes WHERE user_id = $1", str(user_id))
        if not data:
            await self.bot.db.execute("INSERT INTO notes(notes, user_id , categories) VALUES ($1, $2, $3)", [] , str(user_id), [])

def setup(bot : commands.Bot):
    bot.add_cog(Notes(bot))