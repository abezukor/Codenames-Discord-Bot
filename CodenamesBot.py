from discord.ext.commands import Bot
from discord import User
import discord
import asyncio
from Codenames import Game
from ImageGenerator import BoardGenerator

prefix = "!"
bot = Bot(command_prefix=prefix)

boardgen = BoardGenerator()
cngames = {}

@bot.event
async def on_ready():
    print("Everything's all ready to go~")

#
#@bot.event
#async def on_message(message):
#    print("The message's content was", message.content)
async def saystatus(ctx,game,dm=True):
	#boardgen.makeBoard(game.getBoardArray())
	#await bot.send_file(ctx.message.channel,"Resources/board.jpg")
	await bot.send_file(ctx.message.channel,boardgen.makeBoard(game.getBoardArray()))

	if(dm):
		await bot.send_message(game.getBlueCM(), game.getGameState())
		await bot.send_message(game.getRedCM(), game.getGameState())

@bot.command(pass_context=True)
async def startcn(ctx, *users: discord.User):
	id = ctx.message.server.id

	if(id in cngames):
		await bot.say("A Game is already running on this server. Please end that game with {}end to start a new game.".format(prefix))
		return

	cngames[id] = Game(users[0], users[1], list(users[2:]))
	game = cngames[id]

	await bot.say("The blue team codemaster is " + game.getBlueCM().mention)
	await bot.say("The blue team is {}.".format(", ".join([member.mention for member in game.getBlueTeam()])))

	await bot.say("The red team codemaster is " + game.getRedCM().mention)
	await bot.say("The red team is {}.".format(", ".join([member.mention for member in game.getRedTeam()])))
	
	
	await bot.send_message(game.getBlueCM(), "You are the blue codemaster.")
	await bot.send_message(game.getRedCM(), "You are the red codemaster.")

	await saystatus(ctx,game)

	await bot.say("It is {} team's turn to give a clue.".format(game.currentTurn))

@bot.command(pass_context=True)
async def end(ctx):
	try:
		del cngames[ctx.message.server.id]
		await bot.say("Game ended.")
	except KeyError:
		await bot.say("No game to end.")

@bot.command(pass_context=True)
async def pastclues(ctx):
	try:
		game = cngames[ctx.message.server.id]
	except KeyError:
		await bot.say("You need to start a game first.")
		return
	
	await bot.say(game.getPastClues(ctx.message.author))

@bot.command(pass_context=True)
async def guess(ctx, *, content:str):
	try:
		game = cngames[ctx.message.server.id]
	except KeyError:
		await bot.say("You need to start a game first.")
		return
	
	cturn=game.getCurrentTurn()

	guess = game.guess(ctx.message.author, content)

	if "wins" in guess:
		del cngames[ctx.message.server.id]
		await bot.say(guess)
		await bot.send_file(ctx.message.channel,boardgen.makeBoard(game.getBoardArray()))
		return
	await bot.say(guess)

	if("Invalid" not in guess):
		await saystatus(ctx,game,dm=(cturn!=game.getCurrentTurn()))
	
@bot.command(pass_context=True)
async def clue(ctx, *, clue):
	try:
		game = cngames[ctx.message.server.id]
	except KeyError:
		await bot.say("You need to start a game first.")
		return
	
	print(clue.split())
	clue = game.clue(ctx.message.author, clue.split()[0], int(clue.split()[1]))
	
	await bot.say(clue)

@bot.command(pass_context=True)
async def skip(ctx):
	try:
		game = cngames[ctx.message.server.id]
	except KeyError:
		await bot.say("You need to start a game first.")
		return
	bot.say(game.skip(ctx.message.author))


bot.run(open("token.txt","r").read().rstrip('\n'))
