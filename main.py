
from Wolfram_Grid import WolframGrid
from Game_Of_Life import *
from cmu_112_graphics import *
from Physics_CA import *

from Element_Objects import *

"""
    Modes: 
        -wolframMode
        -GameOfLifeMode
        -menuMode
"""
#TODO LIST: Change dimensions of board



##########################################
# Setup (initialization)
##########################################

def appStarted(app):
    #I need to be able to pass objects into the board 
    resetGame(app)
    pass

def resetGame(app):
    #reset game
    app.mode = "menuMode"
    
    initSettings(app)
    
def runGame():
    
    #! fixed width and heigth. need to change this to be resizable. 
    width = 1000
    height = 700
    runApp(width=width, height=height)


##########################################
# menuMode
##########################################
#? Home screen

def menuMode_keyPressed(app,event):
    
    if event.key == "1":
        app.mode = "wolframMode"
        initWolframSettings(app)
    elif event.key == "2":
        app.mode = "GameOfLifeMode"
        initGameOfLifeSettings(app)
    elif event.key == "3":
        app.mode = "elementMode"
        initElementSettings(app)
    elif event.key == "s":
        app.mode = "settingsMode"
        
def menuMode_redrawAll(app,canvas):
    drawBlackBackground(app,canvas)
    drawTitle(app,canvas)
    
def drawTitle(app,canvas):
    
    canvas.create_text(app.width/2, app.height/2, text="Cellular Automata Engine",
                       fill="White", font="Helvetica 26 bold underline")
    
    helpText = """
                Press 1 for Wolfram 1D Automata
                Press 2 for Game Of Life 2D Automata 
                Press 3 for Physics Engine
                
                Press S for Settings Menu
                
                """
    
    canvas.create_text(app.width/2, app.height/4 * 3 , text= helpText,
                       fill="White", font="Helvetica 14")


##########################################
# Settings
##########################################

def initSettings(app):

    app.timerDelay = 50
    
    ##do not ch
    app.wolframCols = 60
    app.wolframRows = 60
    
    app.wolframMargin = app.height//30
    
    #min 10 max 100
    app.GameOfLifeRows = 25
    app.GameOfLifeCols = app.GameOfLifeRows
    
    app.GameOfLifeMargin = app.height/30
    
    app.physicsRows = 50
    app.physicsCols = 50
    
    app.physicsMargin = app.height/30
    
    #min 10, max 75
    app.elementCols = 30
    app.elementRows = app.elementCols
    app.elementMargin = app.height/30
    

def settingsMode_keyPressed(app,event):

    if event.key == "b":
        app.mode = "menuMode"
    elif event.key == "[":
        #decrease size of GOL
        
        if app.GameOfLifeCols >= 15:
            
            app.GameOfLifeCols -= 5
            app.GameOfLifeRows = app.GameOfLifeCols
            
    elif event.key == "]":
        #increase size of GOL
        
        if app.GameOfLifeCols <= 75:
            app.GameOfLifeCols += 5
            app.GameOfLifeRows = app.GameOfLifeCols
        
    elif event.key == "i":
        #decrase physics size
        if app.elementCols >= 15:
            
            app.elementCols -= 5
            app.elementRows = app.elementCols
        
    elif event.key == "o":
        #increase physics size  
        
        if app.elementCols <= 75:
            app.elementCols += 5
            app.elementRows = app.elementCols  
        
        
def settingsMode_redrawAll(app,canvas):
    drawButtons(app,canvas)
    drawSettingsTitle(app, canvas)

def drawSettingsTitle(app,canvas):
    
    x0 = app.width/2
    y0 = app.GameOfLifeMargin * 3
    
    canvas.create_text(x0,y0,text = "Settings", fill = "White", font="Helvetica 26 bold ")

def drawButtons(app,canvas):
    
    dataText = [f"Game of Life Size: {app.GameOfLifeCols}x{app.GameOfLifeRows}",
                f"Physics Engine Size: {app.elementCols}x{app.elementRows}"]
    
    x0 = app.width/2
    
    y0 = app.GameOfLifeMargin *5
    for text in dataText:
        canvas.create_text(x0,y0, text = text, font = "Helvetica 20 bold")
        
        y0 += app.GameOfLifeMargin *3
        
    helpText = ["use [ and ] to change Game of Life Size",
                "use i and o to change Physics Engine Size",
                "exit mode with b"]
    
    y1 = y0 + app.GameOfLifeMargin*3
    
    for text in helpText:
        canvas.create_text(x0,y1,text = text, font = "Helvetica 14")
        y1 += app.GameOfLifeMargin*2
        

##########################################
# wolframMode
##########################################
#? Wolfram CA 


