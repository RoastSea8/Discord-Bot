import discord
from discord.ext import commands 
import requests
from bs4 import BeautifulSoup

class Define(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="provides definitions from Urban Dictionary")
    async def define(self, ctx, *, words):
        words = words.lower()
        words = words.replace(' ', '%20')
        r = requests.get(f"http://www.urbandictionary.com/define.php?term={words}")
        soup = BeautifulSoup(r.content, 'lxml')
        try:
            def_header = soup.find("a",attrs={"class":"word text-3xl text-denim font-bold font-serif"}).text
            meaning = soup.find("div",attrs={"class":"meaning my-4"}).text
            for br in soup.find_all("br"):
                br.replace_with("\n")
            example = soup.find("div",attrs={"class":"example italic mb-4"}).text
            contributor = soup.find("div",attrs={"class":"contributor font-bold mb-4"}).text
            up_votes = soup.find("span",attrs={"class":"text-xs font-bold ml-2 count"}).text
            down_votes = soup.find("span",attrs={"class":"text-xs font-bold ml-2 count"}).text
            embed = discord.Embed(
                title=f"{def_header}",
                url=f"http://www.urbandictionary.com/define.php?term={words}",
                description=f'**Definition**: {meaning}\n\n**Example**:\n*{example}*\n\n{contributor}'
            )
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"👍 {up_votes} | 👎 {down_votes}")
            await ctx.send(embed=embed)
        except:
            words = words.replace(' ', '%20')
            url = f"http://www.urbandictionary.com/define.php?term={words}"
            embed = discord.Embed(title="", description=f"[enter a different term g]({url})")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Define(bot))