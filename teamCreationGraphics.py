import random
import os

def drawBackground(canvas):
    width = canvas.data['width']
    height = canvas.data['height']
    canvas.create_rectangle(0,0,width,height,fill="cyan")

def teamNameCreation(canvas):
    # Prompt user for name of the user
    width = canvas.data["width"]
    height = canvas.data["height"]
    cx = width/2
    cy = height/2
    if canvas.data["team1Made"] == False:
        msg = "Player 1, please name your team. \n"
        msg += "Press [Return] to finalize the name."
        canvas.create_text(cx,cy, text=msg, font=("Helvetica", 25))
        canvas.create_text(cx,height-250, text="Player 1 team name: " + canvas.data["team1Name"],font=("Helvetica", 25))
    elif canvas.data["team1Made"] == True and canvas.data["teamsNamesMade"] == False:
        msg = "Player 2, please name your team. \n"
        msg += "Press [Return] to finalize the name."
        canvas.create_text(cx,cy, text=msg, font=("Helvetica", 25))
        canvas.create_text(cx,height-250, text="Player 2 team name: " + canvas.data["team2Name"],font=("Helvetica", 25))

def removePickedPlayersInBench(canvas):
    # remove players picked that were already on the bench. 
    playersToRemove  = []
    for (player,position) in canvas.data["team1Roster"]:
        if player != "Empty":
            playersToRemove.append((player,position))
    for (player,position) in canvas.data["team2Roster"]:
        if player != "Empty":
            playersToRemove.append((player,position))
    for (player,position) in playersToRemove:
        filepath = "Statistics/" +position + "/" +player +".txt"
        if (player,filepath,"gray80",position) in canvas.data["playersAvailable"]:
            canvas.data["playersAvailable"].remove((player,filepath,"gray80",position))
            

    
def scrapePlayers(canvas,position):
    # get the file location, position, and the playerName
    if position == "BENCH":
        canvas.data["playersAvailable"] = []
        for position in canvas.data["benchPositions"]:
            path = position
            for filename in os.listdir("Statistics/" +path):
                filepath = "Statistics/" +path + "/" +filename
                index = filename.find(".txt")
                playerName = filename[:index]
                canvas.data["playersAvailable"].append((playerName,filepath,"gray80",position))
        canvas.data["playersAvailable"].sort()
        removePickedPlayersInBench(canvas)
        canvas.data["playersPages" ] = (len(canvas.data["playersAvailable"])-1)/canvas.data["playersOnOnePage"]
    elif position == "P":
        canvas.data["playersAvailable"] = []
        for position in canvas.data["pitcherPositions"]:
            path = position
            for filename in os.listdir("Statistics/" +path):
                filepath = "Statistics/" +path + "/" +filename
                index = filename.find(".txt")
                playerName = filename[:index]
                canvas.data["playersAvailable"].append((playerName,filepath,"gray80",position))
        canvas.data["playersAvailable"].sort()
        removePickedPlayersInBench(canvas)
        canvas.data["playersPages" ] = (len(canvas.data["playersAvailable"])-1)/canvas.data["playersOnOnePage"]
    else:
        path = position
        canvas.data["playersAvailable"] = []
        for filename in os.listdir("Statistics/" +path):
            filepath = "Statistics/" +path + "/" +filename
            index = filename.find(".txt")
            playerName = filename[:index]
            canvas.data["playersAvailable"].append((playerName,filepath,"gray80",position))
        canvas.data["playersPages" ] = (len(canvas.data["playersAvailable"])-1)/canvas.data["playersOnOnePage"]

def getPlayersForPosition(canvas):
    #this gets the players for the position
    position = canvas.data["positionsToPick"][canvas.data["positionPicking"]]
    scrapePlayers(canvas,position)