def initWolframSettings(app):
    #?wolfram settings. should be allowed to be changed in splashscreen
        
    app.rule = 90
    app.timerDelay = 50
    
    app.changingRule = False
    app.wolframPaused = True
    
    initWolframBoard(app)
    
def initWolframBoard(app):
    #?wolframBoard data x0, x1, y0, y1, margin
    
    #use app.wolframRows and app.wolframCols
    
    
    #! wolfram board and object! very important!!!!!
    app.wolframBoard = [ ([0] * app.wolframCols) for row in range(app.wolframRows)]
    
    app.wolframObject = WolframGrid(app.wolframBoard[0], app.rule)
    
    app.boardWidth = app.width -app.wolframMargin*2
    app.boardHeight = app.height - app.wolframMargin*2
    
    cellWidth = app.boardWidth/app.wolframCols
    
    cellHeight = app.boardHeight/app.wolframRows
    
    app.wolframCellSize = min(cellWidth,cellHeight)
    
    app.wolframBoardx0 = app.wolframMargin
    app.wolframBoardx1 = app.wolframBoardx0 + app.wolframCellSize * app.wolframCols
    app.wolframBoardy0 = app.wolframMargin
    app.wolframBoardy1 = app.wolframBoardy0 + app.wolframCellSize * app.wolframRows
    

    
    
def pointInWolframGrid(app,x,y):  
    return (app.wolframBoardx0 <= x <= app.wolframBoardx1 and app.wolframBoardy0 <= y <= app.wolframBoardy1)

def getWolframCell(app, x, y):
    #? return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.wolframMargin) / app.wolframCellSize)
    col = int((x - app.wolframMargin) / app.wolframCellSize)
    
    return row,col

def changeWolframCellState(app,row,col):
    #?changes cell in app.board row,col from 0-1 or 1-0 
    state = app.wolframBoard[row][col]
    
    if state == 0:
        newState = 1
    
    elif state == 1:
        newState = 0
    
    app.wolframBoard[row][col] = newState

def wolframMode_timerFired(app):
    #?whenever timer fired and app not paused, update cell geneations
    
    if app.wolframPaused:
        return 
    
    updateWolframCA(app)

def resetWolframBoard(app,event):
    app.wolframPaused = True
    initWolframBoard(app)

def wolframMode_keyPressed(app,event):
    
    
    if event.key in "0123456789" and app.changingRule:
        
        app.ruleStr += event.key 
    
    if event.key == "p":
        #pause cells
        app.wolframPaused = not app.wolframPaused
        
    elif event.key == "r":
        #restart cells
        #! reset board 
        app.wolframPaused = True
        initWolframBoard(app)
        
    elif event.key == "b":
        #go back to main screen
        
        app.mode = "menuMode"
        
    elif event.key == "l":
        app.changingRule = not app.changingRule
        
        if app.changingRule:
            app.wolframPaused = True
            app.ruleStr = ""
                
        if not app.changingRule:
            #changed from changing rule, to no longer changing rule.
            app.wolframPaused = False
            #! make sure cannot go out of bounds
            app.rule = int(app.ruleStr)
            
            resetWolframBoard(app, event)
    
    elif event.key == "[":
        #lower speed 
        
        if app.timerDelay <= 1000:
            app.timerDelay += 10
            
    elif event.key == "]":
        #raise and lower speed
        if app.timerDelay > 10:
            app.timerDelay -= 10

    elif event.key == "h":
        app.showWolframHelp = not app.showWolframHelp

          
def wolframMode_mousePressed(app,event):
    #Todo toggle pause, reset board 
    app.cellsDragged = set()
    
    if pointInWolframGrid(app, event.x, event.y):
        #changes boards value based on this click
        cellRow, cellCol = getWolframCell(app,event.x,event.y)
        if cellRow == 0:
            changeWolframCellState(app,cellRow,cellCol)

def wolframMode_mouseDragged(app, event):
    
    if pointInWolframGrid(app, event.x, event.y):
        (row,col) = getWolframCell(app, event.x, event.y)
        
        if (row,col) not in app.cellsDragged:
            changeWolframCellState(app,row,col)
            app.cellsDragged.add((row,col))        

def updateWolframCA(app):
    #! SUPER IMPORTANT! updates current row using wolfram grid object!!!
    
    if app.wolframObject.generation < app.wolframRows - 1:
        #will only update if there is space in grid to update
        gen, newGrid = app.wolframObject.updateGeneration()
        
        app.wolframBoard[gen] = newGrid
        
    
    pass

def wolframMode_redrawAll(app, canvas):
    drawBlackBackground(app,canvas)
    drawWolframBoard(app,canvas)
    drawWolframRules(app,canvas)
    
    
