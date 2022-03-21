import json
import os
import random
import logging
import aiohttp
from random import randrange
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, guild_only
from discord.utils import get
import asyncio
import sys
import requests
import re
from bs4 import BeautifulSoup
from googletrans import Translator
from cogs.define import Define
from cogs.howdoi import Howdoi
from cogs.jokes import Jokes
from cogs.meme import Meme
from cogs.music import Music
from cogs.uptime import Time
from cogs.calculus import Calculus
from cogs.hangman import Hangman
from cogs.scramble import Scramble
from cogs.sfhs_cal import Calendar
sys.path.append(".")
try:
    import discord
except ImportError:
    import pip
    pip.main(['install', 'discord'])
    import discord

try:
    with open('config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    with open('config.json', 'w') as f:
        config = {}
        print("config file created.")
        json.dump({'discord_token': '', 'response': '', 'words': ['']}, f)

desc = """
Simple moderation bot.
"""

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=commands.when_mentioned_or(','), help_command=None, intents=intents)


# help command
@bot.command(name="help", brief="shows this message", description="shows this message")
async def help_(ctx):
    colors = [0x4ef207, 0x6f5df0, 0x40ffcf, 0xa640ff, 0xe00d6c, 0xb2e835]
    color = random.choice(colors)
    embed = discord.Embed(
        title="Kermit's commands", url="https://en.wikipedia.org/wiki/Kermit_the_Frog",
        description="React with the following emojis to see their respective commands",
        color=color
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.add_field(name="Home Page", value="🏠", inline=False)
    embed.add_field(name="Music", value="🎵", inline=False)
    embed.add_field(name="Games", value="🎮", inline=False)
    embed.add_field(name="Memes and Stupidities", value="🤡", inline=False)
    embed.add_field(name="Intellectual Tools", value="🤔", inline=False)
    embed.add_field(name="Others", value="🦦", inline=False)
    embed.add_field(name="DM feature", value="try to DM me!", inline=True)
    embed.set_thumbnail(url=config['thumbnail_url'])
    embed.set_footer(text=f"Information requested by: {ctx.author.display_name}")
    help_cmd = await ctx.send(embed=embed)
    await help_cmd.add_reaction('🏠')
    await help_cmd.add_reaction('🎵')
    await help_cmd.add_reaction('🎮')
    await help_cmd.add_reaction('🤡')
    await help_cmd.add_reaction('🤔')
    await help_cmd.add_reaction('🦦')

used_commands = []
for command in Define.__cog_commands__:
    used_commands.append(command)
for command in Howdoi.__cog_commands__:
    used_commands.append(command)
for command in Jokes.__cog_commands__:
    used_commands.append(command)
for command in Meme.__cog_commands__:
    used_commands.append(command)
for command in Music.__cog_commands__:
    used_commands.append(command)


# help event
@bot.event
async def on_reaction_add(reaction, user):
    channel = await bot.fetch_channel(reaction.message.channel.id)
    if user != bot.user:
        help_msg = await channel.fetch_message(reaction.message.id)
        if help_msg.embeds:
            if help_msg.embeds[0].title:
                if "Kermit's commands" == help_msg.embeds[0].title[:17]:
                    if reaction.emoji == '🏠':
                        embed = discord.Embed(
                            title="Kermit's commands", url="https://en.wikipedia.org/wiki/Kermit_the_Frog",
                            description="React with the following emojis to see their respective commands",
                            color=help_msg.embeds[0].color
                        )
                        embed.add_field(name="Home Page", value="🏠", inline=False)
                        embed.add_field(name="Music", value="🎵", inline=False)
                        embed.add_field(name="Games", value="🎮", inline=False)
                        embed.add_field(name="Memes and Stupidities", value="🤡", inline=False)
                        embed.add_field(name="Intellectual Tools", value="🤔", inline=False)
                        embed.add_field(name="Others", value="🦦", inline=False)
                        embed.add_field(name="DM feature", value="try to DM me!", inline=True)
                        embed.set_thumbnail(url=config['thumbnail_url'])
                    elif reaction.emoji == '🎮':
                        embed = discord.Embed(title="Kermit's commands 🎮", description=f"__{len(Hangman.__cog_commands__) + len(Scramble.__cog_commands__)} Game Commands__", color=help_msg.embeds[0].color)
                        for command in Hangman.__cog_commands__:
                            embed.add_field(name=command, value=command.description, inline=True)
                        for command in Scramble.__cog_commands__:
                            embed.add_field(name=command, value=command.description, inline=True)
                    elif reaction.emoji == '🎵':
                        embed = discord.Embed(title="Kermit's commands 🎵", description=f"__{len(Music.__cog_commands__)} Music Commands__", color=help_msg.embeds[0].color)
                        for command in Music.__cog_commands__:
                            if (command == Music.change_volume):
                                embed.add_field(name="volume", value="volume <num>", inline=True)
                            embed.add_field(name=command, value=command.description, inline=True)
                    elif reaction.emoji == '🤡':
                        embed = discord.Embed(title="Kermit's commands 🤡", description=f"__{len(Meme.__cog_commands__) + len(Jokes.__cog_commands__)} Meme Commands__", color=help_msg.embeds[0].color)
                        for command in Meme.__cog_commands__:
                            embed.add_field(name=command, value=command.description, inline=False)
                        for command in Jokes.__cog_commands__:
                            embed.add_field(name=command, value=command.description, inline=False)
                    elif reaction.emoji == '🤔':
                        length = len(Define.__cog_commands__) + len(Howdoi.__cog_commands__) + len(Calculus.__cog_commands__) + len(Calendar.__cog_commands__)
                        embed = discord.Embed(title="Kermit's commands 🤔", description=f"__{length} Intellectual Commands__", color=help_msg.embeds[0].color)
                        for command in Define.__cog_commands__:
                            embed.add_field(name=command, value=command.description, inline=True)
                        for command in Howdoi.__cog_commands__:
                            embed.add_field(name=command, value=command.description, inline=True)
                        for command in Calculus.__cog_commands__:
                            embed.add_field(name=command, value=command.description, inline=True)
                        for command in Calendar.__cog_commands__:
                            embed.add_field(name=command, value=command.description, inline=True)
                        for command in bot.commands:
                            if (command == map):
                                embed.add_field(name=command, value=command.description, inline=True)
                            if (command == schedule):
                                embed.add_field(name="schedule", value=command.description, inline=True)
                            if (command == activity_schedule):
                                embed.add_field(name="activity", value=command.description, inline=True)
                            if (command == special_schedule):
                                embed.add_field(name="special", value=command.description, inline=True)
                    elif reaction.emoji == '🦦':
                        embed = discord.Embed(title="Kermit's commands 🦦", description=f"__{len(bot.commands) - 10} Other Commands__", color=help_msg.embeds[0].color)
                        for command in Time.__cog_commands__:
                            embed.add_field(name=command, value=command.description, inline=True)
                        for command in bot.commands:
                            if (command != say and command != reply and command != speak and command != _servers and command != secret and command != edit and command != schedule and command != _commands and command != load and command != unload and command != _reload):
                                if command not in used_commands:
                                    if (command == delete):
                                        embed.add_field(name="delete (admins only)", value=command.description, inline=True)
                                    elif (command == proll):
                                        embed.add_field(name="proll (number of options)", value=command.description, inline=True)
                                    else:
                                        embed.add_field(name=command, value=command.description, inline=True)
                    embed.set_author(name=user.display_name, icon_url=user.avatar_url)
                    embed.set_footer(text=f"Information requested by: {user.display_name}")
                    await help_msg.edit(embed=embed)
                    try:
                        await help_msg.remove_reaction(reaction, user)
                    except:
                        pass
        else:
            return


@bot.command(description="disables commands")
@commands.is_owner()
async def disable(ctx, cmd):
    for command in bot.commands:
        if str(command) == cmd:
            command.update(enabled=False)
            await ctx.send(f"{command} disabled")


@bot.command(description="enables commands")
@commands.is_owner()
async def enable(ctx, cmd):
    for command in bot.commands:
        if str(command) == cmd:
            command.update(enabled=True)
            await ctx.send(f"{command} enabled")


@bot.command(description="clears entered amount of messages")
@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
async def delete(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)


@bot.command(description="deletes channel", aliases=["d_c"])
@commands.is_owner()
async def delete_channel(ctx, channel_name):
    await ctx.send(f"Are you sure you want to delete channel {channel_name}?")
    msg = await bot.wait_for(event='message', check=lambda message: message.author == ctx.author, timeout=10.0)
    if msg.content == "yes" or msg.content == "Yes":
        existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        if existing_channel is not None:
            await existing_channel.delete()
            await ctx.send(f"{channel_name} deleted")
        else:
            await ctx.send(f'No channel named, "{channel_name}", was found')
    else:
        await ctx.send(f"deletion of {channel_name} canceled")


@bot.command(description="returns images of input from Google")
async def search(ctx, *, query):
    res = requests.get("https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch")
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all("img")[1:4]
    for i in results:
        await ctx.send(i["src"])


editMsgList = []
editMsgs = []
# text-through command
@bot.command()
@commands.is_owner()
async def say(ctx, arg1, *, arg):
    global editMsgList, editMsgs
    if arg1.isnumeric():
        arg1 = int(arg1)
    else:
        arg1 = config[arg1]
    channel = bot.get_channel(arg1)
    try:
        await channel.send(ctx.message.attachments[0].url)
    except IndexError:
        pass
    await channel.trigger_typing()
    msg = await channel.send(arg)
    try:
        editMsgList.append((arg1, msg.id))
    except:
        pass
    try:
        editMsgs.append((msg.content, msg.guild.name))
    except:
        pass


# edit command
@bot.command()
@commands.is_owner()
async def edit(ctx, msgIndex: int, *, edited):
    global editMsgList
    try:
        _channel = editMsgList[-msgIndex][0]
        channel = bot.get_channel(_channel)
        message = await channel.fetch_message(editMsgList[-msgIndex][1])
        await message.edit(content=str(edited))
    except:
        return


@bot.command()
@commands.is_owner()
async def editList(ctx):
    global editMsgs
    await ctx.send(list(reversed(editMsgs)))


# speak command
@bot.command()
@commands.is_owner()
async def speak(ctx, *, arg):
    try:
        await ctx.send(arg, tts=True)
    except:
        pass


# reply command
@bot.command()
@commands.is_owner()
async def reply(ctx, arg1, *, arg):
    if arg1.isnumeric():
        user_id = int(arg1)
    else:
        user_id = config[arg1]
    user = await bot.fetch_user(user_id)
    await user.send(arg)


# poll command
@bot.command(brief="sets up a poll", description="sets up a poll")
async def poll(ctx, *, arg):
    global editMsgList, editMsgs
    # await ctx.send('{} Poll started by {}: '.format(ctx.message.guild.roles[0], ctx.author.mention))
    await ctx.message.delete()
    await ctx.send('Poll started by {}: '.format(ctx.author.mention))
    m = await ctx.send('`{}`'.format(arg))
    await m.add_reaction('👍')
    await m.add_reaction('👎')
    await m.add_reaction('🤷')
    try:
        editMsgList.append((ctx.channel.id, m.id))
    except:
        pass
    try:
        editMsgs.append((arg, m.guild.name))
    except:
        pass

poll_options = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶',
                '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']