def mousePressedPlayerSelection(canvas,eventx,eventy):
    width = canvas.data["width"]
    height = canvas.data["height"]
    top = 150
    bottom = top + canvas.data["heightOfEachRow"]*(canvas.data["playersOnOnePage"]+1)
    left = 2.0*width/4
    right = 2.75*width/4
    rows = canvas.data["playersOnOnePage"] + 1
    heightOfEachRow = canvas.data["heightOfEachRow"]
    if eventy >= top and eventy <= bottom and eventx>= left and eventx<= right:
        # get the player selected
        row = ((eventy)-top)/heightOfEachRow
        if row > 0:
            player = (canvas.data["playerSelectionPage"] * canvas.data["playersOnOnePage"])+row-1
            if player <= len(canvas.data["playersAvailable"])-1:
                # change the color of the previous selected player to original color
                currentPlayerSelected = canvas.data["CurrentPlayerSelected"]
                if currentPlayerSelected != None:
                    (playerName,link,color,position) = canvas.data["playersAvailable"][currentPlayerSelected]
                    color = "gray80"
                    canvas.data["playersAvailable"][currentPlayerSelected] = (playerName,link,color,position)
                # set the new selected player
                canvas.data["CurrentPlayerSelected"] = player
                # change the color of the player selected
                (playerName,link,color,position) = canvas.data["playersAvailable"][player]
                color = "red"
                canvas.data["playersAvailable"][player] = (playerName,link,color,position)

def getDataForRoster(playerName,link):
    fileHandler = open(link,"rt")
    data = fileHandler.read()
    fileHandler.close()
    #We need the data in one string
    return data
    

def doubleMousePressedPlayerSelect(canvas,eventx,eventy):
    width = canvas.data["width"]
    height = canvas.data["height"]
    top = 150
    bottom = top + canvas.data["heightOfEachRow"]*(canvas.data["playersOnOnePage"]+1)
    left = 2.0*width/4
    right = 2.75*width/4
    rows = canvas.data["playersOnOnePage"] + 1
    heightOfEachRow = canvas.data["heightOfEachRow"]
    if eventy >= top and eventy <= bottom and eventx>= left and eventx<= right:
        # get the player selected
        row = ((eventy)-top)/heightOfEachRow
        if row > 0:
            player = (canvas.data["playerSelectionPage"] * canvas.data["playersOnOnePage"])+row-1
            positionPicking = canvas.data["positionPicking"]
            if player <= len(canvas.data["playersAvailable"])-1:
                # put the player on the roster
                (playerName,link,color,position) = canvas.data["playersAvailable"][player]
                data = getDataForRoster(playerName,link)
                if canvas.data["team1Picked"] == False:
                    canvas.data["team1Roster"][positionPicking] = (playerName,position)
                    canvas.data["team1PlayersString"][positionPicking] = data
                    
                else:
                    canvas.data["team2Roster"][positionPicking] = (playerName,position)
                    canvas.data["team2PlayersString"][positionPicking] = data
      

def getPitcherString(data):
    string = ""
    string += "Player: " + data[1] + "(" +data[0] + ") \n"
    string += "Age: " + data[2] + "    W: " + data[3] + "\n"
    string += "L: " + data[4] + "    ERA: " + data[6] + "\n"
    string += "GP: " + data[7] + "    CG: " + data[10] + "\n"
    string += "S: " + data[12] + "    IP: " + data[13] + "\n" 
    string += "HA: " + data[14] + "    RA: " + data[15] + "\n"
    string += "HRA: " + data[17] + "    BB: " + data[18] + "\n"
    string += "SO: " + data[20] + "    HBP: " + data[21] + "\n"
    string += "WHIP: " + data[26] + "    S0/9I: " + data[30] + "\n" 
    return string

def getBatterString(data):
    string = ""
    string += "Player: " + data[1] + "(" +data[0] + ") \n"
    string += "Age: " + data[2] + "    Games Played: " + data[3] + "\n"
    string += "PA: " + data[4] + "    R: " + data[6] + "\n"
    string += "H: " + data[7] + "    2B: " + data[8] + "\n"
    string += "3B: " + data[9] + "    HR: " + data[10] + "\n" 
    string += "RBI: " + data[11] + "    BB: " + data[14] + "\n"
    string += "SO: " + data[15] + "    BA: " + data[16] + "\n"
    string += "OBP: " + data[17] + "    SLUG: " + data[18] + "\n"
    string += "GIDP: " + data[22] + "    HBP: " + data[23] + "\n" 
    return string