def drawWolframRules(app,canvas):
    
    #draw a big box that says the current rule being used 
    
    x0 = app.wolframBoardx1 + app.wolframMargin*3
    x1 = x0 + 150
    y0 = app.wolframBoardy0 + app.wolframMargin
    y1 = y0 + 100
    

    
    canvas.create_rectangle(x0,y0,x1,y1,fill = "white")
    
    canvas.create_text((x0+x1)/2,(y0+y1)/2, text = f"Rule {app.rule}", font="Helvetica 26 bold ") 
    

    
    ty0 = (y0+y1)/2 + app.wolframMargin*3
    
    helpText = ["b - return to main menu",
                "r - reset board", 
                "p - pause/unpause", 
                "l - change rule by",
                "using numbers to type,",
                "and then pressing", 
                "l to lock in.",
                "r - Reset",
                "[ / ] - slow or speed up animation",
                f"speed is {app.timerDelay}"]
    
    for text in helpText:
        
        canvas.create_text((x0+x1)/2,ty0, text = text, fill = "white", font = "Helvetica 9")
        ty0 += app.wolframMargin

    
    helpText = """
                Hey! Some cool patterns you 
                may want to look into are 
                30, 54, 60, 90, 102, 110, 
                150, 220, 182, 220. 
                Have fun exploring!
                
                """
    
    canvas.create_text((x0+x1)/2, app.height / 8 * 6,text = helpText, fill = "white", font = "Helvetica 9" )

def drawWolframBoard(app,canvas):
    x0 = app.wolframBoardx0 - app.wolframMargin/2
    x1 = app.wolframBoardx1 + app.wolframMargin/2
    y0 = app.wolframBoardy0 - app.wolframMargin/2
    y1 = app.wolframBoardy0 + app.wolframCellSize + app.wolframMargin/2
    
    canvas.create_rectangle(x0,y0,x1,y1, fill = "yellow")
    for row in range(app.wolframRows):
        for col in range(app.wolframCols):
            drawWolframCell(app,canvas,row,col)
    
def drawBlackBackground(app,canvas):
    
    canvas.create_rectangle(0,0,app.width,app.height,fill = "black")
    
def drawWolframCell(app,canvas,row,col):
    #draws cell in wolfram board 
    
    x0 = app.wolframBoardx0 + col* app.wolframCellSize    
    x1 = app.wolframBoardx0 + (col+1)*app.wolframCellSize
    y0 = app.wolframBoardy0 + row * app.wolframCellSize
    y1 = app.wolframBoardy0 + (row+1)*app.wolframCellSize
    
    element = app.wolframBoard[row][col]
    #color for states
    
    if element == 0:
        color = "white"
    elif element == 1:
        color = "black"
    
    canvas.create_rectangle(x0,y0,x1,y1, fill = color, width = 1)


##########################################
# GameOfLifeMode
##########################################
#? Game of Life Cellular Automata Screen

#todo :
"""
    -Change Board speed (slow or speed up)
    -Change Board dimensions somehow
    -drag and drop stuff onto board
    -change app.onPercent variable

"""

#!important
def initGameOfLifeSettings(app):
    
    initGameOfLifeCA(app)
    initGameOfLifeBoard(app)
    app.GameOfLifePaused = True
    
def initGameOfLifeCA(app):
    
    app.population = 0
    app.showGameOfLifeHelpScreen = True
    app.onPercent = 40
    app.brushSize = 1
    app.GameOfLifeBoard =  [ ([0] * app.GameOfLifeCols) for row in range(app.GameOfLifeRows)]
    
    app.GameOfLifeCA = GameOfLife(app.GameOfLifeBoard, app.onPercent)
    
    
def initGameOfLifeBoard(app):
    #uses rows cols and margin data to get board dimensions and create board grid. 

    
    boardWidth = app.width -app.GameOfLifeMargin*2
    boardHeight = app.height - app.GameOfLifeMargin*2
    
    cellWidth = boardWidth/app.GameOfLifeCols
    
    cellHeight = boardHeight/app.GameOfLifeRows
    
    app.GameOfLifeCellSize = min(cellWidth,cellHeight)
    
    app.GameOfLifeBoardx0 = app.GameOfLifeMargin
    app.GameOfLifeBoardx1 = app.GameOfLifeMargin + app.GameOfLifeCellSize * app.GameOfLifeCols
    app.GameOfLifeBoardy0 = app.GameOfLifeMargin
    app.GameOfLifeBoardy1 = app.GameOfLifeMargin + app.GameOfLifeCellSize * app.GameOfLifeRows
  
