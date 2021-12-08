#Imports

import discord
import discord.ext
import asyncio
from discord.ext import commands

#Variables

color = int('771aa2', 16)
suggestchannel = "suggestions"
loggingchannel = "audit-log"
rrchannel = "⭐-roles"
reactionmsgs = []
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.reactions = True
client = commands.Bot(command_prefix = '.v ', intents=intents, case_insensitive=True)
client.remove_command("help")

#Random Commands

@client.command(name='members')
async def get_members(ctx):
	guild = ctx.message.guild
	gname = guild.name
	ms = guild.members
	tnum = len(ms)
	unum = 0
	bnum = 0
	ulist = ''
	blist = ''
	for m in ms:
		if m.bot:
			blist += m.name
			blist += "\n"
			bnum += 1
		else:
			ulist += m.name
			ulist += "\n"
			unum += 1
	embed = discord.Embed(title=f"{gname} Members", description=f"All members in {gname}.")
	embed.add_field(name="Amount", value=f"Bots - {bnum}\nUsers - {unum}\nTotal - {tnum}")
	embed.add_field(name="Users", value=ulist, inline=False)
	embed.add_field(name="Bots", value=blist, inline=False)
	await ctx.message.channel.send(embed=embed)

@client.command(name="inv")
async def invite(ctx):
	invlink = "<https://bit.ly/3rjOmo4>"
	embed = discord.Embed(title="Apply to add Vestal to your server!", description="The bot is in progress.", color=color)
	embed.add_field(name="Link", value=invlink, inline=False)
	await ctx.message.channel.send(embed=embed)
	await ctx.message.delete()

@client.command(name="purge")
@commands.has_permissions(administrator=True)
async def purge(ctx, a="all"):
	try:
		a = int(a) + 1
	except:
		pass
	if type(a) == int and a > 0:
		messages = await ctx.message.channel.history(limit=a).flatten()
		for m in messages:
			await m.delete()
			if len(messages) < 1:
				break
	elif a == 'all':
		messages = await ctx.message.channel.history().flatten()
		for m in messages:
			await m.delete()
			if len(messages) < 1:
				break
			await asyncio.sleep(0.1)
	else:
		m = await ctx.message.channel.send("No")
		await ctx.message.delete()
		await asyncio.sleep(5)
		await m.delete()

@client.command(name='spam')
async def spam(ctx, msg, amount:int):
	amount2=amount
	while amount > 0:
		await ctx.message.channel.send(msg)
		amount-=1
	embed = discord.Embed(title="Spamming Finished", description=f"{msg} has been sent {amount2} times")
	await ctx.message.channel.send(embed=embed)

@client.command(name='help')
async def help(ctx):
	embed=discord.Embed(name="Commands", description='List of commands in Vestal',color=color)
	await ctx.message.channel.send(embed=embed)

@client.command(name='emb')
async def emb(ctx, title, description, colour=color):
	embed = discord.Embed(title=title, description=description,color=colour)
	await ctx.message.channel.send(embed=embed)
	await ctx.message.delete()

@client.command(name='suggest')
async def suggest(ctx, title, description):
	embed = discord.Embed(title=title, description=description,color=color)
	channel = discord.utils.get(ctx.guild.channels, name=suggestchannel)
	await channel.send(embed=embed)

@client.command(pass_context = True)
async def poll(ctx, question, *options: str):
    if len(options) <= 1:
        await ctx.message.channel.send("```Error! A poll must have more than one option.```")
        return
    if len(options) > 2:
        await ctx.message.channel.send("```Error! Poll can have no more than two options.```")
        return

    reactions = ['👍', '👎']

    description = []
    for x, option in enumerate(options):
        description += ' {} - {}\n\n'.format(reactions[x], option)

    embed = discord.Embed(title = question, color =color, description = ''.join(description))

    react_message = await ctx.message.channel.send(embed = embed)

    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)

    embed.set_footer(text='Poll ID: {}'.format(react_message.id))

    await react_message.edit(embed=embed)