# pro poll command
@bot.command(description="sets up a poll with entered number of options")
async def proll(ctx, args: int, *, content):
    await ctx.message.delete()
    await ctx.send('Poll started by {}: '.format(ctx.author.mention))
    m = await ctx.send('`{}`'.format(content))
    for i in range(args):
        await m.add_reaction(poll_options[i])


# suggests command
@bot.command(brief="sends feature suggestions to Kermit", description="sends feature suggestions to Kermit")
async def suggest(ctx, *, suggestion):
    channel = bot.get_channel(config['suggestions_channel'])
    await channel.send(f'`{(str(ctx.author)[:-5])} suggests`: {suggestion}')
    try:
        await channel.send(ctx.message.attachments[0].url)
    except IndexError:
        pass
    _id = ctx.author.id
    user = await bot.fetch_user(_id)
    await user.send('Your suggestion has been received!')


# troll token command
@bot.command(brief="provides Kermit's token", description="provides Kermit's token")
async def token(ctx):
    await ctx.send("Here's my token: `{}`\nHave fun!".format(config['troll_token']))


# provides invite link
@bot.command(brief='provides link to invite Kermit into a server', description='provides link to invite Kermit into a server')
async def invite(ctx):
    app_info = await bot.application_info()
    perms = discord.Permissions.none()
    url = discord.utils.oauth_url(app_info.id, perms)
    embed = discord.Embed(
        title="Discord - Invite Link",
        url=f'{url}',
        description="Kermit is a Discord bot containing a multitude of commands for entertainment and educational purposes."
    )
    embed.set_image(url=config['invite_img_url'])
    await ctx.send(embed=embed)


