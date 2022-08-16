#this is a new way of looking at things! each element is going to be an object itself.

#TODO impliment gravity on cells 
#todo Make more elements
#todo impliment generations to avoid double movement
 
import copy
import random

class element():
    board = None
    elementNames = ["empty", "sand","stone","water","salt","lava"]
    boardGeneration = 0
    
    @staticmethod
    def elementIDToColor(elementID):
        
        if elementID == 0:
            #empty
            return "white"
        
        elif elementID == 1:
            #sand
            return "yellow"
        
        elif elementID == 2:
            #stone
            return "grey"
        
        elif elementID == 3:
            #water
            return "blue" 
        
        elif elementID == 4:
            return "pink"
        
        elif elementID == 5:
            return "brown"
        
        elif elementID == 6:
            return "red"
    
    @staticmethod
    def getElementAtCell(row,col):
        #returns object element from row,col in board.
        #if out of range, return -1
        
        if element.inBounds(row, col):
            return element.board[row][col]
        else:
            #out of bounds
            return None    
    
    @staticmethod
    def inBounds(row,col):
        #? returns true if element in row
        
        bRows = len(element.board)
        bCols = len(element.board[0])
        
        if ((row >= bRows or row < 0) 
            or (col >= bCols or col < 0)):
            #out of bounds
            return False
        else:
            return True
    
    @staticmethod
    def initBoard(outsideBoard):
        #initializes specically made board 
        element.board = copy.deepcopy(outsideBoard)
        for row in range(len(element.board)):
            for col in range(len(element.board[0])):
                
                elementID = element.board[row][col]
                elementName = element.elementNames[elementID]
                element.addElementID(elementID, row, col) 
    
       
    @staticmethod
    def initEmptyBoard(rows,cols):
        #takes an outside board and initializes it as all empty. 
        element.board = [ ([0] * cols) for row in range(rows) ]
        generation = 0
        for row in range(len(element.board)):
            for col in range(len(element.board[0])):
                element.board[row][col] = empty(row, col, generation)
    
    @staticmethod
    def updateBoard():
        #! super important! Goes through all element objects in board and updates them. Only update once per generation!
        
        for iteration in range(len(element.board)):
            row = len(element.board) - iteration - 1
            for col in range(len(element.board[0])):
                
                element.board[row][col].update(element.boardGeneration)
        
        element.boardGeneration += 1 
        
    
    @staticmethod
    def returnNumberBoard():
        #returns board as a panel of numbers representing element IDs
        numberBoard = copy.deepcopy(element.board)
        
        for row in range(len(numberBoard)):
            for col in range(len(numberBoard[0])):
                
                elementObject = element.board[row][col]
                numberBoard[row][col] = elementObject.getID()
                
        return numberBoard

    @staticmethod
    def addElementID(elementID,row,col):
        
        if elementID == 0:
            element.board[row][col] = empty(row, col, element.boardGeneration + 1)
            
        elif elementID == 1:
            element.board[row][col] = sand(row, col, element.boardGeneration + 1)
            
        elif elementID == 2:
            element.board[row][col] = stone(row, col, element.boardGeneration + 1)
            
        elif elementID == 3:
            #make sure to use boardGeneration + 1 to avoid being skipped
            element.board[row][col] = water(row, col, element.boardGeneration + 1)     
        elif elementID == 4:
            element.board[row][col] = salt(row, col, element.boardGeneration + 1)
        elif elementID == 5:
            element.board[row][col] = dirt(row, col, element.boardGeneration + 1)

        elif elementID == 6:
            element.board[row][col] = lava(row, col, element.boardGeneration + 1 )

   
    
    def __init__(self,row,col, generation):  
        
        #covers self.row, self.col and baord[row][col]
        
        self.setPosition(row,col)
        self.updates = generation #make sure updates == generation of board as not to double update 
        #put self object into board 2D list        
        
        
        self.Empty = False
        self.Solid = False
        self.Liquid = False
        self.ID = 0
        
        #how many blocks element has been consecutively falling down 
        self.fallMultiplier = 0
        
        
    def isEmpty(self):
        return self.Empty
    
    def isSolid(self):
        return self.Solid
    
    def isLiquid(self):
        return self.Liquid
    
    def getID(self):
        return self.ID
    
    def setPosition(self,row,col):
        #changes element position in board
        
        self.row = row
        self.col = col
        
        #changes board object to have self on it
        element.board[row][col] = self
        
    def swap(self,bRow,bCol):
        #? using your own row,col and other row,col, swaps position
        
        #other is other cell object
        aCol = self.col
        aRow = self.row
        if element.inBounds(bRow, bCol) and element.inBounds(aRow, bCol):
            
            
            other = element.board[bRow][bCol]
            
            other.setPosition(aRow,aCol)
            self.setPosition(bRow,bCol)
    
    def cellEmpty(self,row,col):
        return element.board[row][col].isEmpty()
    
    def destroyElement(self,row,col):
        #turns element into empty element...
        
        element.board[row][col] = empty(row, col, element.boardGeneration)
        
    def getSurroundingElements(self):
        #returns a 8 long string of elementIDs of surrounding objects
        
        row = self.row
        col = self.col
 
        directions = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        elements = []
        for direction in directions:
            drow,dcol = direction
            
            element = self.getElementAtCell(row+drow, col+dcol)
            
            
            
            elements.append(element)     
            
        return elements
        
    
