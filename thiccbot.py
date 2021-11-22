#Imports

import discord
import time
import discord.ext
from discord.ext import commands

#Variables

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '.v ', intents=intents, case_insensitive=True)
client.remove_command("help")

#Random Commands

@client.command(name="members")
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

@client.command(name="mail")
async def mail(ctx, person, *message):
	guild = ctx.message.guild
	ms = guild.members
	yes = False
	for m in ms:
		if person == m.name:
			yes = True
			person = m
			break
	if yes:
		channel = await person.create_dm()
		msg = ''
		for part in message:
			msg += part + " "
		await channel.send(msg)
		await ctx.message.channel.send(":white_check_mark: Message Successfully Sent")
		await ctx.message.delete()
	else:
		await ctx.message.channel.send("no")

@client.command(name="poglist")
async def pog(ctx):
	embed = discord.Embed(title="List of Pog Things", description="The list is in increasing order.")
	embed.add_field(name='Number', value='10 - Barbecue Sauce\n9 - Sweet and Sour Sauce\n8 - Buffalo Sauce\n 7 - Chicken Nuggets to put the Sweet and Sour sauce on\n6 - Hooks. The Chicken....I do not fish.\n5 - Ribs to put the Barbecue Sauce on\n4 - Chicken Wings to put the Buffalo Sauce on\n3 - Programming\n2 - Minecraft\n 1 - **You :)**')
	await ctx.message.channel.send(embed=embed)

@client.command(name="inv")
async def invite(ctx):
	invlink = "https://discord.com/oauth2/authorize?client_id=801602344176975914&permissions=8&scope=bot"
	embed = discord.Embed(title="Add Vestal to your server!", description="The bot is in progress.")
	embed.add_field(name="Link", value=invlink, inline=False)
	await ctx.message.channel.send(embed=embed)
	await ctx.message.delete()

@client.command(name="purge")
@commands.has_permissions(administrator=True)
async def purge(ctx, a=None):
	try:
		a = int(a) + 1
	except:
		pass
	if a > 0:
		messages = await ctx.message.channel.history(limit=a).flatten()
		for m in messages:
			await m.delete()
			if len(messages) < 1:
				break
	else:
		m = await ctx.message.channel.send("No")
		await ctx.message.delete()
		time.sleep(5)
		await m.delete()

@client.command(name='help')
async def help(ctx):
	embed=discord.Embed(name="Commands", description='List of commands in Vestal')
	await ctx.message.channel.send(embed=embed)

# @client.command(name='emb')
# async def emb(ctx, *title):
# 	embed = discord.Embed(name=title, description="hi")
# 	await ctx.message.channel.send(embed=embed)

#Events

@client.event
async def on_ready():
	print(f"{client.user.name} is online")
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="your bs"))

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
			time.sleep(1)
			try:
				await msg.delete()
				time.sleep(2)
				await nt.delete()
			except:
				time.sleep(2)
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
