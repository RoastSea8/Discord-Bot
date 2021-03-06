import discord
from discord.ext import commands
import howdoi
import os
from subprocess import PIPE, run
from guesslang import Guess

guess = Guess()

class howdoi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(description="answers your programming question from StackOverflow")
    async def howdoi(self, ctx, *, question):
        def out(command):
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
            return result.stdout
        output = out("howdoi -a " + str(question))
        language = guess.language_name(output)
        try:
            output = output.split("================================================================================")
        except:
            pass
        for answer in output:
            await ctx.send(f'```{(language.lower())}\n{answer}```')       

def setup(bot):
    bot.add_cog(howdoi(bot))