class empty(element):
    
    def __init__(self,row,col, generation):
        super().__init__(row, col,generation)
        self.ID = 0
        self.Empty = True
        self.color = "white"
        
    def update(self,generation):
        #takes 2D list of objects and position, and updates accordingly
        pass
        
class sand(element):
    
    def __init__(self,row,col,generation):
        super().__init__(row, col,generation)
        self.ID = 1
        self.solid = True
        self.color = random.choice(["khaki","pale goldenrod","dark khaki"])
        
        
    def update(self, generation):
        # if self.updates != generation:
        #     #make sure not to double update solid
        #     return 
        #todo randomize BR/BL movement 
        #if gen = updates, update board as not to double count 
        
        row = self.row
        col = self.col
        
        #looks at below, bottomleft, bottom right elements, and swaps if empty
        lower = element.getElementAtCell(row+1, col)
        lowerLeft = element.getElementAtCell(row+1, col-1)
        lowerRight = element.getElementAtCell(row+1, col+1)
        
        
        # != None makes sure getElementAtCell returns an object and isnt out of bounds
        if lower != None and (lower.isEmpty()):
            #swap with lower cell if liquid or empty.
            fallRow = row+1
            self.swap(fallRow,col)
            
            
            targetRow = self.fallMultiplier + row
            
            targetElement = element.getElementAtCell(targetRow, col)
            
            while targetElement != None and not targetElement.isEmpty():
                targetRow -= 1 
                
                targetElement = element.getElementAtCell(targetRow, col)
                
            self.swap(targetRow, col)
            
            self.fallMultiplier += 1 
            
            return
        #on the ground, reset multiplier to zero
        self.fallMultiplier = 0 
        
        if lower != None and lower.isLiquid():
            #if lower element is liquid, swap 
            
            self.swap(row+1,col)
        
        elif lowerLeft != None and (lowerLeft.isEmpty() or lower.isLiquid()):    
            self.swap(row+1, col-1)
            
        elif lowerRight != None and (lowerRight.isEmpty() or lower.isLiquid()):
            self.swap(row+1, col+1)
        
        else:
            return #do nothing, no possible moves.     
            
            
class stone(element):
    
    def __init__(self,row,col,generation):
        super().__init__(row, col,generation)
        self.ID = 2
        self.name = 'stone'
        self.solid = True
        self.velocity = 1
        self.color = random.choice(["grey","grey64","grey39","grey70"])
    def update(self,generation):
        return #no update. Stone stays still no matter where it is
    
