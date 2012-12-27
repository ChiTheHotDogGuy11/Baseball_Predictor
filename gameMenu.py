# events-example0.py

from Tkinter import *
import random
import makeTeamInGame
import gameGraphics
import GamePlay
import teamCreationGraphics
import mainMenu
import endGame
import tkSimpleDialog

def doubleMousePressed(event):
    canvas = event.widget.canvas
    eventx = event.x
    eventy = event.y
    if canvas.data["state"] == "creation":
        if canvas.data["teamSelectionProcess"]== True:
            teamCreationGraphics.doubleMousePressedPlayerSelect(canvas,eventx,eventy)
    elif canvas.data["state"] == "game":
        if canvas.data["changePitcher"] == True:
            GamePlay.changePitcherClick(canvas,eventx,eventy)
        if canvas.data["changeBatter"] == True:
            GamePlay.changeBatterClick(canvas,eventx,eventy)
        
    
    redrawAll(canvas)

def mousePressed(event):
    canvas = event.widget.canvas
    eventx = event.x
    eventy = event.y
    if canvas.data["state"] == "mainMenu":
        if canvas.data["displayHelpScreen"] == True:
            mainMenu.mousePressedInHelp(canvas,eventx,eventy)
        else:
            mainMenu.mousePressedInMenu(canvas,eventx,eventy)
            if canvas.data["state"] == "creation":
                teamCreation(canvas)
    if canvas.data["state"] == "creation":
        if canvas.data["teamSelectionProcess"]== True:
            teamCreationGraphics.mousePressedPlayerSelection(canvas,eventx,eventy)
        elif canvas.data["fixLineupOrder"] == True:
            teamCreationGraphics.fixLineupOrderPlayerSelection(canvas,eventx,eventy)
    if canvas.data["state"] == "game":
        GamePlay.soundChanger(canvas, eventx, eventy)
        gameGraphics.clickdrawHelpButton(canvas,eventx,eventy)
        if canvas.data["Player1Pause"] == True or canvas.data["Player2Pause"] == True:
            GamePlay.clickPlayerPause(canvas, eventx,eventy)
    if canvas.data["state"] == "endGame":
        endGame.mousePressedInMenu(canvas,eventx,eventy)
        if canvas.data["exportTeams"] == True:
            setUpTeams(canvas)
            canvas.data["exportTeams"] = False
        if canvas.data["state"] == "creation":
            teamCreation(canvas)
        if canvas.data["meanScoreReport"] == True:
            while True:
                message = "How many trials do you want to run?\n"
                message += "Minimum of 500 trials are required.\n"
                message += "There is a maximum of 10000 trials.\n"
                message += "These trials may take a while to run.\n"
                title = "Prompt"
                response = tkSimpleDialog.askstring(title, message)
                # make sure we get an integer response
                try:
                    if response == None:
                        break
                    response = int(response)
                    if response >= 500 and response <= 10000:
                        canvas.data["gameCounter"] = response
                        break
                except:
                    pass
            canvas.data["meanScoreReport"] = False
            if response != None:
                simulateResults(canvas)
    redrawAll(canvas)
    
