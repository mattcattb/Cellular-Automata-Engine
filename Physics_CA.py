
#? the physics grid object stores the entire 3d list within it for 
#?keep track of what has and hasnt been updated to not have tiles teleport
import random
class Physics_Grid():
    import random
    #class Variables
    
    elementNames = ["empty","sand","stone","water"]
    #index is used to index into each element. air = 0, sand = 1 etc
    liquidNames = ["water"]
    solidNames = ["sand", "stone"]
    
    
    def __init__(self,board):
        self.board = board #initially, board should all be zero
        self.generation = 0
        self.bRows = len(board)
        self.bCols = len(board[0])
        # self.newBoard = [ ([0] * self.bCols) for row in range(self.bRows) ]
        self.elements = len(self.elementNames)
        
    def updateBoard(self):
        #?goes though each grid and updates!
        
        # self.newBoard = [ ([0] * self.bCols) for row in range(self.bRows) ]
        
        for iteration in range(self.bRows):
            #start from bottom of row to top of row 
            row = self.bRows - iteration - 1
            for col in range(self.bCols):
                #cycel through each elemetn
                elementID = self.board[row][col]
                elementName = self.elementNames[elementID]
                self.updateCell(elementName,row,col)
                
        #set self.board = self.newBoard
        # self.board = self.newBoard
        self.generation += 1
                
    def updateCell(self, elementName, eRow, eCol):
        #get cell type, 
        #find behavior based off 
        
        if elementName == "empty":
            #dont change anything 
            return 
        
        elif elementName == "sand":
            
            self.updateSand(eRow,eCol)
            
        elif elementName == "stone":
            
            self.updateStone(eRow,eCol)
        elif elementName == "water":
            
            self.updateWater(eRow,eCol)
        
    def updateSand(self, eRow, eCol):
        #check lower element, if it is empty, move there.
        #if full, check lower left and lower right element and move there.
        #element is name
        
        BottomMiddle = self.isEmpty((eRow+1, eCol))
        BottomMiddleLiquid = self.isLiquid(eRow+1,eCol)
        
        BottomRight = self.isEmpty((eRow+1,eCol+1))
        BottomRightLiquid = self.isLiquid(eRow+1,eCol+1)
        
        BottomLeft = self.isEmpty((eRow+1, eCol-1))
        BottomLeftLiquid = self.isLiquid(eRow+1, eCol-1)
        
        if BottomMiddle or BottomMiddleLiquid:
            self.swap((eRow,eCol),(eRow +1,eCol)) 
        
        elif ((BottomLeft or BottomLeftLiquid) and (BottomRight or BottomRightLiquid)):
            #if both empty, swap randomly into 1
            dir = random.choice([-1,1])
            self.swap((eRow,eCol),(eRow +1,eCol+dir))
        
        elif BottomLeft or BottomLeftLiquid:
            self.swap((eRow,eCol),(eRow +1,eCol - 1))
        
        elif BottomRight or BottomRightLiquid:
            self.swap((eRow,eCol),(eRow +1,eCol + 1))
        else:
            #all empty 
            return
          
    def updateStone(self, eRow,eCol):
        #stone stays the same no matter what. 
        
        self.board[eRow][eCol] = 2
          
    def updateWater(self, eRow,eCol):
        #water will swap left and right if the bottom two areas are open. 
        #locations:   BM     ML    MR     
        locations = [(eRow+1,eCol+0),(eRow,eCol-1),(eRow,eCol+1)]
        
        
        if self.isEmpty(locations[0]):
            
            self.swap((eRow, eCol), locations[0])
        
        elif self.isEmpty(locations[1]) and self.isEmpty(locations[2]):
            
            self.swap((eRow,eCol),locations[random.choice([1,2])])
        
        elif self.isEmpty(locations[1]):

            self.swap((eRow,eCol),locations[1])
        
        elif self.isEmpty(locations[2]):

            self.swap((eRow,eCol),locations[2])
        else:
            #no areas found 
            return        
            
    def swap(self, aPosition, bPosition):
        #? swaps 2 elements a and b
        
        aRow, aCol = aPosition
        bRow, bCol = bPosition 
        aElementID = self.board[aRow][aCol]
        bElementID = self.board[bRow][bCol]
        
        self.board[aRow][aCol] = bElementID
        
        self.board[bRow][bCol] = aElementID
        
        #element is the element number
        
    def getElementID(self,elementName):
        return self.elementNames.index(elementName)
    
    def getElementName(self, elementID):
        return self.elementNames[elementID]
        
    def getElementFromCell(self,row,col):
        #returns element in row,col 
        if (row < self.bRows and row >= 0) and (col < self.bCols and col >= 0): 
            return self.elementNames[self.board[row][col]]
        else:
            return "invalid"
        
    def inBounds(self,row,col):
        
        if ((row >= self.bRows or row < 0) 
            or (col >= self.bCols or col < 0)):
            return False
        else:
            return True 
        
    def isEmpty(self, position):
        #if out of bounds or full, return False 
        #if in bounds and empty, return False
        row,col = position
        if not self.inBounds(row, col):
            #out of bounds
            return False
            
        elif self.board[row][col] != 0:
            #isn't empty 
            return False
        
        elif self.board[row][col] == 0:
            #is empty 
            return True
        
    def inBounds(self,row,col):
        if ((row >= self.bRows or row < 0) 
            or (col >= self.bCols or col < 0)):
            #out of bounds
            return False
        else:
            return True
        
    def isLiquid(self,row,col):
        #true if is liquid, false if not liquid
        if not self.inBounds(row, col):
            return
        
        
        elementID = self.board[row][col]
    
        elementName = self.getElementName(elementID)
        
        if elementName in self.liquidNames:
            
            return True
        else:
            return False
       
        
        
    def editBoard(self, row, col, elementID):
        #changes row,col to element
        self.board[row][col] = elementID
        

#testing!!!

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


originalGrid = [[0,1,3],
                [0,2,0],
                [0,0,0]]

CA = Physics_Grid(originalGrid)
gens = 4

print2dList(CA.board)

for it in range(3):
    
    CA.updateBoard()
    print2dList(CA.board)