class water(element):
    
    def __init__(self,row,col,generation):
        super().__init__(row, col,generation)
        self.ID = 3
        self.name = "water"
        self.Liquid = True
        self.density = 4
        self.color = random.choice(["RoyalBlue1","RoyalBlue2"])
        self.velocity = random.choice([-1,1])
        
        
    def update(self, generation):
        row = self.row
        col = self.col
        #takes water element and updates accordingly
        bottomMiddle = element.getElementAtCell(row+1, col)
        middleLeft = element.getElementAtCell(row, col-1)
        middleRight = element.getElementAtCell(row, col+1)
        

        if bottomMiddle != None and bottomMiddle.isEmpty():

            #swap with lower cell if liquid or empty.
            fallRow = row+1
            self.swap(fallRow,col)
            
            
            targetRow = self.fallMultiplier + row
            
            targetElement = element.getElementAtCell(targetRow, col)
            
            while targetElement != None and not targetElement.isEmpty():
                targetRow -= 1 
                
                targetElement = element.getElementAtCell(targetRow, col)
                
            self.swap(targetRow, col)
            
            self.fallMultiplier += 1 
            
            
        else:
            #use self.velocity to do this!
            self.fallMultiplier = 0
            if bottomMiddle != None and bottomMiddle.isLiquid:
                #check other places to move 
                bottomLeft = self.getElementAtCell(row+1, col-1)
                bottomRight = self.getElementAtCell(row+1, col+1)
                if (bottomLeft != None and bottomLeft.isEmpty()):
                    self.swap(row+1, col-1)  
                    return
                elif bottomRight != None and bottomRight.isEmpty():
                    self.swap(row+1, col+1)
                    return
                 
            if self.velocity == 1:
                #velocity has water moving left
                if middleRight != None and middleRight.isEmpty():
                    self.swap(row, col+1)
                else:
                    self.velocity = -1
                    
            elif self.velocity == -1:
                if middleLeft != None and middleLeft.isEmpty():
                    self.swap(row,col-1)
                else:    
                    self.velocity = 1
                    
class salt(element):
    
    def __init__(self, row, col, generation):
        super().__init__(row, col, generation)
        
        #salt acts like sand, but has a change to float and dissolve in water
        self.Solid = True
        self.ID = 4
        self.color = random.choice(["pink","IndianRed1","IndianRed2","RosyBrown2"])
        self.disolveChange = 2
        
        self.floatChance = 55
        
    def update(self, generation):
        #update itself like sand, but can disolve if in water. More water surrounded by, greater dislolve chances.

        row = self.row
        col = self.col

        if self.evaporates():
            self.addElementID(0, row, col)
            #turns element into empty (disolves)
 
        else:
            #do movement. similar to sand, but with float properties. 
            bottomMiddle = self.getElementAtCell(row+1, col)

                
            if bottomMiddle != None and bottomMiddle.isEmpty():

                #swap with lower cell if liquid or empty.
                fallRow = row+1
                self.swap(fallRow,col)
                
                
                targetRow = self.fallMultiplier + row
                
                targetElement = element.getElementAtCell(targetRow, col)
                
                while targetElement != None and not targetElement.isEmpty():
                    targetRow -= 1 
                    
                    targetElement = element.getElementAtCell(targetRow, col)
                    
                self.swap(targetRow, col)
                
                self.fallMultiplier += 1 
            
            else:
                #alternate movement. 
                bottomLeft = self.getElementAtCell(row+1, col-1)
                bottomRight = self.getElementAtCell(row+1,col+1)
                topMiddle = self.getElementAtCell(row-1, col)
            
                if self.floats():
                    self.swap(row-1, col)
                    
                elif bottomMiddle != None and bottomMiddle.isLiquid():
                    #bottom middle element is liquid, fall down
                    self.swap(row+1, col)
                    
                elif bottomLeft != None and (bottomLeft.isEmpty() or bottomLeft.isLiquid()):
                    self.swap(row+1,col-1)
                    
                elif bottomRight != None and (bottomRight.isEmpty() or bottomRight.isLiquid()):
                    self.swap(row+1,col+1)
                    
    def floats(self):
        randomVal = random.randint(0, 100)
        
        topElement = self.getElementAtCell(self.row-1, self.col)
        if randomVal <= self.floatChance and topElement.isLiquid():
            return True
        
        else:
            return False
                
        
    def evaporates(self):
        
        surroundingLiquids = self.getSurroundingLiquids()

        disolveChance = surroundingLiquids * 5/8 #5% per 8 liquid
        randomVal = random.randint(1,100)
        
        if randomVal <= disolveChance:
            return True
        else:
            return False
    
    def getSurroundingLiquids(self):
        
        surroundingElements = self.getSurroundingElements() 
        liquids = 0
        
        for element in surroundingElements:
            
            if element!= None and element.isLiquid():
                #3 is liquid element
                liquids += 1    
            
        
        return liquids