def changeGameOfLifeCellState(app,row,col):
    #?changes cell in app.board row,col from 0-1 or 1-0 
    state = app.GameOfLifeBoard[row][col]
    app.GameOfLife
    if state == 0:
        newState = 1
    elif state == 1:
        newState = 0
    
    app.GameOfLifeBoard[row][col] = newState
    
def pointInGameOfLifeGrid(app,x,y):  
    return (app.GameOfLifeBoardx0 <= x <= app.GameOfLifeBoardx1 and app.GameOfLifeBoardy0 <= y <= app.GameOfLifeBoardy1)

def getGameOfLifeCell(app, x, y):
    #? return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.GameOfLifeMargin) / app.GameOfLifeCellSize)
    col = int((x - app.GameOfLifeMargin) / app.GameOfLifeCellSize)
    
    return row,col

#!important
def updateGameOfLifeCA(app):
    #? Updates app.board using CA grid object 
    app.GameOfLifeCA.updateBoard()
    app.population = app.GameOfLifeCA.population
    
                          
def GameOfLifeMode_keyPressed(app,event):
    #Todo change grid colors to init board configurations
    
    if event.key == "p":
        app.GameOfLifePaused = not app.GameOfLifePaused
    
    elif event.key == "s":
        #step forward the cellular automata 
        app.GameOfLifePaused = True
        updateGameOfLifeCA(app)
        
    elif event.key == "r":
        
        initGameOfLifeSettings(app)
        
    elif event.key == "b":
        app.mode = "menuMode"
        
    elif event.key == "d":
        #todo make go backwards.
        pass

    elif event.key == "]":
        #lower speed 
        
        if app.timerDelay <= 1000:
            app.timerDelay += 10
            
        
        
    elif event.key == "[":
        #raise and lower speed
        if app.timerDelay > 10:
            app.timerDelay -= 10

    elif event.key == "h":
        app.showGameOfLifeHelpScreen = not app.showGameOfLifeHelpScreen

    #popularizations and grid starters
    if event.key == "1":
        #random popularization 
        app.GameOfLifeCA.randomPopularization() 
        
        pass
    elif event.key == "2":
        #checkered popularization
        app.GameOfLifeCA.checkerPopularization()
    
    elif event.key == "3":
        #center cluster popularization 
        #the closer you are to the center, the more likely will spawn
        app.GameOfLifeCA.centerClusterPopularization()
          
    elif event.key == "4":
        #spread cluster center
        pass

        
#!important
def GameOfLifeMode_mousePressed(app,event):
     
    app.cellsDragged = set()
    
    if pointInGameOfLifeGrid(app, event.x, event.y):
        #changes boards value based on this click
        cellRow, cellCol = getGameOfLifeCell(app,event.x,event.y)
        app.GameOfLifeCA.flipCell(cellRow,cellCol)
        
        

def GameOfLifeMode_mouseDragged(app, event):
    
    if pointInGameOfLifeGrid(app, event.x, event.y):
        (row,col) = getGameOfLifeCell(app, event.x, event.y)
        GameOfLifeBrushDraw(app, row, col)
    
def GameOfLifeBrushDraw(app, row, col):
    #square brush! 
    
    if app.brushSize == 1:
        
        # changeGameOfLifeCellState(app, row, col)
        app.GameOfLifeCA.flipCell(row,col)
        return 
    
    brushSize = app.brushSize - 1
    
    for drow in range(-brushSize, brushSize+1):
        diff = brushSize - abs(drow)
        for dcol in range(-diff, diff+1):
            
            app.GameOfLifeCA.turnOnCell(row,col)
            

#!important
def GameOfLifeMode_timerFired(app):
    
    if app.GameOfLifePaused:
        return 
    
    updateGameOfLifeCA(app)
    
    pass    

#!important
def GameOfLifeMode_redrawAll(app,canvas):
    drawGameOfLifeBackground(app,canvas)
    drawGameOfLifeBoard(app,canvas)
    drawGameOfLifeRules(app,canvas)
    drawGameOfLifeHelpScreen(app,canvas)
    
def drawGameOfLifeBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill = "black")
    
def drawGameOfLifeBoard(app,canvas):
    
    for row in range(app.GameOfLifeRows):
        for col in range(app.GameOfLifeCols):
            drawCell(app,canvas,row,col)
            
