# import discord, datetime
# from discord.ext import commands, tasks
# import json

# with open('config.json') as f:
#     config = json.load(f)

# class wednesday(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
    
#     @tasks.loop(hours=1)
#     async def time_checker(self):
#         self.channel = await self.bot.fetch_channel(config['g'])
#         self.time = datetime.datetime.now
#         if self.time().hour == 6:
#             if datetime.datetime.today().weekday() == 2:
#                 await self.channel.send(file=discord.File('images/wednesday_pic.png'))
    
#     @commands.Cog.listener()
#     async def on_ready(self):
#         await self.bot.wait_until_ready()
#         self.time_checker.start()

# def setup(bot):
#     bot.add_cog(wednesday(bot))