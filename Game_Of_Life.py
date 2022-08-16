
import random

class GameOfLife():
    
    def __init__(self,board, onPercent):
        
        self.onPercent = onPercent
        self.board = board #2d list of cells, either 1 or 0 
        self.generation = 0
        self.bRows = len(board)
        self.bCols = len(board[0])
        self.population = 0
        
    def getCell(self,row,col):
        return self.board[row][col]
        
    def updateOnPercent(self,onPercent):
        self.onPercent = onPercent
        
    def updateBoard(self):
        #creates empty 2d array board      
        tempPopulation = 0  
        newBoard = [ ([0] * self.bCols) for row in range(self.bRows) ]
        
        #update newGrid cells according to self.board
        for row in range(self.bRows):
            for col in range(self.bCols):
                
                newState = self.getState(row,col)
                
                if newState == 1: 
                    tempPopulation += 1
                    
                newBoard[row][col] = newState
        
        #make self.board equal to newGrid
        self.board = newBoard
        self.population = tempPopulation
        #goes through every element in board and updates position into self
        self.generation += 1
    
    def getState(self,cellRow,cellCol):
        
        
        originalState = self.board[cellRow][cellCol]
        
        neighbors = self.getNeighbors(cellRow, cellCol)
        
        #does logic using neighbors and original state 
        if originalState == 1:
            #cell originally alive
            if neighbors >= 4:
                finalState = 0 
            elif neighbors <= 1:
                finalState = 0
            else:
                finalState = 1
        elif originalState == 0:
            #cell originally dead 
            if neighbors == 3:
                finalState = 1
            else:
                finalState = 0
        
        return finalState 
    
    def turnOnCell(self,row,col):
        
        self.board[row][col] = 1
    
    def flipCell(self,row,col):
        #flips state of element at board in that area
        original = self.board[row][col]
        
        if original == 0:
            new = 1
        elif original == 1:
            new = 0
            
        self.board[row][col] = new
    
    def getNeighbors(self,cellRow,cellCol):
        #? returns how many cells around cellRow and cellCol are alive (1's)
        neighbors = 0
        
        for rowChange in [-1,0,1]:
            for colChange in [-1,0,1]:
                neighborRow = cellRow + rowChange
                neighborCol = cellCol + colChange
                
                #factors in out of bounds errors
                if neighborRow < 0:
                    neighborRow = self.bRows - 1
                elif neighborRow >= self.bRows:
                    neighborRow = 0
                    
                if neighborCol < 0:
                    neighborCol = self.bCols -1 
                elif neighborCol >= self.bCols:
                    neighborCol = 0
                    
                neighbors += self.board[neighborRow][neighborCol]
                    
                #makes sure we are not recounting the original rows                
        
        neighbors -= self.board[cellRow][cellCol]
                    
        return neighbors
    
    def randomPopularization(self):
        #using an on parameter (int from 0-100), randomize cells being on or off in board for a random effect. 
        
        for row in range(self.bRows):
            for col in range(self.bCols):

                self.weightedFlipCell(row,col,self.onPercent)   

    def weightedFlipCell(self,row,col,onPercent):
        
        #if passes onPercent, flip cell. Otherwise, dont 
        randVal = random.randint(0,100)
        
        if randVal <= onPercent:
            self.flipCell(row,col)

        
    def columnStarter(self):
        #changes states across columns in patter
        
        for row in range(self.bRows):
            for col in range(self.bRows):
                
                if col%2 == 0:
                    #only draw things in columns
                    self.weightedFlipCell(row, col,self.onPercent)
        
    def rowStarter(self):
        #changes states across rows in pattern
        
        for row in range(0,self.bRows, 2):
            
            for col in range(self.bCols):
                
                self.weightedFlipCell(row,col,self.onPercent)
                
    def checkerPopularization(self):
        
        self.rowStarter()
        self.columnStarter()
    
    def centerClusterPopularization(self):
        
        midR = self.bRows//2
        midC = self.bCols//2
        maxDist = self.distance(midR, midC, 0, 0)
        
        minDist = 0
         
        #closer to center the board is, the more likely a thing will spawn
        for row in range(self.bRows):
            for col in range(self.bCols):
                
                dist = self.distance(midR, midC, row, col)
                
                #value 0-100. 100 is max dist, 0 is min dist
                regDist = 100*(dist-minDist)/(maxDist-minDist)
                
                onPercent = 75 - regDist
                
                self.weightedFlipCell(row, col, onPercent)
                #greater distance, less change to spawn. first, regularize distance
                
    def distance(self, x1,y1,x2,y2):
        
        return (((x1-x2)**2 + (y1-y2)**2)**0.5)
        