def drawCell(app,canvas,row,col):
    
    x0 = app.GameOfLifeBoardx0 + col* app.GameOfLifeCellSize    
    x1 = app.GameOfLifeBoardx0 + (col+1)*app.GameOfLifeCellSize
    y0 = app.GameOfLifeBoardy0 + row * app.GameOfLifeCellSize
    y1 = app.GameOfLifeBoardy0 + (row+1)*app.GameOfLifeCellSize
    
    element = app.GameOfLifeCA.getCell(row,col)
    #color for states
    
    if element == 0:
        color = "white"
    elif element == 1:
        color = "black"
    
    canvas.create_rectangle(x0,y0,x1,y1, fill = color, width = app.GameOfLifeCellSize//10+1)

def drawGameOfLifeRules(app,canvas):
    x0 = app.GameOfLifeBoardx1 + app.GameOfLifeMargin*3
    x1 = x0 + 150
    y0 = app.GameOfLifeBoardy0 + app.GameOfLifeMargin
    y1 = y0 + 100 
    
    canvas.create_rectangle(x0,y0,x1,y1, fill = "white")
    
    canvas.create_text((x0+x1)/2,(y0+y1)/2, text = f"Generation: {app.GameOfLifeCA.generation} ", fill = "black", font="Helvetica 15 bold ")

    ox0 = (x0 + x1)/2
    oy0 = y1 + app.GameOfLifeMargin * 3
    
    #list of rules and information
    
    rules = [f"Spawn Percent is {app.onPercent}",
             f"Board Speed is {app.timerDelay}",
             f"Population is {app.population}"] 
        
    for text in rules:
        
        canvas.create_text(ox0,oy0,text = text, font = "Helvetica 13", fill = "white")
        
        oy0 += 30


def drawGameOfLifeHelpScreen(app,canvas):
    #only show if toggled on
    
    if app.showGameOfLifeHelpScreen:
        
        x0 = app.GameOfLifeMargin*3
        x1 = app.width - app.GameOfLifeMargin*3
        
        y0 = app.elementMargin*3
        y1 = app.height - app.GameOfLifeMargin*3
        
        canvas.create_rectangle(x0,y0,x1,y1, fill = "White", width = 4)
        
        tx0 = app.width//2
        ty0 = y0 + app.GameOfLifeMargin *4
        
        canvas.create_text(tx0,ty0, text = "Key Mappings", font = "Helvetica 20")
        
        ty0 += app.GameOfLifeMargin *2
        
        helpText = ["h - Turn off help menu",
                    "b - go back to menu",
                    "s - skip forward generation", 
                    "p - pause simulation", 
                    "r - reset engine",
                    "[ / ] - slow or speed up animation",
                    "1 - random Popularization.", 
                    "2 - Checker Popularize", 
                    "3 - Center Cluster Popularize"]
        
        for text in helpText:
            
            canvas.create_text(tx0,ty0, text = text, fill = "black", font = "Helvetica 14")
            ty0 += app.GameOfLifeMargin*2


##########################################
# physicsMode
##########################################    
#!important
def initPhysicsSettings(app):
    #setsup physics Settings
    
    #when application starts, show help screen
    
    app.physicsPaused = True
    app.timerDelay = 20
    app.physicsBoard =  [ ([0] * app.physicsCols) for row in range(app.physicsRows)]
    
    initPhysicsBoard(app)
    initCA(app)
    
    #automatically choses the sand element
    app.selectedElement = 1
    app.brushSize = 1 #how large placement is 
    
def initPhysicsBoard(app):
    #?sets up board x0,x1,y0,y1 information
    
    app.PhysicsBoardWidth = app.width -app.physicsMargin*2
    app.PhysicsBoardHeight = app.height - app.physicsMargin*2
    cellWidth = app.PhysicsBoardWidth/app.physicsCols
    cellHeight = app.PhysicsBoardHeight/app.physicsRows
    
    app.physicsCellSize = min(cellHeight,cellWidth)
    
    app.physicsBoardx0 = app.physicsMargin
    app.physicsBoardx1 = app.physicsMargin + app.physicsCellSize*app.physicsCols
    app.physicsBoardy0 = app.physicsMargin
    app.physicsBoardy1 = app.physicsMargin + app.physicsCellSize*app.physicsRows
    
def initCA(app):
    
    #! possibly the most important object!
    app.physics_grid = Physics_Grid(app.physicsBoard)

def initIndicator(app):
    #element indicator, changes color to whatever element is selected

    color = getColor(app.selectedElement)

def getColor(elementID):
    
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
    

def pointInPhysicsGrid(app, x, y):  
    return (app.physicsBoardx0 <= x <= app.physicsBoardx1 and app.physicsBoardy0 <= y <= app.physicsBoardy1)

def getPhysicsCell(app, x, y):
    #? return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.physicsMargin) / app.physicsCellSize)
    col = int((x - app.physicsMargin) / app.physicsCellSize)
    
    return row,col

def changeElementState(app,row,col):
 
    #changes state based off what element is selected 
    #?changes cell in app.board row,col from 0-1 or 1-0 

    #selected element changed    
    newElementID = app.selectedElement
    if str(newElementID) in "0123" and inPhysicsBoardBounds(app,row, col):
        #to stop an out of bounds error
        app.physics_grid.editBoard(row,col,newElementID)

#!important       
def updatePhysicsCA(app):
    #? Updates app.board using CA grid object 
    app.physics_grid.updateBoard()
    app.board = app.physics_grid
    
def inPhysicsBoardBounds(app,row,col):
        #? returns true if element in row
        
        if ((row >= app.physicsRows or row < 0) 
            or (col >= app.physicsCols or col < 0)):
            #out of bounds
            return False
        else:
            return True    

def physicsMode_keyPressed(app,event):
    #Todo change grid colors to init board configurations
    
    if event.key == "p":
        app.physicsPaused = not app.physicsPaused
    
    elif event.key == "s":
        #step forward the cellular automata 
        app.physicsPaused = True
        
        updatePhysicsCA(app)
    
    elif event.key == "r":
        initPhysicsSettings(app)
        
    elif event.key == "o":
        #increase brush size
        if app.brushSize <= 6:
            app.brushSize += 1
    elif event.key == "i":
        #decrease brush size
        if app.brushSize > 1:
            app.brushSize -= 1
    elif event.key == "b":
        app.mode = "menuMode"
    
    elif event.key == "]":
        #lower speed 
        
        if app.timerDelay <= 1000:
            app.timerDelay += 10
            
        
        
    elif event.key == "[":
        #raise and lower speed
        if app.timerDelay > 10:
            app.timerDelay -= 10
    
    elif event.key == "h":
        app.showPhysicsHelpScreen = not app.showPhysicsHelpScreen
    
    if str(event.key) in "01234":
        app.selectedElement = int(event.key)

#!important
def physicsMode_mousePressed(app,event):
    #Todo toggle pause, reset board 
    app.cellsDragged = set()
    
    if pointInPhysicsGrid(app, event.x, event.y):
        #changes boards value based on this click
        cellRow, cellCol = getPhysicsCell(app,event.x,event.y)
        
        physicsBrushDraw(app,cellRow,cellCol)

def physicsMode_mouseDragged(app, event):
    #?when mouse is dragged, updates grid (pallet change) 
    
    if pointInPhysicsGrid(app, event.x, event.y):
        cellRow, cellCol = getPhysicsCell(app, event.x, event.y)
        
        if (cellRow, cellCol) not in app.cellsDragged:
            physicsBrushDraw(app,cellRow, cellCol)
            
            app.cellsDragged.add((cellRow, cellCol)) 
            
    #draw brush as well!!!!  
      
def physicsBrushDraw(app, row, col):
    #square brush! 
    
    brushSize = app.brushSize - 1
    
    for drow in range(-brushSize, brushSize+1):
        diff = brushSize - abs(drow)
        for dcol in range(-diff, diff+1):
            changeElementState(app, drow+row, dcol+col)
           
#!important
def physicsMode_timerFired(app):
    #? very important, updates physics engine grid using object
    if app.physicsPaused:
        return 
    
    updatePhysicsCA(app)
    
#!Important
def physicsMode_redrawAll(app,canvas):
    
    drawPhysicsBackground(app,canvas)
    drawPhysicsBoard(app,canvas)
    drawPalletFeatures(app, canvas)
    
def drawPhysicsBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill = "black")
    
