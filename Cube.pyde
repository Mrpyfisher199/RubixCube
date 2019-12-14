#I, Maximilian Latysh, am the creator of this program. 
#Yes, the Russian who lives in Costa Rica, can solve rubiks cubes, and will soon become a unicyclist.
import random

def setup():
    #We define the size and also implement the OpenGl 3d library... I think.
    size(700,700,P3D)
    #Im not even sure if we need the global thing, or if there is a better way, but I don't really care, it's good enough.
    global RUB, stars
    #We make an instance of the Rubix cube.
    RUB = CUBE()
    stars = starField()
    l = createFont("AlegreyaSansSC-Bold",int(width*24/500))
    textFont(l)
    textAlign(CENTER)
    
class CUBE(list):
    def __init__(self):
        self.perspectiveTurn = True
        #These are separate values from the cube itself.
        self.move = True #Determines if we want the cube to turn with the mouse.
        self.cont = 0 #Generally makes the cube turn according to the mouse on the X axis.
        self.cotn = 0 #Generally makes the cube turn according to the mouse on the Y axis.
        #These two are necessary because processing has bad input management.
        self.mouseP = False #Checkpoint for wether or not the mouse has been pressed down.
        self.kEy = False #Checkpoint for wether or not a key has been pressed down.
        #We define the colors.
        self.c = {"W":"ffffff",
                "Y":"ffff00",
                "G":"00ff00",
                "B":"0000ff",
                "R":"ff0000",
                "O":"ffa000"}   
        #We start making the cube.
        #We start with the Y axis.
        for y in range(3):
            #We continue with the X axis.
            for x in range(3):
                #And then finally with the Z axis.
                for z in range(3):
                    #We make a piece.
                    piece = [[x,y,z],["","","","","",""]]
                    #If it's the center piece, we dont add it.
                    if [y,x,z] == [1,1,1]:
                        continue
                    #We check where the piece is located, and we accordingly add the correct color.
                    if y < 1:
                        piece[1][2] = self.c["W"]
                    elif y > 1:
                        piece[1][3] = self.c["Y"]
                    if x < 1:
                        piece[1][4] = self.c["O"]
                    elif x > 1:
                        piece[1][5] = self.c["R"]
                    if z < 1:
                        piece[1][0] = self.c["G"]
                    elif z > 1:
                        piece[1][1] = self.c["B"]
                    self.append(piece)
        #If False, no side will turn, if X then the Right and Left sides.
        #If Y then the Up and Down sides.
        #If Z then the Front and Back sides.
        #If 1 then it turns one way, if -1 then the other way.
        self.turn = [False,0,1]
        self.turnIndexes = []
        self.turnItems = []
        self.angle = -90
    #COMPLETE MESS... I couldn't figure out how to do it automatically, so I had to do it manually.
    #We analize the cubes rotation based on self.cont and self.cotn, and output based on the analisis and input.
    def turnWithOrientation(self,side,prime,activate):
        xy = [0,0]
        sides = ["F","B","U","D","R","L"]
        #We "clean up" the cube's rotations on X and Y.
        if self.cont > PI:
            self.cont %= -PI
        if self.cont < -PI:
            self.cont %= PI
        if self.cotn > PI:
            self.cotn %= -PI
        if self.cotn < -PI:
            self.cotn %= PI
        #We manually assign the side changes based on the rotations.
        if -QUARTER_PI <= self.cont <= QUARTER_PI:
            if -QUARTER_PI <= self.cotn <= QUARTER_PI:
                xy[1] = 0
            elif -3*QUARTER_PI <= self.cotn < -QUARTER_PI:
                xy[1] = 3
            elif QUARTER_PI < self.cotn <= 3*QUARTER_PI:
                xy[1] = 1
            elif 3*QUARTER_PI < self.cotn <= PI or -PI <= self.cotn < -3*QUARTER_PI:
                xy[1] = 2
            sides = self.turnFactor(sides,"X",xy[1])
        elif -3*QUARTER_PI <= self.cont < -QUARTER_PI:
            xy[0] = 3
            if -QUARTER_PI <= self.cotn <= QUARTER_PI:
                sides = self.turnFactor(sides,"Y",xy[0])
            elif -3*QUARTER_PI <= self.cotn < -QUARTER_PI:
                sides = ["R","L","B","F","D","U"]
            elif QUARTER_PI < self.cotn <= 3*QUARTER_PI:
                sides = ["R","L","F","B","U","D"]
            elif 3*QUARTER_PI < self.cotn <= PI or -PI <= self.cotn < -3*QUARTER_PI:
                sides = ["R","L","D","U","F","B"]
        elif 3*QUARTER_PI < self.cont <= PI or -PI <= self.cont < -3*QUARTER_PI:
            xy[0] = 2
            if -QUARTER_PI <= self.cotn <= QUARTER_PI:
                sides = self.turnFactor(sides,"Y",xy[0])
        elif QUARTER_PI < self.cont <= 3*QUARTER_PI:
            xy[0] = 1
            if -QUARTER_PI <= self.cotn <= QUARTER_PI:
                sides = self.turnFactor(sides,"Y",xy[0])
            elif -3*QUARTER_PI <= self.cotn < -QUARTER_PI:
                sides = ["L","R","B","F","U","D"]
            elif QUARTER_PI < self.cotn <= 3*QUARTER_PI:
                sides = ["L","R","F","B","D","U"]
            elif 3*QUARTER_PI < self.cotn <= PI or -PI <= self.cotn < -3*QUARTER_PI:
                sides = ["L","R","D","U","B","F"]
        if activate:
            if side == "U":
                self.activateFunction(sides[2],prime)
            elif side == "D":
                self.activateFunction(sides[3],prime)
            elif side == "F":
                self.activateFunction(sides[0],prime)
            elif side == "B":
                self.activateFunction(sides[1],prime)
            elif side == "R":
                self.activateFunction(sides[4],prime)
            elif side == "L":
                self.activateFunction(sides[5],prime)
        else:
            if side == "U":
                return self.returnColor(sides[2])
            elif side == "D":
                return self.returnColor(sides[3])
            elif side == "F":
                return self.returnColor(sides[0])
            elif side == "B":
                return self.returnColor(sides[1])
            elif side == "R":
                return self.returnColor(sides[4])
            elif side == "L":
                return self.returnColor(sides[5])
        return None
    #We activate the turn of the requested side based on the XY rotation of the cube.
    def activateFunction(self,name,prime):
        if not prime:
            if name == "U":
                self.U()
            if name == "D":
                self.D()
            if name == "F":
                self.F()
            if name == "B":
                self.B()
            if name == "R":
                self.R()
            if name == "L":
                self.L()
        else:
            if name == "U":
                self.Up()
            if name == "D":
                self.Dp()
            if name == "F":
                self.Fp()
            if name == "B":
                self.Bp()
            if name == "R":
                self.Rp()
            if name == "L":
                self.Lp()
    #We give a color depending on the XY rotation of the cube and the given "side".
    def returnColor(self,name):
        if name == "U":
            return self.c["W"]
        if name == "D":
            return self.c["Y"]
        if name == "F":
            return self.c["G"]
        if name == "B":
            return self.c["B"]
        if name == "R":
            return self.c["R"]
        if name == "L":
            return self.c["O"]
    #We initiate the turn animation variables.
    def startTurn(self,indexes,XYZ,d):
        RUB.angle = -90
        self.turn = [True,XYZ,d]
        self.turnItems = [self[i] for i in indexes]
    #We look for the indexes of all the pieces which should be affected by the requesting process.
    #IF the process requests edges, the program looks for pieces with only 2 colored sides
    #Other wise we look for 3 colored sides.                
    def getIds(self,side,EesONo):
        if side == "U":
            #I used VARIABLENAME as the name of the variable because I was so stressed because of the bugs here which ate at my soul and made me so sad I was unable to think.
            VARIABLENAME = []
            for i in range(len(self)):
                if self[i][0][1] == 0:
                    tots = 0
                    for o in self[i][1]:
                        if o!="":
                            tots+=1
                    if EesONo == True and tots==2:
                        VARIABLENAME.append(i)
                    elif EesONo == False and tots==3:
                        VARIABLENAME.append(i)
                    if EesONo == "A":
                        VARIABLENAME.append(i)
            return VARIABLENAME
        if side == "D":
            VARIABLENAME = []
            for i in range(len(self)):
                if self[i][0][1] == 2:
                    tots = 0
                    for o in self[i][1]:
                        if o!="":
                            tots+=1
                    if EesONo == True and tots==2:
                        VARIABLENAME.append(i)
                    elif EesONo == False and tots==3:
                        VARIABLENAME.append(i)
                    if EesONo == "A":
                        VARIABLENAME.append(i)
            return VARIABLENAME
        if side == "F":
            VARIABLENAME = []
            for i in range(len(self)):
                if self[i][0][2] == 0:
                    tots = 0
                    for o in self[i][1]:
                        if o!="":
                            tots+=1
                    if EesONo == True and tots==2:
                        VARIABLENAME.append(i)
                    elif EesONo == False and tots==3:
                        VARIABLENAME.append(i)
                    if EesONo == "A":
                        VARIABLENAME.append(i)
            return VARIABLENAME
        if side == "B":
            VARIABLENAME = []
            for i in range(len(self)):
                if self[i][0][2] == 2:
                    tots = 0
                    for o in self[i][1]:
                        if o!="":
                            tots+=1
                    if EesONo == True and tots==2:
                        VARIABLENAME.append(i)
                    elif EesONo == False and tots==3:
                        VARIABLENAME.append(i)
                    if EesONo == "A":
                        VARIABLENAME.append(i)
            return VARIABLENAME
        if side == "L":
            VARIABLENAME = []
            for i in range(len(self)):
                if self[i][0][0] == 0:
                    tots = 0
                    for o in self[i][1]:
                        if o!="":
                            tots+=1
                    if EesONo == True and tots==2:
                        VARIABLENAME.append(i)
                    elif EesONo == False and tots==3:
                        VARIABLENAME.append(i)
                    if EesONo == "A":
                        VARIABLENAME.append(i)
            return VARIABLENAME
        if side == "R":
            VARIABLENAME = []
            for i in range(len(self)):
                if self[i][0][0] == 2:
                    tots = 0
                    for o in self[i][1]:
                        if o!="":
                            tots+=1
                    if EesONo == True and tots==2:
                        VARIABLENAME.append(i)
                    elif EesONo == False and tots==3:
                        VARIABLENAME.append(i)
                    if EesONo == "A":
                        VARIABLENAME.append(i)
            return VARIABLENAME
    #THE MAGICAL FUNCTION THAT SAVED THIS PROJECT.
    #We basically turn the colors according to how they should be turned.
    def turnFactor(self,colors,mode,times):
        if mode == "X":
            for i in range(times):
                COPY = colors[0]
                colors[0] = colors[3]
                colors[3] = colors[1]
                colors[1] = colors[2]
                colors[2] = COPY 
            return colors
        elif mode == "Y":
            for i in range(times):
                COPY = colors[4]
                colors[4] = colors[0]
                colors[0] = colors[5]
                colors[5] = colors[1]
                colors[1] = COPY
            return colors
        elif mode == "Z":
            for i in range(times):
                COPY = colors[2]
                colors[2] = colors[4]
                colors[4] = colors[3]
                colors[3] = colors[5]
                colors[5] = COPY
            return colors
        return None
    #We turn the White side counter-clockwise.    
    #I messed up this function while copying it so it became the prime of itself, and thus I will document the FRONT function (self.F()).    
    def Up(self):
        for i in self.getIds("U",True):
            POS = self[i][0]
            NEWPOS=[]
            for o in POS:
                NEWPOS.append(o)
            if POS[0] < 1:
                NEWPOS[2]-=1
                NEWPOS[0]+=1
            if POS[0]>1:
                NEWPOS[2]+=1
                NEWPOS[0]-=1
            if POS[0] == 1:
                if POS[2] < 1:
                    NEWPOS[2]+=1
                    NEWPOS[0]+=1
                if POS[2]>1:
                    NEWPOS[2]-=1
                    NEWPOS[0]-=1
            self[i][0] = NEWPOS
            self[i][1] = self.turnFactor(self[i][1],"Y",3)
        for i in self.getIds("U",False):
            POS = self[i][0]
            NEWPOS = []
            for o in POS:
                NEWPOS.append(o)
            if POS[2] < 1 and POS[0] < 1:
                NEWPOS[0] +=2
            elif POS[2] > 1 and POS[0] > 1:
                NEWPOS[0] -=2
            elif POS[2] > 1 and POS[0] < 1:
                NEWPOS[2] -=2
            else:
                NEWPOS[2] +=2
            self[i][0] = NEWPOS
            self[i][1] = self.turnFactor(self[i][1],"Y",3)
        self.startTurn(self.getIds("U","A"),"Y",1)
    #We turn the yellow side clockwise.
    def D(self):
        for i in self.getIds("D",True):
            POS = self[i][0]
            NEWPOS=[]
            for o in POS:
                NEWPOS.append(o)
            if POS[0] < 1:
                NEWPOS[2]-=1
                NEWPOS[0]+=1
            if POS[0]>1:
                NEWPOS[2]+=1
                NEWPOS[0]-=1
            if POS[0] == 1:
                if POS[2] < 1:
                    NEWPOS[2]+=1
                    NEWPOS[0]+=1
                if POS[2]>1:
                    NEWPOS[2]-=1
                    NEWPOS[0]-=1
            self[i][0] = NEWPOS
            self[i][1] = self.turnFactor(self[i][1],"Y",3)
        for i in self.getIds("D",False):
            POS = self[i][0]
            NEWPOS = []
            for o in POS:
                NEWPOS.append(o)
            if POS[2] < 1 and POS[0] < 1:
                NEWPOS[0] +=2
            elif POS[2] > 1 and POS[0] > 1:
                NEWPOS[0] -=2
            elif POS[2] > 1 and POS[0] < 1:
                NEWPOS[2] -=2
            else:
                NEWPOS[2] +=2
            self[i][0] = NEWPOS
            self[i][1] = self.turnFactor(self[i][1],"Y",3)
        self.startTurn(self.getIds("D","A"),"Y",1)
    #We turn the green side clockwise.    
    def F(self):
        #We get the indexes of the to be affected edges.
        for i in self.getIds("F",True):
            #We get the position of the piece and we try to change it with that code.
            POS = self[i][0]
            NEWPOS=[]
            for o in POS:
                NEWPOS.append(o)
            if POS[1] == 0:
                NEWPOS[0]+=1
                NEWPOS[1]+=1
            elif POS[1] == 2:
                NEWPOS[0]-=1
                NEWPOS[1]-=1
            elif POS[1] == 1:
                if POS[0] == 0:
                    NEWPOS[0]+=1
                    NEWPOS[1]-=1
                elif POS[0] == 2:
                    NEWPOS[0]-=1
                    NEWPOS[1]+=1
            #We change the position.
            self[i][0] = NEWPOS
            #We "rotate" the colors accordingly
            self[i][1] = self.turnFactor(self[i][1],"Z",1)
        #We get the indexes of the to be affected corners.
        #Essentially, we do the same thing.
        for i in self.getIds("F",False):
            POS = self[i][0]
            NEWPOS = []
            for o in POS:
                NEWPOS.append(o)
            if POS[0] < 1 and POS[1] < 1:
                NEWPOS[0] +=2
            elif POS[0] > 1 and POS[1] > 1:
                NEWPOS[0] -=2
            elif POS[0] > 1 and POS[1] < 1:
                NEWPOS[1] +=2
            else:
                NEWPOS[1] -=2
            self[i][0] = NEWPOS
            self[i][1] = self.turnFactor(self[i][1],"Z",1)
        self.startTurn(self.getIds("F","A"),"Z",1)
    #We turn the Blue side clockwise.
    def B(self):
        self.startTurn(self.getIds("B","A"),"Z",-1)
        for i in self.getIds("B",True):
            POS = self[i][0]
            NEWPOS=[]
            for o in POS:
                NEWPOS.append(o)
            if POS[1] < 1:
                NEWPOS[0]-=1
                NEWPOS[1]+=1
            if POS[1]>1:
                NEWPOS[0]+=1
                NEWPOS[1]-=1
            if POS[1] == 1:
                if POS[0] < 1:
                    NEWPOS[0]+=1
                    NEWPOS[1]+=1
                if POS[0]>1:
                    NEWPOS[0]-=1
                    NEWPOS[1]-=1
            self[i][0] = NEWPOS
            self[i][1] = self.turnFactor(self[i][1],"Z",3)
        for i in self.getIds("B",False):
            POS = self[i][0]
            NEWPOS = []
            for o in POS:
                NEWPOS.append(o)
            if POS[0] < 1 and POS[1] < 1:
                NEWPOS[1] +=2
            elif POS[0] > 1 and POS[1] > 1:
                NEWPOS[1] -=2
            elif POS[0] > 1 and POS[1] < 1:
                NEWPOS[0] -=2
            else:
                NEWPOS[0] +=2
            self[i][0] = NEWPOS
            self[i][1] = self.turnFactor(self[i][1],"Z",3)
    #We turn the red side clockwise.            
    def R(self):
        self.startTurn(self.getIds("R","A"),"X",1)
        for i in self.getIds("R",True):
            POS = self[i][0]
            NEWPOS=[]
            for o in POS:
                NEWPOS.append(o)
            if POS[1] < 1:
                NEWPOS[2]+=1
                NEWPOS[1]+=1
            if POS[1]>1:
                NEWPOS[2]-=1
                NEWPOS[1]-=1
            if POS[1] == 1:
                if POS[2] < 1:
                    NEWPOS[2]+=1
                    NEWPOS[1]-=1
                if POS[2]>1:
                    NEWPOS[2]-=1
                    NEWPOS[1]+=1
            self[i][0] = NEWPOS
            self[i][1] = self.turnFactor(self[i][1],"X",1)
        for i in self.getIds("R",False):
            POS = self[i][0]
            NEWPOS = []
            for o in POS:
                NEWPOS.append(o)
            if POS[2] < 1 and POS[1] < 1:
                NEWPOS[2] +=2
            elif POS[2] > 1 and POS[1] > 1:
                NEWPOS[2] -=2
            elif POS[2] > 1 and POS[1] < 1:
                NEWPOS[1] +=2
            else:
                NEWPOS[1] -=2
            self[i][0] = NEWPOS
            self[i][1] = self.turnFactor(self[i][1],"X",1)
    #We turn the Orange side clockwise.
    def L(self):
        self.startTurn(self.getIds("L","A"),"X",-1)
        for i in self.getIds("L",True):
            POS = self[i][0]
            NEWPOS=[]
            for o in POS:
                NEWPOS.append(o)
            if POS[1] < 1:
                NEWPOS[2]-=1
                NEWPOS[1]+=1
            if POS[1]>1:
                NEWPOS[2]+=1
                NEWPOS[1]-=1
            if POS[1] == 1:
                if POS[2] < 1:
                    NEWPOS[2]+=1
                    NEWPOS[1]+=1
                if POS[2]>1:
                    NEWPOS[2]-=1
                    NEWPOS[1]-=1
            self[i][0] = NEWPOS
            self[i][1] = self.turnFactor(self[i][1],"X",3)
        for i in self.getIds("L",False):
            POS = self[i][0]
            NEWPOS = []
            for o in POS:
                NEWPOS.append(o)
            if POS[2] < 1 and POS[1] < 1:
                NEWPOS[1] +=2
            elif POS[2] > 1 and POS[1] > 1:
                NEWPOS[1] -=2
            elif POS[2] > 1 and POS[1] < 1:
                NEWPOS[2] -=2
            else:
                NEWPOS[2] +=2
            self[i][0] = NEWPOS
            self[i][1] = self.turnFactor(self[i][1],"X",3)
    
    #These are the "primes" of the turns.
    #The reason why U is calling Up() 3 times is because I messed up and made the inverse of U().
    def U(self):
        for i in range(3):self.Up()
        self.startTurn(self.getIds("U","A"),"Y",-1)
    def Dp(self):
        for i in range(3):self.D()
        self.startTurn(self.getIds("D","A"),"Y",-1)
    def Fp(self):
        for i in range(3):self.F()
        self.startTurn(self.getIds("F","A"),"Z",-1)
    def Bp(self):
        for i in range(3):self.B()
        self.startTurn(self.getIds("B","A"),"Z",1)
    def Rp(self):
        for i in range(3):self.R()
        self.startTurn(self.getIds("R","A"),"X",-1)
    def Lp(self):
        for i in range(3):self.L()
        self.startTurn(self.getIds("L","A"),"X",1)

