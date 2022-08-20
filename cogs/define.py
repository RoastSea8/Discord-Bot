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
            current_url = r.url.replace('%20', '+')
            current_url = current_url[current_url.rfind('/'):]
            def_header = soup.find("a", attrs={"href": current_url}).text
            meaning = soup.find("div", attrs={"class": "break-words meaning mb-4"}).text
            for br in soup.find_all("br"):
                br.replace_with("\n")
            example = soup.find("div", attrs={"class": "break-words example italic mb-4"}).text
            contributor = soup.find("div", attrs={"class": "contributor font-bold"}).text
            up_votes = soup.find("span", attrs={"data-x-text": "thumbText('up')"}).text
            down_votes = soup.find("span", attrs={"data-x-text": "thumbText('down')"}).text
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