def drawPhysicsBoard(app,canvas):

    for row in range(app.physicsRows):
        for col in range(app.physicsCols):
            drawPhysicsCell(app,canvas,row,col)
            
def drawPhysicsCell(app,canvas,row,col):
    
    x0 = app.physicsBoardx0 + col* app.physicsCellSize    
    x1 = app.physicsBoardx0 + (col+1)*app.physicsCellSize
    y0 = app.physicsBoardy0 + row * app.physicsCellSize
    y1 = app.physicsBoardy0 + (row+1)*app.physicsCellSize
    
    elementID = app.physics_grid.board[row][col]
    #color for states
    
    #remember, each number corresponds to a different element.
    
    color = getColor(elementID)
    
    canvas.create_rectangle(x0,y0,x1,y1, fill = color, width = app.physicsCellSize//20)
    
def drawPalletFeatures(app,canvas):
    #todo be able to switch elements by clicking on them, and change brush size too.
    
    #indicates what element is selected
    drawIndicatorCell(app,canvas)
    
    drawElementInfo(app,canvas)
    
def drawElementInfo(app,canvas):
    
    textElements = ["0 - Empty", " 1 - Sand", "2 - Stone", "3 - Water",
                    "press s to skip", "press p to pause", "press i/o to decrease/increase brush size",
                    "press r to reset engine", f"Brush Size: {app.brushSize}"]
    x = (app.physicsBoardx1+app.width)/2 + app.physicsMargin
    y = (app.physicsBoardy0 + app.physicsBoardy1)/4 * 1
    
    for text in textElements:
        canvas.create_text(x,y,text = text, fill = "white", font = "Helvetica 10")
        y+= app.physicsMargin
        
        
def drawIndicatorCell(app,canvas):
    
    elementID = app.selectedElement
    color = getColor(elementID)
    
    x0 = app.physicsBoardx1 + 50
    x1 = x0 + 50
    y0 = app.physicsBoardy0
    y1 = app.physicsBoardy0 + 50
    canvas.create_rectangle(x0,y0,x1,y1 , fill = color)
    canvas.create_text((x0+x1)/2,y1 + app.physicsMargin, text = "Current Element", fill = color, font = "Helvetica 10")

##########################################
# Element Prototype
##########################################

#!important
def initElementSettings(app):
    #setsup element Settings
    
    app.showElementHelpScreen = True
    
    app.elementsPaused = True
    app.timerDelay = 20
    app.elementBoard =  [ ([0] * app.elementCols) for row in range(app.elementRows)]
    
    initElementBoard(app)
    initElementCA(app)
    
    #automatically choses the sand element
    app.selectedElement = 1
    app.brushSize = 1 #how large placement is 
    
def initElementBoard(app):
    #?sets up board x0,x1,y0,y1 information
    
    app.elementBoardWidth = app.width -app.elementMargin*2
    app.elementBoardHeight = app.height - app.elementMargin*2
    cellWidth = app.elementBoardWidth/app.elementCols
    cellHeight = app.elementBoardHeight/app.elementRows
    
    app.elementCellSize = min(cellHeight,cellWidth)
    
    app.elementBoardx0 = app.elementMargin
    app.elementBoardx1 = app.elementMargin + app.elementCellSize*app.elementCols
    app.elementBoardy0 = app.elementMargin
    app.elementBoardy1 = app.elementMargin + app.elementCellSize*app.elementRows
    
def initElementCA(app):
    
    #! possibly the most important object!
    
    print("did this ")
    element.initEmptyBoard(app.elementRows, app.elementCols)

def initIndicator(app):
    #element indicator, changes color to whatever element is selected

    color = getColor(app.selectedElement)


def pointInElementGrid(app, x, y):  
    return (app.elementBoardx0 <= x <= app.elementBoardx1 and app.elementBoardy0 <= y <= app.elementBoardy1)

def getElementCell(app, x, y):
    #? return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.elementMargin) / app.elementCellSize)
    col = int((x - app.elementMargin) / app.elementCellSize)
    
    return row,col

def changeElementState(app,row,col):
    #! used to add new elements to CA.board!!!
    #changes state based off what element is selected 
    #?changes cell in app.board row,col from 0-1 or 1-0 

    #selected element changed    
    selectedElementID = app.selectedElement
    if str(selectedElementID) in "0123456" and element.inBounds(row, col):
        #to stop an out of bounds error
        #static update 
        element.addElementID(selectedElementID, row, col)

        
#!important       
def updateElementCA(app):
    #? Updates app.board using CA grid object 
    element.updateBoard()
     

def elementMode_keyPressed(app,event):
    #Todo change grid colors to init board configurations
    
    if event.key == "p":
        app.elementsPaused = not app.elementsPaused
    
    elif event.key == "s":
        #step forward the cellular automata 
        app.elementsPaused = True
        
        updateElementCA(app)
    
    elif event.key == "r":
        initElementSettings(app)
        
    elif event.key == "o":
        #increase brush size
        if app.brushSize <= 6:
            app.brushSize += 1
    elif event.key == "i":
        #decrease brush size
        if app.brushSize > 1:
            app.brushSize -= 1
    elif event.key == "b":
        app.mode = "menuMode"
    
    elif event.key == "h":
        app.showElementHelpScreen = not app.showElementHelpScreen
    
    if str(event.key) in "0123456":
        app.selectedElement = int(event.key)

#!important
def elementMode_mousePressed(app,event):
    #Todo toggle pause, reset board 
    app.cellsDragged = set()
    
    if pointInElementGrid(app, event.x, event.y):
        #changes boards value based on this click
        cellRow, cellCol = getElementCell(app,event.x,event.y)
        
        elementBrushDraw(app,cellRow,cellCol)

def elementMode_mouseDragged(app, event):
    #?when mouse is dragged, updates grid (pallet change) 
    
    if pointInElementGrid(app, event.x, event.y):
        cellRow, cellCol = getElementCell(app, event.x, event.y)
        
        if (cellRow, cellCol) not in app.cellsDragged:
            elementBrushDraw(app,cellRow, cellCol)
            
            app.cellsDragged.add((cellRow, cellCol)) 
            
    #draw brush as well!!!!  
      
def elementBrushDraw(app, row, col):
    #square brush! 
    
    brushSize = app.brushSize - 1
    
    for drow in range(-brushSize, brushSize+1):
        diff = brushSize - abs(drow)
        for dcol in range(-diff, diff+1):
            changeElementState(app, drow+row, dcol+col)
           
#!important
def elementMode_timerFired(app):
    #? very important, updates board engine grid using object
    if app.elementsPaused:
        return 
    
    updateElementCA(app)
    
#!Important
def elementMode_redrawAll(app,canvas):
    
    drawElementBackground(app,canvas)
    drawElementBoard(app,canvas)
    drawPalletFeatures(app, canvas)
    
def drawElementBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill = "black")
    