@client.command(aliases=['rr','reactrole','rrole'])
async def reactionrole(ctx, react, role, *ms):
	msg = ""
	for m in ms:
		msg += m
	embed = discord.Embed(title="React to get ")
#Events

@client.event
async def on_ready():
	print(f"{client.user.name} is online")
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='your bs'))

@client.event
async def on_member_join(member):
	embed=discord.Embed(title='Look who showed up!', description=f"Welcome to {member.guild.name}, {member.name}. If you don't love this server, tell us how to improve it in #suggestions. If you do, then I recommend joining these, as well as applying to invite Vestal to your own server:\n\nServer 1 - <https://bit.ly/3FHCyzN>\nServer 2 - <https://bit.ly/3l1OeW4>\nVestal Invite - <https://bit.ly/3rjOmo4>\n\n:tada: Have fun!",color=color)
	embed2 = discord.Embed(title='Member Joined',description=member.mention,color=color)
	channel2 = discord.utils.get(member.guild.channels, name=loggingchannel)
	channel = await member.create_dm()
	await channel.send(embed=embed)
	await channel2.send(embed=embed2)

@client.event
async def on_member_remove(member):
	embed = discord.Embed(title='Member Left', description=member.mention,color=color)
	channel = discord.utils.get(member.guild.channels, name=loggingchannel)
	await channel.send(embed=embed)

@client.event
async def on_message_delete(message):
    embed = discord.Embed(title=f"{message.author.name} deleted a message",description=f"**Message sent by {message.author.mention} deleted in {message.channel.mention}**\n{message.content}", color=color)
    channel = discord.utils.get(message.channel.guild.channels, name=loggingchannel)
    await channel.send(embed=embed)

@client.event
async def on_message_edit(msgb, msga):
	embed = discord.Embed(title=f"{msgb.author.name}",description=f"Edited a message in {msga.channel.mention}", color=color)
	embed.add_field(name="Before", value=msgb.content,inline=False)
	embed.add_field(name="After", value=msga.content,inline=False)
	channel = discord.utils.get(msga.channel.guild.channels, name=loggingchannel)
	await channel.send(embed=embed)

@client.event
async def on_message(message):
	msgc = message.content
	msg = message
	msgcr = msgc.lower().split()
	nono = ("shit", "fuck","bitch","ass","dumbass","faggot", "fucking","tranny","fag","furrfag",'nigga')
	for w in msgcr:
		if w in nono and not msg.author.bot:
			nt = await msg.channel.send("Naughty, naughty")
			dm = await client.get_user(778430856757772318).create_dm()
			await dm.send('{ma} in {guild} was being naughty! They tried to say "{m}" but were stopped.'.format(ma=msg.author,guild=msg.guild,m=msgc))
			asyncio.sleep(1)
			try:
				await msg.delete()
				await asyncio.sleep(2)
				await nt.delete()
			except:
				await asyncio.sleep(2)
				await nt.delete()

			break
	if msgc.lower().startswith("l") and msgc.lower().endswith("l") and "o" in msgc.lower():
		onum = 0
		rnum = 0
		for c in msgc.lower():
			if c == "o":
				onum += 1
			elif c != "o" and c != "l":
				onum = 0
				break
		if onum >= 1:
			try:
				for r in msg.reactions:
					rnum += r.count
			except:
				return
			if not rnum >= 1:
				await msg.add_reaction('😝')
		else:
			return
	if msgc.lower().startswith("l") and msgc.lower().endswith("l") and "e" in msgc.lower():
		enum = 0
		for c in msgc.lower():
			if c == "e":
				enum += 1
			elif c != "e" and c != "l":
				enum = 0
				break
		if enum == 1:
			await msg.add_reaction('😆')
		elif enum == 2:
			await msg.add_reaction('😂')
		elif enum >= 3:
			await msg.add_reaction('🤣')
		else:
			return
	await client.process_commands(message)
