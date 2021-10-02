from discord import Embed
from discord.ext import commands

class Categories(commands.Cog):
    
    def __init__(self,bot : commands.Bot):
        self.bot = bot

    @commands.group(name="categories",invoke_without_command=True,case_insensitive=True)
    async def categories(self,ctx : commands.Context) -> None:

        embed = Embed(title="Subcommands.",description="Below there are a list of subcommands.")

        embed.add_field(name=f"`{ctx.prefix}categories create`",value="This creates a categories.")

        embed.add_field(name=f"`{ctx.prefix}categories update`",value="This updates the name of a category.")

        embed.add_field(name=f"`{ctx.prefix}categories view`",value="This shows you all of your categories.")

        embed.add_field(name=f"`{ctx.prefix}categories delete`",value="This deletes a category.")

        await ctx.reply(embed=embed)

    @categories.command(name="create")
    async def create(self,ctx : commands.Context , category : str):

        await self.open_account(ctx.author.id)
        
        categories = await self.get_data(ctx.author.id)
            
        for _category in categories["categories"]:
            if _category == category:
                return await ctx.reply("There is already a category under that name!")
        
       
        categories["categories"].append(category)

        await self.bot.db.update_one({"user_id" : ctx.author.id},{"$set" : {"categories" : categories["categories"]}})

        await ctx.reply(f"Added {category} to your categories.")

    @categories.command(name="delete")
    async def delete(self,ctx : commands.Context, name : str):

        await self.open_account(ctx.author.id)

        categories = await self.get_data(ctx.author.id)
        
        for category in categories["categories"]:
         
            if category == name:
                
                categories["categories"].remove(category)
                
                await self.bot.db.update_one({"user_id" : ctx.author.id},{"$set" : {"categories" : categories["categories"]}}) 
                
                return await ctx.reply("Deleted that category.")

        await ctx.reply(f"Couldn't find a category under the name of {name}")
    
    @categories.command(name="update")
    async def update(self, ctx: commands.Context, name : str, new_name : str):

        await self.open_account(ctx.author.id)

        categories = await self.get_data(ctx.author.id)

        for category in categories["categories"]:
        
            if category == name:

                categories["categories"].remove(category)
                categories["categories"].append(new_name)

                await self.bot.db.update_one({"user_id" : ctx.author.id}, {"$set" : {"categories" : categories["categories"]}})

        await ctx.reply("Updated the name of that category.")

    @categories.command(name="view")
    async def view(self,ctx : commands.Context):
        await self.open_account(ctx.author.id)

        categories = await self.get_data(ctx.author.id)

        m = ""

        for category in categories["categories"]:
            if len(m) < 4000:
                m += f"**{category}**\n"
            else:
                await ctx.author.send(m)

        try:
            await ctx.author.send(m)
        except:
            pass

    async def get_data(self,user_id : int) -> dict:
        
        data = await self.bot.db.find_one({"user_id" : user_id})
        
        if not data:
            return None
        
        return data

    async def open_account(self, user_id : str) -> None:
        data = await self.get_data(user_id)
        if not data:
            await self.bot.db.insert_one({"user_id" : user_id, "categories" : [], "notes" : []})
            
def setup(bot : commands.Bot):
    bot.add_cog(Categories(bot))