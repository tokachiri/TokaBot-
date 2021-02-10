from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, has_permissions, MissingPermissions
import discord
import random 
import json
import os
import asyncio
from itertools import cycle
from io import BytesIO

bot = commands.Bot(command_prefix="t!")
bot.sniped_messages = {}
bot.remove_command("help")

kiss = [
  "https://media2.giphy.com/media/bGm9FuBCGg4SY/giphy.gif","https://i.pinimg.com/originals/e3/4e/31/e34e31123f8f35d5c771a2d6a70bef52.gif",
  "https://acegif.com/wp-content/uploads/anime-kiss-m.gif",
  "https://i.imgur.com/So3TIVK.gif",
  "https://media1.giphy.com/media/oHZPerDaubltu/giphy.gif"
]
grabify = [
    "lovebird.guru", "trulove.guru", "dateing.club", "otherhalf.life",
    "shrekis.life", "headshot.monster", "gaming-at-my.best",
    "progaming.monster", "yourmy.monster", "screenshare.host",
    "imageshare.best", "screenshot.best", "gamingfun.me", "catsnthing.com",
    "mypic.icu", "catsnthings.fun", "curiouscat.club", "joinmy.site",
    "fortnitechat.site", "fortnight.space", "freegiftcards.co", "stopify.co",
    "leancoding.co", "grabify.link", "you.tube.com"
]

dice = [
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
]

status = cycle(["t!help | Made by Toka#8008",
                "t!help | Stop Reading This Status.",
                "t!help | 😏",
                "t!help | Child Friendly Since 1976!",
                "t!help | There are Secret Commands!",
                "t!help | This Bot is Terr- I mean Awesome!",
                "t!help | Oh no.. They're coming.. Hel-",
                "t!help | Please Pay my Ransom..",
                "t!help | Hacking Discord Since 1991!",
                "t!help | This Bot was Written in Python!",
                "t!help | OwO",
                "t!help | ZzzzzzZzzzzZzzz",
                "t!help | Who Woke me Up From My Nap!",
                "t!help | Don't Question Me.",
                "t!help | Ruffles Was Here B)",
                "t!help | Dale Yeah!",
                "t!help | Quack!",
                "t!help | Landen is Bald!",
                "t!help | w o w",
             ])

@bot.event
async def on_ready():
  print("This Bot is Up and Running!")
  await bot.change_presence(status=discord.Status.online)
  change_status.start()

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, id="795786263353229352")
    await bot.add_roles(member, role)

# Snipe Command

@bot.event
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id] = (message.content, message.author,
                                             message.channel.name,
                                             message.created_at)


@bot.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = bot.sniped_messages[
            ctx.guild.id]

    except:
        await ctx.channel.send("Nothing to snipe dummy.")
        return
    embed = discord.Embed(description=contents,
                          color=ctx.author.color,
                          timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}",
                     icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in #{channel_name}")

    await ctx.send(embed=embed)

# Ping Command

@bot.command()
async def ping(ctx):
  await ctx.send(f"Pong! `{round(bot.latency * 1000)}`ms")

# Purge Command

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

# Anti Bypass
@bot.listen("on_message")
async def el_message(message):
  for word in grabify:
    if word in message.content:
      await message.channel.purge(limit=1)
      msg = await message.channel.send(
          f"Nobody falls for those grabify links stupid. <@{message.author.id}>"
          )

# Say Command

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, arg):
      await ctx.channel.purge(limit=1)
      say_embed = discord.Embed(color=ctx.author.color,)
      say_embed.add_field(name="Somebody has Said -",value=f"{arg}")
      await ctx.send(embed=say_embed)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!(Missing Permmisions)")

# Rick Roll Command

@bot.command()
async def rickroll(ctx, arg):
  await ctx.channel.purge(limit=1)
  await ctx.send(f'You\'ve Been RickRolled by {ctx.message.author.mention}, {arg}!')
  await ctx.send('https://media4.giphy.com/media/Vuw9m5wXviFIQ/giphy.gif')

# Kis Command
@bot.command()
async def kiss(ctx, arg):
  await ctx.send(f'{ctx.message.author.mention} has given a kiss to {arg}!')
  await ctx.send('https://i.imgur.com/So3TIVK.gif')

# Dale Yeah! Command
@bot.command()
async def DaleYeah(ctx):
  await ctx.send("Denson says Dale Yeah!")
  await ctx.send("https://media.discordapp.net/attachments/779472056949276672/808478079319932968/Yoshi.gif?width=225&height=225")