class starField(list):
    def __init__(self):
        for i in range(100):
            star = [[random.randint(0,width),random.randint(0,height)],random.randint(2,5),
                    random.choice([[150,0,150],[200,200,200]])]
            self.append(star)
    def render(self):
        translate(0,0,-50)
        for i in self:
            stroke(i[2][0],i[2][1],i[2][2])
            strokeWeight(i[1])
            point(i[0][0],i[0][1])
            

#Here we make the separate planes of the box.
def make(END,OTHER,MODE):
    if not MODE:
        beginShape();
        vertex(0, 0, -OTHER);
        vertex(END, 0, -OTHER);
        vertex(END, END, -OTHER);
        vertex(0, END, -OTHER);
        endShape();
    elif MODE < 2:
        beginShape();
        vertex(0, OTHER, 0);
        vertex(END, OTHER, 0);
        vertex(END, OTHER, -END);
        vertex(0, OTHER, -END);
        endShape();
    else:
        beginShape();
        vertex(OTHER, 0, 0);
        vertex(OTHER, END, 0);
        vertex(OTHER, END, -END);
        vertex(OTHER, 0, -END);
        endShape(); 

#Had to make my own BOX function because I couldn't figure out how to color each side separately.        
def makeBox(colors):
    #0,1 Front,Back; 2,3 topBottom; 4,5 Right,Left
    stroke(0)
    strokeWeight(2)
    fill(unhex("FF"+colors[0]))
    make(50,0,0)
    fill(unhex("FF"+colors[2]))
    make(50,0,1)
    fill(unhex("FF"+colors[4]))
    make(50,0,2)
    fill(unhex("FF"+colors[1]))
    make(50,50,0)
    fill(unhex("FF"+colors[3]))
    make(50,50,1)
    fill(unhex("FF"+colors[5]))
    make(50,50,2)
   