# provides American map pic
@bot.command(brief="sends American map pic", description="shows picture of American map")
async def map(ctx):
    await ctx.send(file=discord.File('media/USmap.gif'))


# provides school schedule pic
@bot.command(brief="sends school schedule b/g", description="sends school schedule b/g")
async def schedule(ctx):
    await ctx.send(file=discord.File('media/schedule3.png'))


# provides activity school schedule pic
@bot.command(brief="sends activity school schedule", description="sends activity school schedule", aliases=["a_schedule", "aschedule", "activity"])
async def activity_schedule(ctx):
    await ctx.send(file=discord.File('media/activitySchedule.png'))


# provides special school schedule pic
@bot.command(brief="sends special school schedule (white/virtual)", description="sends special school schedule (white/virtual)", aliases=["s_schedule", "sschedule", "special"])
async def special_schedule(ctx):
    await ctx.send(file=discord.File('media/specialSchedule.png'))


# get names of servers that bot belongs to
@bot.command()
@commands.is_owner()
async def _servers(ctx):
    await ctx.send('Servers connected to:')
    for guild in bot.guilds:
        await ctx.send(f"{guild.name} - {guild.owner.name}")


# prints out all commands with descriptions
@bot.command()
@commands.is_owner()
async def _commands(ctx):
    for command in bot.commands:
        await ctx.send(f'{command}: {command.description}')