# Rock Paper Scissors Command
@bot.command()
async def rps(ctx):
    rpsGame = ['rock', 'paper', 'scissors']
    await ctx.send(f"Rock, paper, or scissors? Choose wisely...")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

    user_choice = (await bot.wait_for('message', check=check)).content

    comp_choice = random.choice(rpsGame)
    if user_choice == 'rock' or 'Rock':
        if comp_choice == 'rock':
            await ctx.send(f'Well, that was weird. We tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Nice try, but I won that time!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Aw, you beat me. It won't happen again!\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'paper' or 'Paper':
        if comp_choice == 'rock':
            await ctx.send(f'The pen beats the sword? More like the paper beats the rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Oh, wacky. We just tied. I call a rematch!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Aw man, you actually managed to beat me.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'scissors' or 'Scissors':
        if comp_choice == 'rock':
            await ctx.send(f'HAHA!! I JUST CRUSHED YOU!! I rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Bruh. >: |\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Oh well, we tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}")       

# Nick Command
@bot.command(pass_context=True)
@commands.has_permissions(manage_nicknames=True)
async def setnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

@setnick.error
async def setnick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

# Slowmode Command
@bot.command()
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

# Ban Command
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban (ctx, member:discord.User=None, *, reason =None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself.. Just leave the server..")
        return
    if reason == None:
        reason = "For being a jerk!"
    message = f"You have been banned from {ctx.guild.name} for {reason}"
    await member.send(message)
    ban_embed = discord.Embed(colour = discord.Colour.red()
    )
    ban_embed.add_field(name="Banned!",value=f"{member} was banned from {ctx.guild.name} for {reason}!")
    await ctx.send(embed=ban_embed)
    await member.ban(reason = reason)

@ban.error
async def ban_error(error, ctx):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await bot.send_message(ctx.message.channel, text)

# UnBan Command
@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            unban_embed = discord.Embed(colour = discord.Colour.green()
            )
            unban_embed.add_field(name="Unbanned!",value=f"{user} has been unbanned!")
            ctx.send(embed=unban_embed)
            return

# Kick Command
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick (ctx, member:discord.User=None, *, reason =None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot kick yourself.. Just leave the server..")
        return
    if reason == None:
        reason = "For being a jerk!"
    message = f"You have been kicked from {ctx.guild.name} for {reason}"
    await member.send(message)
    # await ctx.guild.ban(member, reason=reason)
    kick_embed = discord.Embed(colour = discord.Colour.red()
    )
    kick_embed.add_field(name="Kicked!",value=f"{member} was kicked from {ctx.guild.name} for {reason}!")
    await ctx.send(embed=kick_embed)
    await member.kick(reason = reason)

# CoinFlip Command
@bot.command(aliases=['cf','coin'])
async def coinflip(ctx):
  coinsides = ['Heads', 'Tails']
  await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

# Nuke Command
@bot.command()
@commands.has_permissions(administrator = True)
async def nuke(ctx, channel: discord.TextChannel = None):
    if channel == None: 
        await ctx.send("You did not mention a channel!")
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel is not None:
        new_channel = await nuke_channel.clone(reason="Has been Nuked!")
        await nuke_channel.delete()
        await new_channel.send("THIS CHANNEL HAS BEEN NUKED!")
        await ctx.send("Nuked the Channel sucessfully!")

    else:
        await ctx.send(f"No channel named {channel.name} was found!")

# Random Integer Command
@bot.command()
async def randint(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and \
               msg.channel == ctx.channel

    await ctx.send("Type a number.")
    msg1 = await bot.wait_for("message", check=check)
    await ctx.send("Type a second, larger number.")
    msg2 = await bot.wait_for("message", check=check)
    x = int(msg1.content)
    y = int(msg2.content)
    if x < y:
        value = random.randint(x,y)
        await ctx.send(f"You got {value}.")
    else:
        await ctx.send(":warning: Please ensure the first number is smaller than the second number.")

# Help Commands
@bot.command()
async def help(ctx):
  author = ctx.message.author

  help_tableofcontents_embed = discord.Embed(colour = discord.Colour.blue()
  )
  help_tableofcontents_embed.set_author(name="BOT PREFIX = t!")
  help_tableofcontents_embed.add_field(name="1 - Moderation",value="Do t!h1 to figure out all of the Moderation Commands and what they do! Some of these commands require some permissions in order to be used!")
  help_tableofcontents_embed.add_field(name="2 - Fun",value="Do t!h2 to figure out all of the Fun commands.")
  help_tableofcontents_embed.set_footer(text="There are lots for Hidden Commands! Look on Toka's Github for the Bot's Code!")

  await ctx.send(embed=help_tableofcontents_embed)

# Help Command - Moderation
@bot.command()
async def h1(ctx):
  author = ctx.message.author

  mod_help = discord.Embed(colour = discord.Colour.red()
  )
  mod_help.set_author(name="Moderation Commands")
  mod_help.add_field(name="Ban",value="Bans a Mentioned User.")
  mod_help.add_field(name="Kick",value="Kicks a Mentioned User.")
  mod_help.add_field(name="Purge",value="Purges the Chat.")
  mod_help.add_field(name="Nuke",value="Nukes a Channel.(You may have to move the channel back to its original position)")
  mod_help.add_field(name="UnBan", value="UnBans a User. (Format - BannedUser#0000)")
  mod_help.add_field(name="Slowmode", value="Sets the slowmode in seconds.")
  mod_help.add_field(name="SetNick", value="Sets a Nickname for another user!")

  await ctx.send(embed=mod_help)

# Help Command - Fun
@bot.command()
async def h2(ctx):
  author = ctx.message.author

  fun_help = discord.Embed(colour = discord.Colour.green()
  )
  fun_help.set_author(name="Fun Commands")
  fun_help.add_field(name="Say",value="Forces the bot to say things against it's will.")
  fun_help.add_field(name="RickRoll",value="We/'re no strangers to love, You know the Rules and so do I, A full commitment is what I'm thinking of... RickRoll someone!")
  fun_help.add_field(name="RPS",value="Play Rock Paper Scissors with this Bot. (There are some bugs)")
  fun_help.add_field(name="RandInt", value="Choose 2 numbers and generate a Random Number between both of them.")
  fun_help.add_field(name="CoinFlip", value="Flips a Coin for you!")

  await ctx.send(embed=fun_help)

bot.run('ODA2OTIxMjAzMjk0MDExNDgz.YBwd7g.04OQA0kGWwdfGEB8aMsWGsCQE5I')