def simulateResults(canvas):
    import tkMessageBox
    import scrape
    gameCounter = 0
    team1Scores = []
    team2Scores = []
    team1Wins = 0
    team2Wins = 0
    while True:
        if gameCounter > canvas.data["gameCounter"]:
            break
        setUpTeams(canvas)
        canvas.data["isSoundOn"] = False
        while canvas.data["isGameOver"] == False:
            GamePlay.runHalfInning(canvas)
        if canvas.data["Player1TotalRuns"] > canvas.data["Player2TotalRuns"]:
            team1Wins += 1
        else:
            team2Wins += 1
        team1Scores.append(canvas.data["Player1TotalRuns"])
        team2Scores.append(canvas.data["Player2TotalRuns"])
        gameCounter+= 1
    canvas.data["state"] = "endGame"
    canvas.data["displayFinalScoreBoard"] = False
    (team1StDev,team1Mean) = scrape.standardDev(team1Scores)
    (team2StDev,team2Mean) = scrape.standardDev(team2Scores)
    team1WinPercentage = round(float(team1Wins)/gameCounter,5)*100
    team2WinPercentage = round(float(team2Wins)/gameCounter,5)*100
    message = "The average runs scored per game for " + canvas.data["player1TeamName"] + " is " + str(round(team1Mean,3)) + ".\n"
    message += "The standard deviation of the runs scored per game for " + canvas.data["player1TeamName"] + " is " + str(round(team1StDev,3)) + ".\n"
    message += "The average runs scored per game for " + canvas.data["player2TeamName"] + " is " + str(round(team2Mean,3)) + ".\n"
    message += "The standard deviation of the runs scored per game for " + canvas.data["player2TeamName"] + " is " + str(round(team2StDev,3)) + ".\n"
    message += "The winning percentage for " + canvas.data["player1TeamName"] + " is " + str(team1WinPercentage) + "%.\n"
    message += "The winning percentage for " + canvas.data["player2TeamName"] + " is " + str(team2WinPercentage) + "%.\n"
    title = "Statistics"
    tkMessageBox.showinfo(title, message)

def keyPressed(event):
    canvas = event.widget.canvas
    if canvas.data["state"] == "creation":
        ################
        #### This is for team name creation purposes
        if canvas.data["team1Made"] == False:
            if (event.char >= "a" and event.char <= "z") or (event.char >= "A" and event.char <= "Z"):
                canvas.data["team1Name"] += event.char
            elif event.keysym == "BackSpace":
                if len(canvas.data["team1Name"]) > 0:
                    canvas.data["team1Name"] = canvas.data["team1Name"][:len(canvas.data["team1Name"])-1]
            elif event.keysym == "Return":
                if len(canvas.data["team1Name"]) != 0:
                    canvas.data["team1Made"] = True
        elif canvas.data["team1Made"] == True and canvas.data["teamsNamesMade"] == False:
            if (event.char >= "a" and event.char <= "z") or (event.char >= "A" and event.char <= "Z"):
                canvas.data["team2Name"] += event.char
            elif event.keysym == "BackSpace":
                if len(canvas.data["team2Name"]) > 0:
                    canvas.data["team2Name"] = canvas.data["team2Name"][:len(canvas.data["team2Name"])-1]
            elif event.keysym == "Return":
                if len(canvas.data["team2Name"]) != 0:
                    canvas.data["teamsNamesMade"] = True
                    canvas.data["teamSelectionProcess"] = True
        elif canvas.data["teamSelectionProcess"] == True:
            # go to the next page for player selection
            if event.keysym == "Down" and canvas.data["playerSelectionPage"]< canvas.data["playersPages"]:
                canvas.data["playerSelectionPage"] += 1
            elif event.keysym == "Up" and canvas.data["playerSelectionPage"] > 0 :
                canvas.data["playerSelectionPage"] -= 1
            elif event.keysym == "Return":
                # Check if player selection has been made and proceed to next pick
                if canvas.data["team1Picked"] == False and canvas.data["team1Roster"][canvas.data["positionPicking"]] != ("Empty",""):
                    #we also to remove the player for the next player
                    teamCreationGraphics.removeLastPlayerPicked(canvas)
                    canvas.data["team1Picked"] = True
                    canvas.data["playerSelectionPage"] = 0
                    canvas.data["CurrentPlayerSelected"] = None
                elif canvas.data["team1Picked"] == True and canvas.data["team2Roster"][canvas.data["positionPicking"]] != ("Empty",""):
                    # Set the table for the next position pick
                    canvas.data["team1Picked"] = False
                    canvas.data["playersAvailable"] = None
                    canvas.data["positionPicking"] += 1
                    canvas.data["playerSelectionPage"] = 0
                    canvas.data["CurrentPlayerSelected"] = None
                    if canvas.data["positionPicking"] == canvas.data["ammountOfPlayers"]:
                        canvas.data["teamSelectionProcess"] = False
                        canvas.data["fixLineupOrder"] = True
        elif canvas.data["fixLineupOrder"] == True:
            if canvas.data["currentPlayerForLineupFixing"] != None:
                #  Allows us to change the lineup order
                if event.keysym == "Down" and canvas.data["currentPlayerForLineupFixing"] < 8:
                    teamCreationGraphics.movePlayerOnRoster(canvas,"down")
                elif event.keysym == "Up" and canvas.data["currentPlayerForLineupFixing"] > 0:
                    teamCreationGraphics.movePlayerOnRoster(canvas,"up")
                if event.keysym == "Return":
                    if canvas.data["player1FixingLineup"] == True:
                        canvas.data["player1FixingLineup"] = False
                        canvas.data["currentPlayerForLineupFixing"] = None
                    else:
                        canvas.data["fixLineupOrder"] = False
                        canvas.data["exportTeams"] = True
                 
    if canvas.data["state"] == "game":
        if canvas.data["isGameOver"] == False:
            if canvas.data["duringGameHelpScreen"] == True:
                if event.keysym == "Return":
                    canvas.data["duringGameHelpScreen"] = False
            else:
                if event.keysym == "Return" and (canvas.data["changePitcher"] == True or canvas.data["changeBatter"] == True):
                    canvas.data["Player1Pause"] = False
                    canvas.data["Player2Pause"] = False
                    canvas.data["changePitcher"] = False
                    canvas.data["changeBatter"] = False
                elif event.char == "q" and canvas.data["Player2Pause"] == False and(canvas.data["changePitcher"] == False and canvas.data["changeBatter"] == False):
                    if canvas.data["Player1Pause"] == True:
                        canvas.data["Player1Pause"] = False
                    else:
                        canvas.data["Player1Pause"] = True
                elif event.char == "p" and canvas.data["Player1Pause"] == False and (canvas.data["changePitcher"] == False and canvas.data["changeBatter"] == False):
                    if canvas.data["Player2Pause"] == True:
                        canvas.data["Player2Pause"] = False
                    else:
                        canvas.data["Player2Pause"] = True
                elif event.keysym == "Right" and canvas.data["Player2Pause"] == False and canvas.data["Player1Pause"] == False:
                    GamePlay.runHalfInning(canvas)
                    if canvas.data["isGameOver"] == True:
                        canvas.data["state"] = "endGame"
                        createMainMenu(canvas)
    redrawAll(canvas)

