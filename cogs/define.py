import discord
from discord.ext import commands 
import urbdict

class Define(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="provides definitions from Urban Dictionary")
    async def define(self, ctx, *, words):
        words = words.lower()
        words = words.replace(' ', '%20')
        try:
            word_dict = urbdict.define(words)
            embed = discord.Embed(
                title=word_dict["word"],
                url=word_dict["url"],
                description=f'**Definition**: {word_dict["definition"]}\n\n**Example**:\n*{word_dict["example"]}*\n\n{word_dict["contributor"]}'
            )
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        except:
            words = words.replace(' ', '%20')
            url = f"http://www.urbandictionary.com/define.php?term={words}"
            embed = discord.Embed(title="", description=f"[enter a different term g]({url})")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Define(bot))
