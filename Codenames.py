import random
from discord import User
from tabulate import tabulate
import math

class Game:
    currentTurn = None
    turnChange = {
            "blue": "red",
            "red": "blue"
    }
    guesses = 0

    def __init__(self, cm1: User, cm2: User, otherUsers):
        self.players = [cm1, cm2] + otherUsers

        self.cm = {
            "blue": cm1,
            "red": cm2
        }

        random.shuffle(otherUsers)
        print(otherUsers)

        self.teams = {
            "red": otherUsers[:len(otherUsers)//2],
            "blue": otherUsers[len(otherUsers)//2:]
        }

        self.inputWords= random.sample(open("nounlist.txt").readlines(),25)
        self.inputWords = [word.rstrip("\n") for word in self.inputWords]
        notBystanders = random.sample(self.inputWords,18)

        firstTeam = [lambda notBystanders: notBystanders[1:10], lambda notBystanders: notBystanders[10:]]
        random.shuffle(firstTeam)

        self.words = {
            "assassin": notBystanders[0],
            "red": firstTeam[0](notBystanders),
            "blue": firstTeam[1](notBystanders)
        }
        self.words["bystander"] = [word for word in self.inputWords if word not in self.words["red"] and word not in self.words["blue"] and word !=self.words["assassin"]]

        if(len(self.words["red"])>len(self.words["blue"])):
            self.currentTurn = "red"
        else:
            self.currentTurn = "blue"


    def getBlueTeam(self):
        return self.teams["blue"]
    
    def getBlueCM(self):
        return self.cm["blue"]
    
    def getRedTeam(self):
        return self.teams["red"]

    def getRedCM(self):
        return self.cm["red"]
    
    def getCurrentTurn(self):
        return self.currentTurn
    
    def printableBoard(self):
        twoDBoard = [self.inputWords[5*n:5*n+5] for n in range(len(self.inputWords)//5)]

        table = "```" + tabulate(twoDBoard, tablefmt="grid") + "```"
        #print(table)
        return table
    
    def getGameState(self):
        return("Blue words remaining: {} \n Red words remaining: {} \n Assassin: {} \n Bystanders remaining: {}"
            .format(", ".join(self.words["blue"]), ", ".join(self.words["red"]), self.words["assassin"], ", ".join(self.words["bystander"])))

    def nextTurn(self):
        self.currentTurn = self.turnChange[self.currentTurn]

        return self.currentTurn
    
    def clue(self, user, clue, num):

        if(user!=self.cm[self.currentTurn]):
            return("You cannot give a clue. {} has to give the clue now.".format(self.cm[self.currentTurn]))
        
        if(num):
            self.guesses = num + 1
        else:
            self.guesses = math.inf
        return("You have {} guesses.".format(self.guesses))

    def skip(self,user):
        if user not in self.teams[self.currentTurn]:
            return("You cant skip.")
        self.nextTurn()
        return("The {} team skips. It is now the {} teams turn.".format(self.turnChange[self.currentTurn],self.currentTurn))

    def guess(self, user, guess):

        if user not in self.teams[self.currentTurn]:
            return("Invalid player. Guess Again.")
        
        if(self.guesses == 0):
            return("Invalid Guess. You need a clue first.")
        
        returnText = ""
        if guess == self.words["assassin"]:
            return("You guessed the assassin. {} team wins.".format(self.turnChange[self.currentTurn]))

        elif(guess in self.words[self.currentTurn]):
            self.words[self.currentTurn].remove(guess)
            self.inputWords = [self.currentTurn.upper() if guess == word else word for word in self.inputWords]

            if(len(self.words[self.currentTurn])==0):
                return("Congratulations, you guessed the last {} word. The {} team wins".format(self.currentTurn, self.currentTurn))
            
            self.guesses -= 1

            returnText = "You guessed correctly. You have {} guesses remaining".format(str(self.guesses))

        elif(guess in self.words[self.turnChange[self.currentTurn]]):
            otherTeam = self.turnChange[self.currentTurn]
            self.words[otherTeam].remove(guess)
            self.inputWords = [otherTeam.upper() if guess == word else word for word in self.inputWords]

            if(len(self.words[self.currentTurn])==0):
                return("Unfortunately, you guessed the last {} word. The {} team wins".format(otherTeam, otherTeam))
            
            returnText = "You guessed one of your opponents words."
            
            self.guesses = 0

        elif(guess in self.words["bystander"]):
            self.words["bystander"].remove(guess)
            self.inputWords = ["BYSTANDER" if guess == word else word for word in self.inputWords]
            
            returnText = "You guessed a bystander"

            self.guesses = 0
        else:
            return("Invalid Guess. Guess Again.")

        if(self.guesses==0):
            self.nextTurn()
            returnText += "\n You are out of guesses. It is now the {} teams turn.".format(self.currentTurn)

        return(returnText)