def convertDataIntoString(data):
    position = data[0]
    if position != "P" and position != "SP" and position != "RP" and position != "CL":
        string = getBatterString(data)
    else:
        string = getPitcherString(data)
    return string

def scrapeData(link):
    fileHandler = open(link,"rt")
    data = fileHandler.read()
    data = data.split("\n")
    fileHandler.close()
    #We need the data in one string
    return convertDataIntoString(data)

def getPlayerStats(canvas):
    currentPlayer = canvas.data["CurrentPlayerSelected"]
    (playerName,link,color,position) = canvas.data["playersAvailable"][currentPlayer]
    #Scrape the data of the player
    msg = scrapeData(link)
    return msg

def currentPlayerSelected(canvas):
    width = canvas.data["width"]
    height = canvas.data["height"]
    left = 2.85*width/4
    right = width-15
    top = 1.0*height/4
    heightOfEachRow = canvas.data["heightOfEachRow"]
    rows = 8
    bottom = top + (rows*heightOfEachRow)
    widthOfText = right-left
    cx = (left+right)/2
    cy = (top+bottom)/2
    bottom = top + rows*(heightOfEachRow)
    canvas.create_rectangle(left,top,right,bottom, fill="gray80", width = 2)
    if canvas.data["CurrentPlayerSelected"] == None:
        #  Initally no player is selected so make sure it is said
        msg = "No Player\n Selected"
        canvas.create_text(cx,cy, text=msg,font=("Helvetica", 32))
    else:
        # Lets get the stats so we can display them
        msg = getPlayerStats(canvas)
        canvas.create_text(cx,cy, text=msg,font=("Helvetica", 12))

def createPlayerSelectionRows(canvas,rows,left,right,top,bottom):
    heightOfEachRow = canvas.data["heightOfEachRow"]
    bottom = top+ heightOfEachRow
    leftForPosition = left - 30
    for row in range(rows):
        cx = (left+right)/2
        cxPosition = (leftForPosition+left)/2
        cy = (top + bottom)/2
        # get the players on the page
        # also get the position
        if row == 0:
            player = "Player Name"
            color = "gray80"
            position = "POS"
        else:
            playerToDisplay = (canvas.data["playerSelectionPage"]) * canvas.data["playersOnOnePage"]  + row-1
            if playerToDisplay <= len(canvas.data["playersAvailable"])-1:
                (player,link,color,position) = canvas.data["playersAvailable"][playerToDisplay]
            else:
                player = ""
                color = "gray80"
                position = ""
        # draw graphics
        canvas.create_rectangle(leftForPosition,top,left,bottom, fill=color, width = 2)
        canvas.create_rectangle(left,top,right,bottom, fill=color, width = 2)
        canvas.create_text(cx,cy, text=player, font=("Helvetica", 10))
        canvas.create_text(cxPosition,cy, text=position, font=("Helvetica", 10))
        top += heightOfEachRow
        bottom = top + heightOfEachRow   

def showPlayersToPick(canvas):
    # create player selection box
    width = canvas.data["width"]
    height = canvas.data["height"]
    top = 150
    bottom = height - 100
    left = 2.0*width/4
    right = 2.75*width/4
    rows = canvas.data["playersOnOnePage"] + 1
    createPlayerSelectionRows(canvas,rows,left,right,top,bottom)

