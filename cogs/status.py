import discord
from discord.ext import commands, tasks
from itertools import cycle


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=5)
    async def change_status(self):
        await self.bot.change_presence(activity=(next(self.activity)))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        total_members = 0
        for guild in self.bot.guilds:
            total_members += guild.member_count
        self.status = ["wit yo emotions", ",help | @Kermit", f"{total_members} losers"] # ["in Alabamian bathrooms", 'ikezi cap',
                       # "foy play mc"]  # ,help | @Kermit, f"on {len(self.bot.guilds)} servers"

        self.activity = cycle([discord.Game(name=self.status[0]), discord.Activity(type=discord.ActivityType.listening,
                                                                                   name=(self.status[1])),
                               discord.Activity(type=discord.ActivityType.watching, name=(self.status[2]))])

        self.change_status.start()


def setup(bot):
    bot.add_cog(Status(bot))