# responding to servers
@bot.command()
@commands.is_owner()
async def secret(ctx, guild_name, channel_name, *, message):
    for guild in bot.guilds:
        guild_name = guild_name.replace('-', ' ')
        if guild_name == (str(guild.name).lower()):
            try:
                channel = get(guild.text_channels, name=channel_name)
            except:
                await ctx.send(f"channel not found in {guild}")
                await ctx.send(channel.name)
                return
            async with channel.typing():
                await asyncio.sleep(0.8)
                await channel.send(message)

emojis = ['🤡', '😐', '😳', '🧢', '🏳️‍🌈', '💩', '😈', '🤓']
servers = ['BotTestingServer', 'denny & danny friends']


@bot.event
async def on_message(message):
    channel = message.channel
    username = message.author.name
    user_id = message.author.id

    if message.author == bot.user:
        return

    await bot.process_commands(message)

    # emoji = random.choice(emojis)
    # last_emote = emoji
    # if (emoji == last_emote):
    #     emoji = random.choice(emojis)
    # if (randrange(15) == 1):
    #     await message.add_reaction(emoji)
    #     if (randrange(6) == 1):
    #         emoji = random.choice(emojis)
    #         await message.add_reaction(emoji)

    if str(bot.user.id) in message.content:
        ctx = await bot.get_context(message)
        await ctx.invoke(help)

    channel = bot.get_channel(config['bot_testing_channel'])
    if message.guild is None and message.author != bot.user:
        await channel.send(f'`{(str(message.author)[:-5])}`: {message.content}')
        try:
            await channel.send(message.attachments[0].url)
        except IndexError:
            pass

    _guild = bot.get_guild(config['bot_testing_server'])
    for server in servers:
        if str(message.guild.name) == server:
            return
    gld_name = (str(message.guild.name)).lower()
    gld_name = re.sub("[^0-9a-zA-Z]+", "-", gld_name)
    server_channel = get(_guild.text_channels, name=gld_name)
    if server_channel is None:
        category = discord.utils.get(_guild.categories, name="servers")
        gld_name = (str(message.guild.name)).lower()
        gld_name = re.sub("[^0-9a-zA-Z]+", "-", gld_name)
        await _guild.create_text_channel(gld_name, category=category)
        server_channel = get(_guild.text_channels, name=gld_name)
    embed = discord.Embed(
        title=f'{message.channel}', description=f'{message.content}'
    )
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    await server_channel.send(embed=embed)
    try:
        await server_channel.send(message.attachments[0].url)
    except IndexError:
        pass
    embeds = message.embeds
    if not embeds:
        return
    else:
        embed = (message.embeds)[0]
        await server_channel.send(embed=embed)