def pickTeam(canvas):
    # get the players for the position
    if canvas.data["playersAvailable"] == None:
        getPlayersForPosition(canvas)
    else:
        width = canvas.data["width"]
        height = canvas.data["height"]
        cx = width/2
        cy = 70
        # get the position that we are picking
        position = canvas.data["positionatoPickFullName"][canvas.data["positionPicking"]]
        if canvas.data["team1Picked"]== False:
            msg = canvas.data["team1Name"] +", choose your " + position + ".\n"
        else:
            msg = canvas.data["team2Name"] +", choose your " + position + ".\n"
        msg += "Single click to view the player's stats from last season. \n"
        msg += "Double click to add the player to your roster. \n"
        msg += "Press [Return] to finalize your decision."
        canvas.create_text(cx,cy, text=msg, font=("Helvetica", 15))
        showPlayersToPick(canvas)

def createRosterLines(canvas,rows,left,right,top,bottom,roster):
    heightOfEachRow = canvas.data["heightOfEachRow"]
    bottom = top+ heightOfEachRow
    leftForPosition = left - 50
    for row in range(rows):
        cx = (left+right)/2
        cxPosition = (leftForPosition+left)/2
        cy = (top + bottom)/2
        # get the players on the roster
        color = "gray80"
        if row == 0:
            player = "Current Roster"
            position = "POS"
        else:
            position = canvas.data["positionsToPick"][row-1]
            (player,playerPosition) = roster[row-1]
        if row-1 == canvas.data["positionPicking"]:
            color = "orange"
        # draw graphics
        canvas.create_rectangle(leftForPosition,top,left,bottom, fill=color, width = 2)
        canvas.create_rectangle(left,top,right,bottom, fill=color, width = 2)
        canvas.create_text(cx,cy, text=player, font=("Helvetica", 10))
        canvas.create_text(cxPosition,cy, text=position, font=("Helvetica", 10))
        top += heightOfEachRow
        bottom = top + heightOfEachRow   

def displayRoster(canvas):
    if canvas.data["team1Picked"] == False:
        roster = canvas.data["team1Roster"]
    else:
        roster = canvas.data["team2Roster"]
    numberofPlayers = canvas.data["ammountOfPlayers"]
    rows = numberofPlayers + 1
    width = canvas.data["width"]
    height = canvas.data["height"]
    top = 150
    bottom = height - 100
    left = 1.0*width/4
    right = 1.75*width/4
    createRosterLines(canvas,rows,left,right,top,bottom,roster)

def saveTeam(data,teamName):
    fileHandler = open("Teams" + '/' + teamName+".txt","w")
    fileHandler.write(data)
    fileHandler.close()
    
def storeTeam(teamName, teamRoster,teamString):
    counter = 1
    data = ""
    for string in teamString:
        if counter == 10 or counter== 15:
            data += "###\n"
        elif counter == 14:
            data += "@@@\n"
        data += "#\n"
        data += string
        counter +=1
    saveTeam(data,teamName)
            
def exportTeams(canvas):
    team1Name = canvas.data["team1Name"]
    team2Name = canvas.data["team2Name"]
    team1Roster = canvas.data["team1Roster"]
    team2Roster = canvas.data["team2Roster"]
    team1String = canvas.data["team1PlayersString"]
    team2String = canvas.data["team2PlayersString"]
    storeTeam(team1Name,team1Roster,team1String)
    storeTeam(team2Name,team2Roster,team2String)

def startGame(canvas):
    canvas.data["team1"] = canvas.data["team1Name"] + ".txt"
    canvas.data["team2"] = canvas.data["team2Name"] + ".txt"

def removeLastPlayerPicked(canvas):
    canvas.data["playersAvailable"].pop(canvas.data["CurrentPlayerSelected"])
    canvas.data["playersPages" ] = (len(canvas.data["playersAvailable"])-1)/canvas.data["playersOnOnePage"]

