class WolframGrid():
    #?wolfram grid is a class of the entire grid, not just cell.
    
    
    def __init__(self,grid,rule):
        self.grid = grid
        self.rule = rule
        self.ruleset = self.getRuleset(rule) #? ex. 1,0,1,0,1,0,1
        self.generation = 0
        self.neighborhoodMap = ['111','110','101','100','011','010','001','000']
        print(self.grid)
        self.maxCell = len(self.grid)
    
    def updateGeneration(self):
        #updates every cell on grid into self.grid, and incriments generation
        newGrid = self.grid + []
        
        for cellIndex in range(len(newGrid)):
            #update every grid based off of cell and rules
            cellNeighborhood = self.getNeighborhood(cellIndex)
            ruleIndex = self.neighborhoodMap.index(cellNeighborhood) #todo get neighborhood of cell from self.grid
            
            cellState = self.ruleset[ruleIndex]
            newGrid[cellIndex] = cellState
            
        #updates these instance variables
        newIntGrid = [int(x) for x in newGrid] #turns '1' into 1
        self.grid = newIntGrid
        self.generation += 1
        
        return self.generation, self.grid
        
    def getNeighborhood(self, cellIndex):
        #returns "000" of cells left and right of cell 
        leftIndex = cellIndex - 1
        rightIndex = cellIndex + 1
        if leftIndex < 0:
            leftIndex = len(self.grid) - 1
        elif rightIndex >= len(self.grid):
            rightIndex = 0
        leftState = self.grid[leftIndex]
        rightState = self.grid[rightIndex]
        currentState  = self.grid[cellIndex]
            
        neighborhood = f"{leftState}{currentState}{rightState}"
        return neighborhood
        
    def getRuleset(self, rule):
        rule = self.validateRule(rule)
        
        #takes rule and converts to list of binary digits of rule number (8 digits long)
        rulesetString = str(bin(rule))
        rulesetString = rulesetString[0:1] + rulesetString[2:]
        while len(rulesetString) < 8:
            rulesetString = "0" + rulesetString
            
        ruleset = list(rulesetString) #list of split number
        
        return ruleset
    
    def validateRule(self, rule):
        #makes sure rule between 0-256, and integer
        rule = int(rule)
        if rule > 256:
            rule = 256
        elif rule < 0:
            rule = 0
        return rule
        
    def reallocateGrid(self, newGrid):
        self.grid = newGrid

#!tutorial of how to use WolframGrid object class

#outside of object, lets test this object. 

#Generation 0
gridStr = "00000001000000"
originalGrid = list(gridStr)

rule = 90

wolframGridObject = WolframGrid(originalGrid, rule) 

iterations = 30 #times you want simulation to run
print("".join(gridStr))
for iteration in range(iterations):
    #iterates as many generations as you want
    #todo this should make new array that has the entire grid updated 
    wolframGridObject.updateGeneration() #updates self.grid attributes cells
    newGrid = wolframGridObject.grid #gets self.grid attribute to show
    
    print(newGrid)
    
    