# missing arguments event
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send('Bot is missing permissions.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry, you do not have the role permissions to use this command!')
    if isinstance(error, commands.NotOwner):
        await ctx.send('Sorry, only the owner of Kermit has access to this command.')


# prints out if bot has been added into another server
@bot.event
async def on_guild_join(guild):
    channel = await bot.fetch_channel(config['server_invites_channel'])
    await channel.send(f'Kermit has been added to: {guild}, owned by {guild.owner.name}')

    _guild = bot.get_guild(config['bot_testing_server'])

    category = discord.utils.get(_guild.categories, name="servers")
    gld_name = (str(guild.name)).lower()
    gld_name = re.sub("[^0-9a-zA-Z]+", "-", gld_name)
    server_channel = get(_guild.text_channels, name=gld_name)
    if server_channel is None:
        await _guild.create_text_channel(gld_name, category=category)


@bot.event
async def on_guild_remove(guild):
    channel = await bot.fetch_channel(config['server_invites_channel'])
    await channel.send(f'Kermit has been kicked from: {guild} - {guild.owner.name}')


@bot.event
async def on_guild_update(before, after):
    channel = await bot.fetch_channel(config['server_invites_channel'])
    if before.name != after.name:
        await channel.send(f'{before.name} was changed to {after.name}')

    _guild = bot.get_guild(config['bot_testing_server'])
    category = discord.utils.get(_guild.categories, name="servers")
    old_gld_name = (str(before.name)).lower()
    old_gld_name = old_gld_name.replace(' ', '-')
    new_gld_name = (str(after.name)).lower()
    new_gld_name = re.sub("[^0-9a-zA-Z]+", "-", new_gld_name)
    server_channel = get(_guild.text_channels, name=old_gld_name)
    await server_channel.edit(name=new_gld_name)


# kick command
@bot.command(description="kicks members: `kick <member>`")
@guild_only()
@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason = reason)
    await ctx.send(f'Kicked {member.mention}')


# ban command
@bot.command(description="bans members: `ban <member> <reason>(optional)`")
@guild_only()
@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason = reason)
    if reason is None:
        await ctx.send(f'Banned {member.mention}')
    else:
        await ctx.send(f"Banned {member.mention}\nReason: {reason}")


# unban command
@bot.command(description="unbans members: `unban <name#discriminator>`")
@guild_only()
@commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


# language translate command
@bot.command(description="<lang to translate to> <message>", aliases=['tr', 't', 'tra', 'tran', 'trans'])
async def translate(ctx, lang, *, msg):
    translator = Translator()
    translation = translator.translate(msg, dest=lang)
    await ctx.send(translation.text)


# load cog command
@bot.command(description="loads extensions")
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} loaded successfully.')


# load cog command
@bot.command(description="reloads extensions")
@commands.is_owner()
async def _reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} reload successfully.')


# unload cog command
@bot.command(description="unloads extensions")
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} unloaded successfully.')

# loading all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    app_info = await bot.application_info()
    bot.owner = app_info.owner
    print('Bot: {0.name}:{0.id}'.format(bot.user))
    print('Owner: {0.name}:{0.id}'.format(bot.owner))
    print('------------------')
    perms = discord.Permissions.none()
    perms.administrator = True
    url = discord.utils.oauth_url(app_info.id, perms)
    print('To invite me to a server, use this link\n{}'.format(url))

if __name__ == '__main__':
    try:
        bot.run(os.environ['token'])
    except KeyError:
        print("config not yet filled out.")
    except discord.errors.LoginFailure as e:
        print("Invalid discord token.")