def timerFired(canvas):
    redrawAll(canvas)
    delay = 250 # milliseconds
    canvas.after(delay, timerFired, canvas) # pause, then call timerFired again

def redrawAll(canvas):
    canvas.delete(ALL)
    if canvas.data["state"] == "mainMenu":
        mainMenu.drawBackground(canvas)
        mainMenu.drawBoxes(canvas)
        if canvas.data["displayHelpScreen"] == True:
            mainMenu.makeHelpScreen(canvas)

    elif canvas.data["state"] == "creation":
        teamCreationGraphics.drawBackground(canvas)
        if canvas.data["teamsNamesMade"] == False:
            teamCreationGraphics.teamNameCreation(canvas)
        elif canvas.data["teamSelectionProcess"]== True:
            teamCreationGraphics.pickTeam(canvas)
            teamCreationGraphics.currentPlayerSelected(canvas)
            teamCreationGraphics.displayRoster(canvas)
        elif canvas.data["fixLineupOrder"] == True:
            teamCreationGraphics.fixLineupOrder(canvas)
        elif canvas.data["exportTeams"] == True:
            # lets start the game
            teamCreationGraphics.exportTeams(canvas)
            if canvas.data["startRightAway"] == True:
                teamCreationGraphics.startGame(canvas)
                setUpTeams(canvas)
                canvas.data["exportTeams"] = False
                return
            canvas.data["exportTeams"] = False
            
    elif canvas.data["state"] == "game":
        gameGraphics.drawBackground(canvas)
        gameGraphics.drawScoreBoard(canvas)
        gameGraphics.drawField(canvas)
        gameGraphics.drawBattingScore(canvas)
        gameGraphics.drawLastPlay(canvas)
        gameGraphics.drawCurrentPitcher(canvas)
        gameGraphics.drawHitAndOutColors(canvas)
        gameGraphics.drawOuts(canvas)
        gameGraphics.drawSound(canvas)
        gameGraphics.drawHelpButton(canvas)
        if canvas.data["duringGameHelpScreen"] == True:
            gameGraphics.drawHelpMenu(canvas)
        if canvas.data["Player1Pause"] == True:
            if canvas.data["changePitcher"] == True:
                GamePlay.drawChangePitcher(canvas,1)
            elif canvas.data["changeBatter"] == True:
                GamePlay.drawChangeBatter(canvas,1)
            else:
                GamePlay.drawPlayerPause(canvas,1)
        if canvas.data["Player2Pause"] == True:
            if canvas.data["changePitcher"] == True:
                GamePlay.drawChangePitcher(canvas,2)
            elif canvas.data["changeBatter"] == True:
                GamePlay.drawChangeBatter(canvas,2)
            else:
                GamePlay.drawPlayerPause(canvas,2)
    elif canvas.data["state"] == "endGame":
        endGame.drawBackground(canvas)
        if canvas.data["displayFinalScoreBoard"] == True:
            gameGraphics.drawScoreBoard(canvas)
        endGame.drawBoxes(canvas)