def displayStartingRosterForLineupChange(canvas,rows,left,right,top,bottom,roster,heightOfEachRow):
    bottom = top+ heightOfEachRow
    leftForPosition = left - 35
    number = 0
    for row in range(rows):
        cx = (left+right)/2
        cxPosition = (leftForPosition+left)/2
        cy = (top + bottom)/2
        # get the players on the roster
        color = "gray80"
        if row == 0:
            player = "Current Lineup"
            position = "#"
        else:
            position = number
            (player,playerPosition) = roster[row-1]
        if row - 1 == canvas.data["currentPlayerForLineupFixing"]:
            color = "orange"
        # draw graphics
        canvas.create_rectangle(leftForPosition,top,left,bottom, fill=color, width = 2)
        canvas.create_rectangle(left,top,right,bottom, fill=color, width = 2)
        canvas.create_text(cx,cy, text=player, font=("Helvetica", 15))
        canvas.create_text(cxPosition,cy, text=position, font=("Helvetica", 15))
        top += heightOfEachRow
        bottom = top + heightOfEachRow
        number += 1
        
def fixLineupOrder(canvas):
    # Displays lineup order when we want to fix the line up
    width = canvas.data["width"]
    height = canvas.data["height"]
    cx = width/2
    cy = 125
    if canvas.data["player1FixingLineup"]== True:
        msg = canvas.data["team1Name"] + ", choose your batting order. \n"
    else:
        msg = canvas.data["team2Name"] + ", choose your batting order.\n"
    msg += "Click on a player and use the arrow keys\n"
    msg += "to change their place in the lineup.\n"
    msg += "Press [Return] to finalize your decisions."
    canvas.create_text(cx,cy, text=msg, font=("Helvetica", 20))
    # show the starting lineup
    if canvas.data["player1FixingLineup"] == True:
        roster = canvas.data["team1Roster"][:9]
    else:
        roster = canvas.data["team2Roster"][:9]
    numberofPlayers = 9
    rows = numberofPlayers + 1
    width = canvas.data["width"]
    height = canvas.data["height"]
    top = 250
    left = 1.50*width/4
    right = 2.50*width/4
    heightOfEachRow = canvas.data["heightOfEachRow"]+15
    bottom = top + (10*heightOfEachRow)
    displayStartingRosterForLineupChange(canvas,rows,left,right,top,bottom,roster,heightOfEachRow)
    
def fixLineupOrderPlayerSelection(canvas,eventx,eventy):
    width = canvas.data["width"]
    height = canvas.data["height"]
    top = 250
    left = 1.50*width/4
    right = 2.50*width/4
    rows = 10
    heightOfEachRow = canvas.data["heightOfEachRow"]+15
    bottom = top + (10*heightOfEachRow)
    if eventy >= top and eventy <= bottom and eventx>= left and eventx<= right:
        # get the player selected
        row = ((eventy)-top)/heightOfEachRow
        if row > 0:
            canvas.data["currentPlayerForLineupFixing"] = row - 1

def movePlayerOnRoster(canvas,direction):
    if direction == "down":
        # get the right indexes. 
        currentPlayerIndex = canvas.data["currentPlayerForLineupFixing"]
        otherPlayerIndex  = currentPlayerIndex + 1
        canvas.data["currentPlayerForLineupFixing"] += 1
    else:
        currentPlayerIndex = canvas.data["currentPlayerForLineupFixing"]
        otherPlayerIndex  = currentPlayerIndex - 1
        canvas.data["currentPlayerForLineupFixing"] -= 1
    if canvas.data["player1FixingLineup"] == True:
        roster = "team1Roster"
        rosterString = "team1PlayersString"
    else:
        roster = "team2Roster"
        rosterString = "team2PlayersString"
    (currentPlayerName,currentPosition) = canvas.data[roster][currentPlayerIndex]
    currentPlayerString = canvas.data[rosterString][currentPlayerIndex]
    (otherPlayerName,otherPosition) = canvas.data[roster][otherPlayerIndex]
    otherPlayerString = canvas.data[rosterString][otherPlayerIndex]
    canvas.data[roster][currentPlayerIndex] = (otherPlayerName,otherPosition)
    canvas.data[rosterString][currentPlayerIndex] = otherPlayerString
    canvas.data[roster][otherPlayerIndex] = (currentPlayerName,currentPosition)
    canvas.data[rosterString][otherPlayerIndex] = currentPlayerString
