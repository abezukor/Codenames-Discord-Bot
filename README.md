# Discord Codenames Bot
## Whats this?
This is a discord bot that allows users to play the game [Codenames](https://czechgames.com/en/codenames/) over discord with their friends. Before using this bot, it is recommended that you read the [rules](https://czechgames.com/files/rules/codenames-rules-en.pdf). The bot uses a list of english nouns compiled by [Densi Quintans](http://www.desiquintans.com/). [The list can be found here](http://www.desiquintans.com/nounlist).

## How can I use it?
The easiest way to use the Codenames bot is to add it to your discord server with this link:

https://discordapp.com/oauth2/authorize?client_id=553991406415511572&scope=bot&permissions=0

## Bot Commands

*       !startcn [Blue Spymaster] [Red Spymaster] [Other players]
    
    This command will start a Codenames game. The first two mentioned players will be the spymasters while the other players will be automatically divided into the blue and red teams. EX:
        
        !startcn @Player1 @Player2 @Player3 @Player4 @Player5
    
    This will start a game with Player 1 as the blue spymaster, Player 2 as the red spymaster. Players 3, 4, and 5 will be automatically sorted into the red and blue teams.
*       !clue [clue] [number]
    This command allows the spymasters to give clues. EX:
        
        !clue location 5

*       !guess [word]
    This command allows players to make guesses. EX:
        
        !guess local
*       !skip
    This command will skip all remaining guesses on the current teams turn and go to the next turn
*       !end
    This command will immediately end the Codenames game on the current server.

## Self-Hosting the Bot
If you would like to self-host the bot you can.

1. Clone the bot.
2. Get you bot token and put it a text file named token.txt. This file should be in the same folder as the bot. If you dont know how to do that follow [this tutorial.](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
3. Get the required python libraries:
        
        pip3 install discord.py tabulate
4. Run the bot:
        
        python3 CodenamesBot.py
If you would like to change the word list just edit nounlist.txt.