def getColorInits(canvas):
    canvas.data["LeftFieldColor"] = "green"
    canvas.data["RightFieldColor"] = "green"
    canvas.data["CenterFieldColor"] = "green"
    canvas.data["InfieldColor"] = "darkgreen"
    canvas.data["firstBaseColor"] = "white"
    canvas.data["secondBaseColor"] = "white"
    canvas.data["thirdBaseColor"] = "white"

def createMainMenu(canvas):
    canvas.data["boxWidth"] = 430
    canvas.data["boxHeight"] = 70
    canvas.data["boxMargin"] = 60
    canvas.data["displayHelpScreen"] = False
    canvas.data["meanScoreReport"] = False
    canvas.data["image"] = PhotoImage(file="mainBackground.gif")

def setUpTeams(canvas):
    canvas.data["state"] = "game"
    #canvas.data["team1"] = "JBones.txt"
    #canvas.data["team2"] = "smonay.txt"
    #randomize away team
    canvas.data["awayTeam"] = random.randint(1,2)
    if canvas.data["awayTeam"] == 1:
        canvas.data["homeTeam"] = 2
    else:
        canvas.data["homeTeam"] = 1
    makeTeamInGame.getTeam(canvas,canvas.data["team1"], 1)
    makeTeamInGame.getTeam(canvas,canvas.data["team2"], 2)
    getColorInits(canvas)
    canvas.data["isSoundOn"] = True
    canvas.data["soundWidth"] = 140
    canvas.data["soundHeight"] = 40
    canvas.data["helpWidth"] = 140
    canvas.data["helpHeight"] = 40
    canvas.data["duringGameHelpScreen"] = False
    canvas.data['innings'] = 9
    canvas.data["outs"] = 0
    canvas.data["currentInning"] = 0
    canvas.data["Player1Runs"] = [None]*9
    canvas.data["Player2Runs"] = [None]*9
    canvas.data["Player1TotalRuns"] = 0
    canvas.data["Player2TotalRuns"] = 0
    canvas.data["Player1TotalHits"] = 0
    canvas.data["Player2TotalHits"] = 0
    canvas.data["Player1Pause"] = False #canvas.data["team1Name"]
    canvas.data["Player2Pause"] = False
    canvas.data["pauseHeight"] = (3* (canvas.data["height"])) / 4
    canvas.data["pauseWidth"] = (3* (canvas.data["width"])) / 4
    canvas.data["pauseTextHeight"] = 50
    canvas.data["optionHeight"] = 70
    canvas.data["optionWidth"] = 300
    canvas.data["optionMargin"] = 40
    canvas.data["bases"] = {}
    canvas.data["currentBases"] = {} #used only for Last Play feature
    canvas.data["initialScore"] = 0
    canvas.data["initialOuts"] = 0
    canvas.data["teamBatting"] = canvas.data["awayTeam"]
    canvas.data["Player1Batting"] = 0
    canvas.data["Player2Batting"] = 0
    canvas.data["teamPitching"] = canvas.data["homeTeam"]
    canvas.data["isGameOver"] = False
    canvas.data["lastPlay"] = "Game is about to start. Good luck!"
    canvas.data["allPlaysCombined"] = []
    canvas.data["exportTeams"] = False
    canvas.data["displayFinalScoreBoard"] = True
    canvas.data["changePitcher"] = False
    canvas.data["changeBatter"] = False
    canvas.data["linesOfLastPlay"] = 1