#Funcition to check if the mouse is inside a cube.
#Where a is the starting X position and c is how wide the button is,
#and where b is the starting Y position and d is how high the button is.
def isInside(a,b,c,d):
    if a<=mouseX<=c+a and b<=mouseY<=d+b:
        return True
    else:
        return False
#A small function to help us make a textBoxie.
def textBox(posX,posY,T):
    fill(0)
    text(T,posX+(width*1.0/24),posY+10+(height*1.0/24))

def draw():
    #We change the alpha if the mouse is hovering over the button.
    tone = [0,0,0,0,0,0,0,0,0,0,0,0]
    if isInside(10,10,width/12,height/12):
        tone[0] = 220
    elif isInside(width/2-width/12,10,width/12,height/12):
        tone[1] = 220
    elif isInside(width-10-width/6,10,width/12,height/12):
        tone[2] = 220
    elif isInside(10,height-10-height/12,width/12,height/12):
        tone[3] = 220
    elif isInside(width/2-width/12,height-10-height/12,width/12,height/12):
        tone[4] = 220
    elif isInside(width-10-width/6,height-10-height/12,width/12,height/12):
        tone[5] = 220
    elif isInside(10+width/12,10,width/12,height/12):
        tone[6] = 220
    elif isInside(width/2,10,width/12,height/12):
        tone[7] = 220
    elif isInside(width-10-width/6+width/12,10,width/12,height/12):
        tone[8] = 220
    elif isInside(width/12+10,height-10-height/12,width/12,height/12):
        tone[9] = 220
    elif isInside(width/2,height-10-height/12,width/12,height/12):
        tone[10] = 220
    elif isInside(width-10-width/6+width/12,height-10-height/12,width/12,height/12):
        tone[11] = 220
    if keyPressed:
        if not RUB.kEy:
            RUB.kEy = True
            #We check for the inputs U, D, F, G, R, and L, which correspond to the sides we want to turn.
            if key == "u":
                RUB.U()
            if key == "d":
                RUB.D()
            if key == "f":
                RUB.F()
            if key == "b":
                RUB.B()
            if key == "r":
                RUB.R()
            if key == "l":
                RUB.L()
            #If the key is the spacebar the pause or unpause the movement of the cube following the mouse
            if key == " ":
                RUB.move = not RUB.move
    else:
        RUB.kEy = False
    if mousePressed:
        #We just check wether or not once the mouse is pressed if it is inside one of the buttons
        if not RUB.mouseP:
            RUB.mouseP = True
            if isInside(10,10,width/6,height/12):
                if mouseX <= width/12+10:
                    #Then we check if the perspective mode is on.
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("U",False,True)
                    else:
                        RUB.U()
                else:
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("U",True,True)
                    else:
                        RUB.Up()
            elif isInside(width/2-width/12,10,width/6,height/12):
                if mouseX <= width/2:
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("D",False,True)
                    else:
                        RUB.D()
                else:
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("D",True,True)
                    else:
                        RUB.Dp()
            elif isInside(width-10-width/6,10,width/6,height/12):
                if mouseX <= width-10-width/6+width/12:
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("F",False,True)
                    else:
                        RUB.F()
                else:
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("F",True,True)
                    else:
                        RUB.Fp()
            elif isInside(10,height-10-height/12,width/6,height/12):
                if mouseX <= width/12+10:
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("B",False,True)
                    else:
                        RUB.B()
                else:
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("B",True,True)
                    else:
                        RUB.Bp()
            elif isInside(width/2-width/12,height-10-height/12,width/6,height/12):
                if mouseX <= width/2:
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("R",False,True)
                    else:
                        RUB.R()
                else:
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("R",True,True)
                    else:
                        RUB.Rp()
            elif isInside(width-10-width/6,height-height/12-10,width/6,height/12):
                if mouseX <= width-10-width/6+width/12:
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("L",False,True)
                    else:
                        RUB.L()
                else:
                    if RUB.perspectiveTurn:
                        RUB.turnWithOrientation("L",True,True)
                    else:
                        RUB.Lp()
            #We change the perspective mode.
            elif isInside(10,40+height/12,width/6-20,height-(40+height/12)*2):
                RUB.perspectiveTurn = not RUB.perspectiveTurn
    else:
        RUB.mouseP = False
    #We render the buttons...
    #They would have been placed inside a fucntion but it didn't work so I gave up...
    translate(-width/2,-height/2)
    background(0)
    #The stars... just to make the background look nicer.
    stars.render()
    translate(0,0,50)
    fill(50)
    #We make the button for changing the perspective.
    if isInside(10,40+height/12,width/6-20,height-(40+height/12)*2):
        fill(100)
    stroke(200)
    strokeWeight(5)
    rect(10,40+height/12,width/6-20,height-(40+height/12)*2)
    fill(250)
    rect(width-width/6-10,40+height/12,width/6,height-(40+height/12)*2)
    fill(0)
    textSize(int(width*12/500))
    #We add the clarifying text field.
    text("Welcome!\n\nMake the cube turn by moving the mouse. Press the spacebar to pause cube movement.\n\nThe left button changes the perspective mode. The other buttons turn the cube's sides.",width-10-width/6,60+height/12,width/6,height-(40+height/12)*2)
    stroke(0)
    textSize(int(width*24/500))
    strokeWeight(4)
    if RUB.perspectiveTurn:
        fill(unhex("FF"+RUB.turnWithOrientation("U",False,False)))
    else:
        fill(unhex("FF"+RUB.c["W"]))
    rect(10,10,width/6,height/12)
    fill(200,tone[0])
    rect(10,10,width/12,height/12)
    fill(200,tone[6])
    rect(width/12+10,10,width/12,height/12)
    line(width/12+10,10,width/12+10,height/12+10)
    if RUB.perspectiveTurn:
        textBox(width/12+10,10,"Up")
        textBox(10,10,"U")
        fill(unhex("FF"+RUB.turnWithOrientation("D",False,False)))
    else:
        textBox(width/12+10,10,"W")
        textBox(10,10,"W")
        fill(unhex("FF"+RUB.c["Y"]))
    rect(width/2-width/12,10,width/6,height/12)
    fill(200,tone[1])
    rect(width/2-width/12,10,width/12,height/12)
    fill(200,tone[7])
    rect(width/2,10,width/12,height/12)
    line(width/2,10,width/2,height/12+10)
    if RUB.perspectiveTurn:
        textBox(width/2,10,"Dp")
        textBox(width/2-width/12,10,"D")
        fill(unhex("FF"+RUB.turnWithOrientation("F",False,False)))
    else:
        textBox(width/2,10,"Y")
        textBox(width/2-width/12,10,"Y")
        fill(unhex("FF"+RUB.c["G"]))
    rect(width-10-width/6,10,width/6,height/12)
    fill(200,tone[2])
    rect(width-10-width/6,10,width/12,height/12)
    fill(200,tone[8])
    rect(width-10-width/6+width/12,10,width/12,height/12)
    line(width-10-width/6+width/12,10,width-10-width/6+width/12,height/12+10)
    if RUB.perspectiveTurn:
        textBox(width-10-width/6+width/12,10,"Fp")
        textBox(width-10-width/6,10,"F")
        fill(unhex("FF"+RUB.turnWithOrientation("B",False,False)))
    else:
        textBox(width-10-width/6+width/12,10,"G")
        textBox(width-10-width/6,10,"G")
        fill(unhex("FF"+RUB.c["B"]))
    rect(10,height-10-height/12,width/6,height/12)
    fill(200,tone[3])
    rect(10,height-10-height/12,width/12,height/12)
    fill(200,tone[9])
    rect(width/12+10,height-10-height/12,width/12,height/12)
    line(width/12+10,height-10-height/12,width/12+10,height-10)
    if RUB.perspectiveTurn:
        textBox(width/12+10,height-10-height/12,"Bp")
        textBox(10,height-10-height/12,"B")
        fill(unhex("FF"+RUB.turnWithOrientation("R",False,False)))
    else:
        textBox(width/12+10,height-10-height/12,"B")
        textBox(10,height-10-height/12,"B")
        fill(unhex("FF"+RUB.c["R"]))
    rect(width/2-width/12,height-10-height/12,width/6,height/12)
    fill(200,tone[4])
    rect(width/2-width/12,height-10-height/12,width/12,height/12)
    fill(200,tone[10])
    rect(width/2,height-10-height/12,width/12,height/12)
    line(width/2,height-10-height/12,width/2,height-10)
    if RUB.perspectiveTurn:
        textBox(width/2,height-10-height/12,"Rp")
        textBox(width/2-width/12,height-10-height/12,"R")
        fill(unhex("FF"+RUB.turnWithOrientation("L",False,False)))
    else:
        textBox(width/2,height-10-height/12,"R")
        textBox(width/2-width/12,height-10-height/12,"R")
        fill(unhex("FF"+RUB.c["O"]))
    rect(width-10-width/6,height-height/12-10,width/6,height/12)
    fill(200,tone[5])
    rect(width-10-width/6,height-height/12-10,width/12,height/12)
    fill(200,tone[11])
    rect(width-10-width/6+width/12,height-height/12-10,width/12,height/12)
    line(width-10-width/6+width/12,height-10-height/12,width-10-width/6+width/12,height-10)
    if RUB.perspectiveTurn:
        textBox(width-10-width/6+width/12,height-10-height/12,"Lp")
        textBox(width-10-width/6,height-10-height/12,"L")
    else:
        textBox(width-10-width/6+width/12,height-10-height/12,"O")
        textBox(width-10-width/6,height-10-height/12,"O")
    #We make sure we actually want to move the cube around with the mouse.
    if RUB.move:
        RUB.cont = map(mouseX,width/8,width-width/8,-PI,PI)
        RUB.cotn = map(mouseY,height/8,height-height/8,PI,-PI)
    #We always keep the camera in the center, so WE don't move but the cube does.
    camera(0,0, (height/2) / tan(PI/6), 0,0, 0, 0, 1, 0) 
    rotateY(RUB.cont)
    rotateX(RUB.cotn)
    #We render the whole Rubix cube.
    for i in RUB:
        if i in RUB.turnItems:
            continue
        pushMatrix()
        #We render each "box" in the cube separetely, EXCEPT for the one in the center.
        translate(i[0][0]*50-75,i[0][1]*50-75,i[0][2]*-50+75)
        makeBox(i[1])
        #I don't know why, but for some reason a black line isn't rendered which annoyed me so I added this.
        if i[0][0]==0 and i[0][1] == 0:
            line(0,0,-50,0,0,0)
        popMatrix()
    #We play the turn "animation" for once a side is turned.
    if RUB.turn[0]:
        #We rotate the matrices accordingly.
        if RUB.turn[1] == "X":
            rotateX(radians(RUB.angle)*RUB.turn[2])
        elif RUB.turn[1] == "Y":
            rotateY(radians(RUB.angle)*RUB.turn[2])
        elif RUB.turn[1] == "Z":
            rotateZ(radians(RUB.angle)*RUB.turn[2])
        for i in RUB.turnItems:
            #We render the pieces
            pushMatrix()
            translate(i[0][0]*50-75,i[0][1]*50-75,i[0][2]*-50+75)
            makeBox(i[1])
            if i[0][0]==0 and i[0][1] == 0:
                line(0,0,-50,0,0,0)
            popMatrix()
        #We increment the angle
        RUB.angle+=3
        if RUB.angle > 0:
            #Then we reset everything
            RUB.angle = -90
            RUB.turn = [False,0,1]
            RUB.turnIndexes = []
            RUB.turnItems = []