def drawElementBoard(app,canvas):

    for row in range(app.elementRows):
        for col in range(app.elementCols):
            drawElementCell(app,canvas,row,col)
            
def drawElementCell(app,canvas,row,col):
    
    x0 = app.elementBoardx0 + col* app.elementCellSize    
    x1 = app.elementBoardx0 + (col+1)*app.elementCellSize
    y0 = app.elementBoardy0 + row * app.elementCellSize
    y1 = app.elementBoardy0 + (row+1)*app.elementCellSize
    
    #color for states
    
    elementObject = element.getElementAtCell(row,col)
    
    #remember, each number corresponds to a different element.
    
    color = elementObject.color
    
    canvas.create_rectangle(x0,y0,x1,y1, fill = color, width = app.elementCellSize//20)
    
def drawPalletFeatures(app,canvas):
    #todo be able to switch elements by clicking on them, and change brush size too.
    
    #indicates what element is selected
    drawElementIndicatorCell(app,canvas)
    
    drawElementInfo2(app,canvas)
    drawElementHelpScreen(app,canvas)
    
def drawElementInfo2(app,canvas):
    
    textElements = ["0 - Empty", 
                    "1 - Sand",
                    "2 - Stone", 
                    "3 - Water", 
                    "4 - Salt",
                    "5 - Dirt",
                    "6 - Lava"
                    f"Brush Size: {app.brushSize}",
                    f"Engine Speed: {app.timerDelay}"]
    
    x = (app.elementBoardx1+app.width)/2 
    y = (app.elementBoardy0 + app.elementBoardy1)/4 * 1
    
    for text in textElements:
        color = "white" 
        
        if text[0] in "0123456":
            color = element.elementIDToColor(int(text[0]))
            
        canvas.create_text(x,y,text = text, fill = color, font = "Helvetica 20")
        y+= app.elementMargin*2
        
    
def drawElementIndicatorCell(app,canvas):
    
    elementID = app.selectedElement
    
    color = element.elementIDToColor(elementID)
    
    x0 = app.elementBoardx1 + 50
    x1 = x0 + 50
    y0 = app.elementBoardy0
    y1 = app.elementBoardy0 + 50
    canvas.create_rectangle(x0,y0,x1,y1 , fill = color)
    canvas.create_text((x0+x1)/2,y1 + app.elementMargin, text = "Current Element", fill = color, font = "Helvetica 10")

def drawElementHelpScreen(app,canvas):
    #only show if toggled on
    
    if app.showElementHelpScreen:
        
        x0 = app.elementMargin*3
        x1 = app.width - app.elementMargin*3
        
        y0 = app.elementMargin*3
        y1 = app.height - app.elementMargin*3
        
        canvas.create_rectangle(x0,y0,x1,y1, fill = "White", width = 4)
        
        tx0 = app.width//2
        ty0 = y0 + app.elementMargin *4
        
        canvas.create_text(tx0,ty0, text = "Key Mappings", font = "Helvetica 20")
        
        ty0 += app.elementMargin *2
        
        helpText = ["h - Turn off help menu",
                    "s - skip forward generation", 
                    "p - pause simulation", 
                    "i/o - decrease or increase brush size",
                    "r - reset engine",
                    "[ / ] - slow or speed up animation"]
        
        for text in helpText:
            
            canvas.create_text(tx0,ty0, text = text, fill = "black", font = "Helvetica 14")
            ty0 += app.elementMargin*2
    
def main():
    runGame()

if __name__ == '__main__':
    main()