def teamCreation(canvas):
    canvas.data["positionsToPick"] = ["C","1B","2B","SS","3B","LF","CF","RF","DH",
                                      "BENCH","BENCH","BENCH","BENCH","SP","P","P",
                                      "P","P","P","P"]
    canvas.data["positionatoPickFullName"] = ["catcher","first baseman", "second baseman",
                                              "shortstop","third baseman", "left fielder",
                                              "center fielder","right fielder",
                                              "designated hitter", "first bench player",
                                              "second bench player", "third bench player", "fourth bench player",
                                              "starting pitcher", "first relief pitcher", "second relief pitcher",
                                              "third relief pitcher","fourth relief pitcher",
                                              "fifth relief pitcher","sixth relief pitcher"]
    canvas.data["benchPositions"] = ["1B", "2B", "3B", "C", "CF", "DH",
                                     "IF", "LF", "MI", "OF", "RF", "SS",
                                     "UT","CI"]
    canvas.data["pitcherPositions"] = ["CL","RP","P"]
    canvas.data["ammountOfPlayers"] = len(canvas.data["positionsToPick"])
    canvas.data["teamsNamesMade"] = False
    canvas.data["team1Name"] = ""
    canvas.data["team2Name"] = ""
    canvas.data["team1Made"] = False
    canvas.data["team1Picked"] = False
    canvas.data["positionPicking"] = 0
    canvas.data["playersAvailable"] = None
    # Page of the position players Available
    canvas.data["playerSelectionPage"] = 0
    canvas.data["playersPages"] = 0
    canvas.data["playersOnOnePage"] = 18
    canvas.data["teamSelectionProcess"] = False
    canvas.data["CurrentPlayerSelected"] = None
    # Fix lineup Order info
    canvas.data["fixLineupOrder"] = False
    canvas.data["player1FixingLineup"] = True
    canvas.data["currentPlayerForLineupFixing"] = None
    # Rosters
    canvas.data["team1Roster"] = [("Empty","")]* canvas.data["ammountOfPlayers"]
    canvas.data["team1PlayersString"] = [""]* canvas.data["ammountOfPlayers"]
    canvas.data["team2Roster"] = [("Empty","")]* canvas.data["ammountOfPlayers"]
    canvas.data["team2PlayersString"] = [""]* canvas.data["ammountOfPlayers"]
    canvas.data["exportTeams"] = False
    canvas.data["startRightAway"] = True
    canvas.data["heightOfEachRow"] = 26
    
def init(canvas):
    canvas.data["state"] = "mainMenu"
    if canvas.data["state"] == "mainMenu":
        createMainMenu(canvas)
    if canvas.data["state"] == "creation":
        teamCreation(canvas)
    if canvas.data["state"] == "game":
        setUpTeams(canvas)

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    root = Tk()
    width = 1000
    height = 700
    root.resizable(width=FALSE, height=FALSE)
    canvas = Canvas(root, width=width, height=height)
    canvas.pack(fill=BOTH,expand=YES)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    canvas.data["width"] = width
    canvas.data['height'] = height
    init(canvas)
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    root.bind("<Double-Button-1>", doubleMousePressed)
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the #window!)

run()
