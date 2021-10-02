from discord import Embed
from discord.ext import commands

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
        
        categories = await self.get_data(ctx.author.id)

        if category not in categories["categories"]:

            return await ctx.reply(f"{category} is not a valid category. The only categories you have are: {' '.join(categories['categories'])}")
        
        categories["notes"].append({"contents" : contents, "category" : category,"id" : len(categories["notes"]) + 1})

    
        await self.bot.db.update_one({"user_id" : ctx.author.id},{"$set" : {"notes" : categories["notes"]}})

        await ctx.reply(f"Added that note to {category}")

    @notes.command(name="delete")
    async def delete(self,ctx : commands.Context, id : int):

        await self.open_account(ctx.author.id)
        
        notes = await self.get_data(ctx.author.id)
        
        if len(notes) < id:
            return await ctx.reply("You do not own any notes with that ID!")
        
        for dictionary in notes["notes"]:
            if dictionary["id"] == id:
                notes["notes"].remove(dictionary)
                await self.bot.db.update_one({"user_id" : ctx.author.id},{"$set" : {"notes" : notes["notes"]}})
        await ctx.reply("Deleted that note.")

    @notes.command(name="update")
    async def update(self, ctx: commands.Context, id : int, *,contents : str):
        await self.open_account(ctx.author.id)
        notes = await self.get_data(ctx.author.id)
        
        
        if len(notes) < id:
            return await ctx.reply("You do not own any notes with that ID!")

        for dictionary in notes["notes"]:

            if dictionary["id"] == id:
                
                notes["notes"].remove(dictionary)
                notes["notes"].append({"contents" : contents, "category" : dictionary["category"], "id" : dictionary["id"]})

                await self.bot.db.update_one({"user_id" : ctx.author.id},{"$set" : {"notes" : notes["notes"]}})

        await ctx.reply("Updated the contents of that note.")

    @notes.command(name="view")
    async def view(self,ctx : commands.Context):
        await self.open_account(ctx.author.id)

        data = await self.get_data(ctx.author.id)
        notes  = data.get("notes")

        m = ""

        for note in notes:
            for key,value in note.items():
                if len(m) < 4000:
                    m += f"**{key}** : {value}\n"
                else:
                    await ctx.author.send(m)

        if len(m) != 0 and m is not None:
            return await ctx.author.send(m)
        await ctx.reply("You don't have any notes!")
    async def get_data(self,user_id : int) -> dict:
        
        data = await self.bot.db.find_one({"user_id" : user_id})
        
        if not data:
            return None
        
        return data

    async def open_account(self, user_id : str) -> str:
        data = await self.get_data(user_id)
        if not data:
            await self.bot.db.insert_one({"user_id" : user_id, "categories" : [], "notes" : []})

def setup(bot : commands.Bot):
    bot.add_cog(Notes(bot))