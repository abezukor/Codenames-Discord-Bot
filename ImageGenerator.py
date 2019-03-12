from PIL import Image, ImageDraw, ImageFont
import copy

class BoardGenerator:
    def __init__(self):
        self.blankcard = Image.open("Resources/template.jpg")
        self.font = ImageFont.truetype("Resources/OpenSans-Light.ttf", 15)
        self.redagent = Image.open("Resources/redagent.jpeg")
        self.blueagent = Image.open("Resources/blueagent.jpeg")
        self.bystander = Image.open("Resources/bystander.png")
        self.assassin = Image.open("Resources/assassin.jpeg")

    def makeCard(self,msg):
        blankcard = copy.deepcopy(self.blankcard)

        draw = ImageDraw.Draw(blankcard)

        w, h = draw.textsize(msg,self.font)
        W, H = 100, 22
        draw.text(((W-w)/2+12,(H-h)/2+44), msg, fill="black", font=self.font)

        return blankcard
    
    def makeBoard(self,board):
        finalboard = Image.new('RGB', (620,395))

        for i in range(0,5):
            for j in range(0,5):
                entry = board[i][j]
                if entry=="RED": finalboard.paste(self.redagent,(j*124,i*79))
                elif entry=="BLUE": finalboard.paste(self.blueagent,(j*124,i*79))
                elif entry=="BYSTANDER": finalboard.paste(self.bystander,(j*124,i*79))
                elif entry=="ASSASSIN": finalboard.paste(self.assassin,(j*124,i*79))
                else: finalboard.paste(self.makeCard(entry),(j*124,i*79))
        
        finalboard.save("Resources/board.jpg")
        return open("Resources/board.jpg","rb")