class dirt(element):
    #element jumps around randomly and then falls down. if 
    
    def __init__(self, row, col, generation):
        super().__init__(row, col, generation)

        self.Solid = True
        self.ID = 5
        self.color = random.choice(["brown","saddleBrown"])
        
        
    def update(self, generation):
        # if self.updates != generation:
        #     #make sure not to double update solid
        #     return 
        #todo randomize BR/BL movement 
        #if gen = updates, update board as not to double count 
        
        row = self.row
        col = self.col
        
        #looks at below, bottomleft, bottom right elements, and swaps if empty
        lower = element.getElementAtCell(row+1, col)

        
        
        # != None makes sure getElementAtCell returns an object and isnt out of bounds
        if lower != None and (lower.isEmpty()):
            #swap with lower cell if liquid or empty.
            fallRow = row+1
            self.swap(fallRow,col)
            
            
            targetRow = self.fallMultiplier + row
            
            targetElement = element.getElementAtCell(targetRow, col)
            
            while targetElement != None and not targetElement.isEmpty():
                targetRow -= 1 
                
                targetElement = element.getElementAtCell(targetRow, col)
                
            self.swap(targetRow, col)
            
            self.fallMultiplier += 1 
            
            return
        #on the ground, reset multiplier to zero
        self.fallMultiplier = 0 
        
        if lower != None and lower.isLiquid():
            #if lower element is liquid, swap 
            
            self.swap(row+1,col)
        
        
        else:
            return #do nothing, no possible moves.     



class lava(element):


    def __init__(self, row, col, generation):
        super().__init__(row, col, generation)
        self.velocity = random.choice([-1,1])
        self.Liquid = True
        self.ID = 6
        self.color = random.choice(["red","red2","dark orange","orange red"])

    
    def update(self,generation):
        #flows like liquid, but slower movement. Whenever touches water, turn to stone. 
        row = self.row
        col = self.col
        
        self.meltSurroundings()
        
        if element.boardGeneration % 2 == 0:
            #to slow movement, only move on even generations
            return

        bottomMiddle = self.getElementAtCell(row+1, col)
        Left = self.getElementAtCell(row, col-1)
        Right = self.getElementAtCell(row, col+1)
        
        if bottomMiddle != None and bottomMiddle.isEmpty():
            self.swap(row+1, col)
        
        else:
            if self.velocity == -1:
                #leftward movement
                if Left != None and Left.isEmpty():
                    self.swap(row, col-1)
                    
                else:
                    self.velocity = self.velocity*-1
                    
            elif self.velocity == 1:
                #rightward movement
                if Right != None and Right.isEmpty():
                    self.swap(row, col+1)
                    
                else:
                    self.velocity = self.velocity * -1
            
    


    def meltSurroundings(self):
        
        #turn salt and sand into empty. 
        row = self.row
        col = self.col
        directions = [(0,-1),(-1,0),(0,1),(1,0)]
        
        for direction in directions:
            
            drow, dcol = direction
            
            elementObject = element.getElementAtCell(row+drow, col+dcol)
            
            if elementObject != None:
                elementID = elementObject.ID
                
                if elementID == 3:
                    #if water, turn water to stone
                    self.addElementID(2, row+drow, col+dcol)            
                elif elementID == 4:
                    self.destroyElement(row+drow, col+dcol)
    
            

    # pass


    

        
def print2dList(a):
    if (a == []): print([]); return
    rows, cols = len(a), len(a[0])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(str(a[row][col])) for row in range(rows)])
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).ljust(colWidths[col]), end='')
        print(' ]')
    print(']')

