import random
import makeTeamInGame
import copy
import winsound

def currentbatterName(canvas):
    currentbatterName = 0
    if canvas.data["teamBatting"] == canvas.data["awayTeam"]:
        currentbatterName = canvas.data["Player" + str(canvas.data["awayTeam"]) + "Batting"]
    else:
        currentbatterName = canvas.data["Player" + str(canvas.data["homeTeam"]) + "Batting"]
    return currentbatterName

def getAdjustedobp(obp,whip, battersFaced, pitcherPosition):
    #WRITE GENERALIZABLE FORMULA!!!
    # Z Score logic
    OBPStdDev = 0.049774891317
    OBPmean = 0.313796064401
    WHIPStdDev = 0.24552379969
    WHIPmean = 1.37148041237
    OBPZScore = (obp - OBPmean)/OBPStdDev
    WHIPZScore = (whip - WHIPmean)/WHIPStdDev
    #square the z-score and multiply by constant, keeping sign in tact to reward good players/ punish bad ones
    obp += (OBPZScore)*abs(OBPZScore)*(0.02) 
    obp += ((WHIPZScore)*abs(WHIPZScore)*(0.086))
    if pitcherPosition == "SP": #starting pitchers are better at handling more batters
        obp += float(battersFaced/50)*(.1)           #very simple algorithm: for every 50 batters faced, obp increases by .1
    else:
        obp += float(battersFaced/8)*(.1)            # for every 8 batters faced, obp increases by .1
    if obp > 0.85:
        obp = 0.85
    if obp < 0.02:
        obp = 0.02
    return obp

def addRunsToScore(number, pitcher, batterName, canvas):
    canvas.data[pitcher]['RA'] += 1
    canvas.data[batterName]['RBI'] += 1
    if canvas.data["teamBatting"] == canvas.data["awayTeam"]:
        canvas.data["Player" + str(canvas.data["awayTeam"]) + "TotalRuns"] += number
        canvas.data["Player" + str(canvas.data["awayTeam"]) + "Runs"][canvas.data["currentInning"]] += number
    else:
        canvas.data["Player" + str(canvas.data["homeTeam"]) + "TotalRuns"] += number
        canvas.data["Player" + str(canvas.data["homeTeam"]) + "Runs"][canvas.data["currentInning"]] += number

def pauseMenuAction(canvas, eventx, eventy):
    if canvas.data["Player1Pause"] == True:
        pass

def clickPlayerPause(canvas, eventx,eventy):
    width = canvas.data["width"]
    height = canvas.data["height"]
    pauseHeight = canvas.data["pauseHeight"]
    pauseWidth = canvas.data["pauseWidth"]
    topLeft = (width/2 - pauseWidth/2, height/2 - pauseHeight/2)
    botRight = (width/2 + pauseWidth/2, height/2 + pauseHeight/2)
    optionHeight = canvas.data["optionHeight"]
    optionWidth = canvas.data["optionWidth"]
    optionMargin = canvas.data["optionMargin"]
    left = (width/2 - optionWidth/2)
    right = (width/2 + optionWidth/2)
    if eventx >= left and eventx <=right and eventy >= height/2 and eventy <= height/2 + optionHeight:
        canvas.data["changePitcher"] = True
    elif eventx >= left and eventx <= right and eventy >= height/2+ optionHeight + optionMargin and eventy <= height/2+ 2*optionHeight + optionMargin:
        canvas.data["changeBatter"] = True

def drawPlayerPause(canvas, player):
    width = canvas.data["width"]
    height = canvas.data["height"]
    pauseHeight = canvas.data["pauseHeight"]
    pauseWidth = canvas.data["pauseWidth"]
    teamName = canvas.data["player" + str(player) + "TeamName"]
    textHeight = canvas.data["pauseTextHeight"]
    topLeft = (width/2 - pauseWidth/2, height/2 - pauseHeight/2)
    botRight = (width/2 + pauseWidth/2, height/2 + pauseHeight/2)
    canvas.create_rectangle(topLeft, botRight, fill = "orange")
    canvas.create_text(width/2, height/2 - pauseHeight/2 + textHeight/2 + 10, text = teamName + " Pause Menu", font = ("Helvetica", 23))
    optionHeight = canvas.data["optionHeight"]
    optionWidth = canvas.data["optionWidth"]
    optionMargin = canvas.data["optionMargin"]
    left = (width/2 - optionWidth/2)
    right = (width/2 + optionWidth/2)
    canvas.create_rectangle(left, height/2, right, height/2 + optionHeight, fill = "red")
    canvas.create_rectangle(left, height/2+ optionHeight + optionMargin, right, height/2+ 2*optionHeight + optionMargin, fill = "red")
    msg1 = "Switch Pitchers"
    canvas.create_text(width/2, height/2 + optionHeight/2, text = msg1, font = ("Helvetica", optionHeight/2 - 4))
    msg2 = "Pinch Hit"
    canvas.create_text(width/2, height/2+ (3*optionHeight)/2 + optionMargin, text = msg2, font = ("Helvetica", optionHeight/2 - 4))                  
#####
def drawCurrentPitcher(canvas,currentPitcher,width,height,pauseWidth,pauseHeight):
    left = width/2 + 0.25*pauseWidth/2
    right = width/2 + 4.0*pauseWidth/10
    top = height/2 - 0.5*pauseHeight/2
    bottom = height/2 - 0.35*pauseHeight/2
    canvas.create_rectangle(left,top,right,bottom, fill = "red")
    cy = (top + bottom) /2
    cx = (left + right) /2
    message = "Current Pitcher: " + currentPitcher[0]
    canvas.create_text(cx,cy, text = message, font = ("Helvetica", 10))
    
def drawAvailablePitchers(canvas,availablePitchers,width,height,pauseWidth,pauseHeight):
    right = width/2 - 0.25*pauseWidth/2
    left = width/2 - 4.0*pauseWidth/10
    top = height/2 - 0.5*pauseHeight/2
    bottom = height/2 - 0.35*pauseHeight/2
    heightOfEachRow = (bottom-top)
    for row in range(len(availablePitchers)+1):
        canvas.create_rectangle(left,top,right,bottom, fill = "red")
        cy = (top + bottom) /2
        cx = (left + right) /2
        if row == 0:
            if len(availablePitchers) == 0:
                message = "No More Available Pitchers"
            else:
                message = "Available Pitchers:"
        else:
            message = availablePitchers[row-1]
        canvas.create_text(cx,cy, text = message, font = ("Helvetica", 10))
        top = bottom
        bottom = top + heightOfEachRow

def changePitcherClick(canvas,eventx,eventy):
    width = canvas.data["width"]
    height = canvas.data["height"]
    pauseHeight = canvas.data["pauseHeight"]
    pauseWidth = canvas.data["pauseWidth"]
    right = width/2 - 0.25*pauseWidth/2
    left = width/2 - 4.0*pauseWidth/10
    top = height/2 - 0.5*pauseHeight/2
    bottom = height/2 - 0.35*pauseHeight/2
    heightOfEachRow = (bottom-top)
    if canvas.data["Player1Pause"] == True:
        player = 1
    else:
        player = 2
    bottom = top + heightOfEachRow*(len(canvas.data['pitchingBenchOfPlayer' + str(player)])+1)
    if eventy >= top and eventy <= bottom and eventx>= left and eventx<= right:
        # get the player selected
        row = int(((eventy)-top)/heightOfEachRow)
        if row > 0:
            pitcherToReplaceWith = canvas.data['pitchingBenchOfPlayer' + str(player)][row-1]
            changePitcher(canvas,player,pitcherToReplaceWith)

def changePitcher(canvas,player,pitcherToReplaceWith):
    currentPitcher = canvas.data['currentPitcherOfPlayer' + str(player)][0]
    canvas.data['currentPitcherOfPlayer' + str(player)][0] = pitcherToReplaceWith
    canvas.data['pitchingBenchOfPlayer' + str(player)].remove(pitcherToReplaceWith)
    canvas.data['usedPitchersOfPlayer' + str(player)].append(currentPitcher)
    canvas.data["Player1Pause"] = False
    canvas.data["Player2Pause"] = False
    canvas.data["changePitcher"] = False

def drawChangePitcher(canvas,player):
    width = canvas.data["width"]
    height = canvas.data["height"]
    pauseHeight = canvas.data["pauseHeight"]
    pauseWidth = canvas.data["pauseWidth"]
    teamName = canvas.data["player" + str(player) + "TeamName"]
    message = "Double Click the pitcher you want in the game. \n"
    message += "Press [return] if you do not want to do anything."
    textHeight = 20
    topLeft = (width/2 - pauseWidth/2, height/2 - pauseHeight/2)
    botRight = (width/2 + pauseWidth/2, height/2 + pauseHeight/2)
    canvas.create_rectangle(topLeft, botRight, fill = "orange")
    canvas.create_text(width/2, height/2 - pauseHeight/2 + textHeight/2 + 40, text = message, font = ("Helvetica", textHeight))
    currentPitcher = canvas.data['currentPitcherOfPlayer' + str(player)]
    availablePitchers = canvas.data['pitchingBenchOfPlayer' + str(player)]
    drawCurrentPitcher(canvas,currentPitcher,width,height,pauseWidth,pauseHeight)
    drawAvailablePitchers(canvas,availablePitchers,width,height,pauseWidth,pauseHeight)


#####

def drawCurrentBatter(canvas,currentBatter,width,height,pauseWidth,pauseHeight):
    left = width/2 + 0.25*pauseWidth/2
    right = width/2 + 4.0*pauseWidth/10
    top = height/2 - 0.5*pauseHeight/2
    bottom = height/2 - 0.35*pauseHeight/2
    canvas.create_rectangle(left,top,right,bottom, fill = "red")
    cy = (top + bottom) /2
    cx = (left + right) /2
    message = "Current Batter: " + currentBatter
    canvas.create_text(cx,cy, text = message, font = ("Helvetica", 10))
    
def drawAvailableBatters(canvas,availableBatters,width,height,pauseWidth,pauseHeight):
    right = width/2 - 0.25*pauseWidth/2
    left = width/2 - 4.0*pauseWidth/10
    top = height/2 - 0.5*pauseHeight/2
    bottom = height/2 - 0.35*pauseHeight/2
    heightOfEachRow = (bottom-top)
    for row in range(len(availableBatters)+1):
        canvas.create_rectangle(left,top,right,bottom, fill = "red")
        cy = (top + bottom) /2
        cx = (left + right) /2
        if row == 0:
            if len(availableBatters) == 0:
                message = "No More Available Batters"
            else:
                message = "Available Batters:"
        else:
            message = availableBatters[row-1]
        canvas.create_text(cx,cy, text = message, font = ("Helvetica", 10))
        top = bottom
        bottom = top + heightOfEachRow
        
def changeBatterClick(canvas,eventx,eventy):
    width = canvas.data["width"]
    height = canvas.data["height"]
    pauseHeight = canvas.data["pauseHeight"]
    pauseWidth = canvas.data["pauseWidth"]
    right = width/2 - 0.25*pauseWidth/2
    left = width/2 - 4.0*pauseWidth/10
    top = height/2 - 0.5*pauseHeight/2
    bottom = height/2 - 0.35*pauseHeight/2
    heightOfEachRow = (bottom-top)
    if canvas.data["Player1Pause"] == True:
        player = 1
    else:
        player = 2
    bottom = top + heightOfEachRow*(len(canvas.data['battingBenchOfPlayer' + str(player)])+1)
    if eventy >= top and eventy <= bottom and eventx>= left and eventx<= right:
        # get the player selected
        row = int(((eventy)-top)/heightOfEachRow)
        if row > 0:
            batterToReplaceWith = canvas.data['battingBenchOfPlayer' + str(player)][row-1]
            changeBatter(canvas,player,batterToReplaceWith)

def changeBatter(canvas,player,batterToReplaceWith):
    currentBatter = canvas.data['startingLineOfPlayer' + str(player)][canvas.data["Player"+str(player)+"Batting"]]
    canvas.data['startingLineOfPlayer' + str(player)][canvas.data["Player"+str(player)+"Batting"]] = batterToReplaceWith
    canvas.data['battingBenchOfPlayer' + str(player)].remove(batterToReplaceWith)
    canvas.data['usedBattersOfPlayer' + str(player)].append(currentBatter)
    canvas.data["Player1Pause"] = False
    canvas.data["Player2Pause"] = False
    canvas.data["changeBatter"] = False

def drawChangeBatter(canvas,player):
    width = canvas.data["width"]
    height = canvas.data["height"]
    pauseHeight = canvas.data["pauseHeight"]
    pauseWidth = canvas.data["pauseWidth"]
    teamName = canvas.data["player" + str(player) + "TeamName"]
    message = "Double Click the batter you want in the game. \n"
    message += "Press [return] if you do not want to do anything."
    textHeight = 20
    topLeft = (width/2 - pauseWidth/2, height/2 - pauseHeight/2)
    botRight = (width/2 + pauseWidth/2, height/2 + pauseHeight/2)
    canvas.create_rectangle(topLeft, botRight, fill = "orange")
    canvas.create_text(width/2, height/2 - pauseHeight/2 + textHeight/2 + 40, text = message, font = ("Helvetica", textHeight))
    currentBatters = canvas.data['startingLineOfPlayer' + str(player)]
    availableBatters = canvas.data['battingBenchOfPlayer' + str(player)]
    currentBatter = currentBatters[canvas.data["Player"+str(player)+"Batting"]]
    drawCurrentBatter(canvas,currentBatter,width,height,pauseWidth,pauseHeight)
    drawAvailableBatters(canvas,availableBatters,width,height,pauseWidth,pauseHeight)


###
def addHitsToScore(canvas):
    if canvas.data["teamBatting"] == canvas.data["awayTeam"]:
        canvas.data["Player" + str(canvas.data["awayTeam"]) + "TotalHits"] += 1
    else:
        canvas.data["Player" + str(canvas.data["homeTeam"]) + "TotalHits"] += 1
    
def checkForPlayer(firstBase, secondBase, thirdBase, canvas):

    bases = canvas.data["bases"]
    check = [firstBase,secondBase,thirdBase]
    currentBases = [False,False,False]
    basesWithPlayers = sorted(bases.values())
    for element in basesWithPlayers:
        currentBases[element-1] = True
    if currentBases == check:
        return True
    else:
        return False

    """
    
    basesToCheck = []
    falseBasesToCheck = []
    if firstBase:
        basesToCheck.append(1)
    else:
        falseBasesToCheck.append(1)
    if secondBase:
        basesToCheck.append(2)
    else:
        falseBasesToCheck.append(2)
    if thirdBase:
        basesToCheck.append(3)
    else:
        falseBasesToCheck.append(3)
    for baseToCheck in basesToCheck:
        if baseToCheck not in basesWithPlayers:
            return False
    for baseToCheck in falseBasesToCheck:
        pass
    return True
    """
        
def manualAdvance (initialBase, basesToMove, deleteRunner, canvas):
    bases = canvas.data["bases"]
    basePlayer = dict(zip(bases.values(), bases.keys())) #stackoverflow.com, tersely reverses keys/ values for dict
    playerToRemember = basePlayer[initialBase]
    battingTeam = canvas.data["teamBatting"]
    teambatterNames = canvas.data['startingLineOfPlayer' + str(battingTeam)]
    batterName = teambatterNames[currentbatterName(canvas)]
    pitchingTeam = canvas.data["teamPitching"]
    pitcher = canvas.data['currentPitcherOfPlayer' + str(pitchingTeam)][0]
    if bases[playerToRemember] + basesToMove > 3:
        addRunsToScore(1, pitcher, batterName, canvas)
        canvas.data[playerToRemember]['R']+= 1
        del bases[playerToRemember]
    else:
        bases[playerToRemember] += basesToMove
    if deleteRunner == True:
        del bases[playerToRemember]
    canvas.data["bases"] = bases

def advanceRunners(numOfBases, batterName, canvas):
    bases = canvas.data["bases"]
    outs = canvas.data["outs"]
    # get the current pitcher
    pitchingTeam = canvas.data["teamPitching"]
    pitcher = canvas.data['currentPitcherOfPlayer' + str(pitchingTeam)][0]
    deleteList = []
    bases[batterName] = 0 # if player gets on base, add them to dict to add base values later
    for key in bases:
        if bases[key] + numOfBases > 3:
            addRunsToScore(1,pitcher, batterName, canvas)
            canvas.data[key]['R']+= 1
            deleteList.append(key) #can't delete key while iterating over dict, so do it after
        else:
            bases[key] += numOfBases
    for key in deleteList:
        del bases[key]
    canvas.data["bases"] = bases
            
def forceMove(batterName, canvas):
    bases = canvas.data["bases"]
    if checkForPlayer(True,False,False,canvas) or checkForPlayer(True,True,False,canvas) or checkForPlayer(True,True,True,canvas):
        advanceRunners(1,batterName,canvas)
    if checkForPlayer(True,False,True,canvas):
        manualAdvance(1, 1, False, canvas)
        bases[batterName] = 1
    else:
        bases[batterName] = 1
    canvas.data["bases"] = bases

def changeFieldColor(location, out, canvas):
    color = ""
    if out:
        color = "red"
    else:
        color = "blue"
    canvas.data[location + "Color"] = color

def getBaseColors(canvas):
    canvas.data["firstBaseColor"] = "white"
    canvas.data["secondBaseColor"] = "white"
    canvas.data["thirdBaseColor"] = "white"
    bases = canvas.data["bases"]
    for key in bases:
        if bases[key] == 1:
            canvas.data["firstBaseColor"] = "black"
        elif bases[key] == 2:
            canvas.data["secondBaseColor"] = "black"
        elif bases[key] == 3:
            canvas.data["thirdBaseColor"] = "black"
                
def getLocation(singleOrOut):
    if singleOrOut:
        possibleLocations = ["LeftField", "RightField", "CenterField", "Infield"]
    else: #doubles and triples always leave the infield
        possibleLocations = ["LeftField", "RightField", "CenterField"]
    index = random.randint(0,len(possibleLocations)-1)
    location = possibleLocations[index]
    return location

def isBattingOver(canvas):
    if canvas.data["outs"] == 3:
        terminateBatting(canvas)
        return True
    else:
        return False

def samePlayers(bases, currentBases):
    if len(bases) >= len(currentBases):
        for key in bases:
            if key not in currentBases:
                return False
        return True
    else:
        for key in currentBases:
            if key not in bases:
                return False
        return True

def getBaseName(baseNumber):
    if baseNumber == 1:
        return "first base"
    elif baseNumber == 2:
        return "second base"
    else:
        return "third base"

def getHitName(baseNumber):
    if baseNumber == 2:
        return "double"
    elif baseNumber == 3:
        return "triple"

def getOutfieldName(location):
    if location == "RightField":
        return "right field"
    elif location == "LeftField":
        return "left field"
    else:
        return "center field"

def soundChanger(canvas,eventx,eventy):
    soundWidth = canvas.data["soundWidth"]
    soundHeight = canvas.data["soundHeight"]
    width = canvas.data["width"]
    height = canvas.data["height"]
    soundOn = canvas.data["isSoundOn"]
    soundLeft = width - soundWidth
    soundBot = soundHeight
    if eventx <= width and eventx >= width - soundWidth and eventy >= 0 and eventy <= soundHeight:
        soundOn = not soundOn
    canvas.data["isSoundOn"] = soundOn

def playSound(canvas, hitName):
    # always asynchronous
    if canvas.data["isSoundOn"] == True:
        flags = winsound.SND_FILENAME | winsound.SND_ASYNC
        winsound.PlaySound(hitName, flags)
    
def updateLastPlay(canvas, location, isHomeRun = False, isStrikeout = False, oneBase = None):
    bases = canvas.data["bases"]
    currentBases = canvas.data["currentBases"]
    initialScore = canvas.data["initialScore"]
    finalScore = int(canvas.data["Player1TotalRuns"]) + int(canvas.data["Player2TotalRuns"])
    initialOuts = canvas.data["initialOuts"]
    outs = canvas.data["outs"]
    lastPlay = ""
    initialStateDict = dict(zip(currentBases.values(), currentBases.keys())) #stackoverflow.com, tersely reverses keys/ values for dict
    initialState = sorted(initialStateDict.keys())
    finalStateDict = dict(zip(bases.values(), bases.keys())) #stackoverflow.com, tersely reverses keys/ values for dict
    finalState = sorted(finalStateDict.keys())
    battingTeam = canvas.data["teamBatting"] #get batter name 1/3
    teambatterNames = canvas.data['startingLineOfPlayer' + str(battingTeam)] # get batter name 2/3
    batterName = teambatterNames[currentbatterName(canvas)] #get batter name 3/3
    if initialState == finalState:
        if isHomeRun == False and isStrikeout == False:
            if location == "Infield" and outs - 2 != initialOuts and outs - 1 == initialOuts:
                lastPlay += batterName + " grounded out to the infield.\n"
                playSound(canvas, "Commentary_Audio/Groundout.wav")
            elif location != "Infield" and outs - 2 != initialOuts and outs - 1 == initialOuts:
                lastPlay += batterName + " popped out to " + getOutfieldName(location) + ".\n"
                if location == "LeftField":
                    randomLF = random.randint(1,2)
                    if randomLF == 1:
                        playSound(canvas, "Commentary_Audio/PopLF.wav")
                    else:
                        playSound(canvas, "Commentary_Audio/PopLF2.wav")
                elif location == "RightField":
                    randomRF = random.randint(1,2)
                    if randomRF == 1:
                        playSound(canvas, "Commentary_Audio/PopRF.wav")
                    else:
                        playSound(canvas, "Commentary_Audio/PopRF2.wav")
                else:
                    randomCF = random.randint(1,2)
                    if randomCF == 1:
                        playSound(canvas, "Commentary_Audio/PopCF.wav")
                    else:
                        playSound(canvas, "Commentary_Audio/PopCF2.wav")
                    
        elif isHomeRun == False and isStrikeout == True:
            lastPlay += batterName + " struck out.\n"
            randomK = random.randint(1,3)
            if randomK == 1:
                playSound(canvas, "Commentary_Audio/K1.wav")
            elif randomK == 2:
                playSound(canvas, "Commentary_Audio/K2.wav")
            else:
                playSound(canvas, "Commentary_Audio/K3.wav")
        if initialOuts == outs and isHomeRun == True:
            lastPlay += batterName + " hit a solo homerun.\n"
            playSound(canvas, "Commentary_Audio/1HR.wav")
        if outs - 2 == initialOuts: #the way it's coded, the players don't move on bases if there are 3 outs after dp
            lastPlay += batterName + " grounded into a double play.\n"
            playSound(canvas, "Commentary_Audio/DoubPlay.wav")
        if initialScore != finalScore:
            if len(bases) == 0 and isHomeRun == True:
                if len(currentBases) == 3:
                    lastPlay += batterName + " hit a GRAND SLAM!\n"
                    playSound(canvas, "Commentary_Audio/4HR.wav")
                else:
                    if len(currentBases) != 0:
                        lastPlay += batterName + " hit a " + str(len(currentBases) + 1) + "- man homerun!\n"
                        if len(currentBases) == 1:
                            playSound(canvas, "Commentary_Audio/2HR.wav")
                        elif len(currentBases) == 2:
                            playSound(canvas, "Commentary_Audio/3HR.wav")
                        
            for key in currentBases: #CODE FOR DOUBLE PLAY WITH SCORE
                isSacFly = False
                if currentBases[key] == 3 and batterName not in bases and isHomeRun == False:
                    lastPlay += key + " scored on a sacrifice fly hit by " + batterName + ".\n"
                    isSacFly = True
                    playSound(canvas, "Commentary_Audio/Sacfly.wav")
                if key not in bases and isSacFly == False:
                    lastPlay += key + " scored.\n"
                if (outs - 2) == initialOuts and key not in bases:
                    lastPlay += batterName + " grounded into a double play. " + key + " was thrown out at second. \n"
                if key in bases and bases[key] != currentBases[key]:
                    lastPlay += key + " advanced from " + getBaseName(currentBases[key]) + " to " + getBaseName(bases[key]) + ".\n"
            for key in bases: #player at bat reached base
                if key not in currentBases:
                    if bases[key] == 1:
                        if oneBase == "walk":
                            lastPlay += key + " walked.\n"
                            if random.randint(1,2) == 1:
                                playSound(canvas, "Commentary_Audio/Walk1.wav")
                            else:
                                playSound(canvas, "Commentary_Audio/Walk2.wav")
                        elif oneBase == "hitBy":
                            lastPlay += key + " was hit by a pitch.\n"
                            playSound(canvas, "Commentary_Audio/Hitby.wav")
                        elif oneBase == "single":
                            if location == "Infield":
                                lastPlay += key + " hit an infield single.\n"
                                playSound(canvas, "Commentary_Audio/SingleIF.wav")
                            else:
                                lastPlay += key + " hit a single to " + getOutfieldName(location) + ".\n"
                                if location == "LeftField":
                                    playSound(canvas, "Commentary_Audio/SingleLF.wav")
                                elif location == "CenterField":
                                    playSound(canvas, "Commentary_Audio/SingleCF.wav")
                                else:
                                    playSound(canvas, "Commentary_Audio/SingleRF.wav")
                    else:
                        lastPlay += key + " hit a " + getHitName(bases[key]) + " to " + getOutfieldName(location) + ".\n"
                        if location == "LeftField":
                            if bases[key] == 2:
                                playSound(canvas, "Commentary_Audio/DoubleLF.wav")
                            elif bases[key] == 3:
                                playSound(canvas, "Commentary_Audio/TripleLF.wav")
                        elif location == "RightField":
                            if bases[key] == 2:
                                playSound(canvas, "Commentary_Audio/DoubleRF.wav")
                            elif bases[key] == 3:
                                playSound(canvas, "Commentary_Audio/TripleRF.wav")
                        elif location == "CenterField":
                            if bases[key] == 2:
                                playSound(canvas, "Commentary_Audio/DoubleCF.wav")
                            elif bases[key] == 3:
                                playSound(canvas, "Commentary_Audio/TripleCF.wav")
    else: #something changed on the bases
        if isHomeRun == False and isStrikeout == False and len(currentBases) != 0 and len(bases) == 0:
            if location != "Infield" and outs - 2 != initialOuts and outs - 1 == initialOuts:
                lastPlay += batterName + " popped out to " + getOutfieldName(location) + ".\n"
                if location == "LeftField":
                    randomLF = random.randint(1,2)
                    if randomLF == 1:
                        playSound(canvas, "Commentary_Audio/PopLF.wav")
                    else:
                        playSound(canvas, "Commentary_Audio/PopLF2.wav")
                elif location == "RightField":
                    randomRF = random.randint(1,2)
                    if randomRF == 1:
                        playSound(canvas, "Commentary_Audio/PopRF.wav")
                    else:
                        playSound(canvas, "Commentary_Audio/PopRF2.wav")
                else:
                    randomCF = random.randint(1,2)
                    if randomCF == 1:
                        playSound(canvas, "Commentary_Audio/PopCF.wav")
                    else:
                        playSound(canvas, "Commentary_Audio/PopCF2.wav")
            elif location == "Infield" and outs - 2 != initialOuts and outs - 1 == initialOuts:
                lastPlay += batterName + " grounded out to the infield.\n"
                playSound(canvas, "Commentary_Audio/Groundout.wav")

        elif isHomeRun == False and isStrikeout == True:
            lastPlay += batterName + " struck out.\n"
            randomK = random.randint(1,3)
            if randomK == 1:
                playSound(canvas, "Commentary_Audio/K1.wav")
            elif randomK == 2:
                playSound(canvas, "Commentary_Audio/K1.wav")
            else:
                playSound(canvas, "Commentary_Audio/K1.wav")
        if samePlayers(bases, currentBases): #same players on bases, they just advanced
            for key in currentBases:
                if currentBases[key] != bases[key]:
                    lastPlay += key + " advanced from " + getBaseName(currentBases[key]) + " to " + getBaseName(bases[key]) + ".\n"
                    if location == "Infield" and initialOuts != outs:
                        lastPlay += batterName + " grounded out to the infield.\n"
                        playSound(canvas, "Commentary_Audio/Groundout.wav")
                    elif location != "Infield" and initialOuts != outs and outs - 2 != initialOuts and outs - 1 == initialOuts:
                        lastPlay += batterName + " popped out to " + getOutfieldName(location) + ".\n"
                if location == "LeftField":
                    randomLF = random.randint(1,2)
                    if randomLF == 1:
                        playSound(canvas, "Commentary_Audio/PopLF.wav")
                    else:
                        playSound(canvas, "Commentary_Audio/PopLF2.wav")
                elif location == "RightField":
                    randomRF = random.randint(1,2)
                    if randomRF == 1:
                        playSound(canvas, "Commentary_Audio/PopRF.wav")
                    else:
                        playSound(canvas, "Commentary_Audio/PopRF2.wav")
                else:
                    randomCF = random.randint(1,2)
                    if randomCF == 1:
                        playSound(canvas, "Commentary_Audio/PopCF.wav")
                    else:
                        playSound(canvas, "Commentary_Audio/PopCF2.wav")
        else: #people on base changed because of play
            if initialScore == finalScore:
                outWritten = False
                for key in currentBases:
                    if key in bases and bases[key] != currentBases[key]:
                        lastPlay += key + " advanced from " + getBaseName(currentBases[key]) + " to " + getBaseName(bases[key]) + ".\n"
                    if key not in bases:
                        if outs ==2 and outWritten == False and (outs-2) != initialOuts:
                            lastPlay += batterName + " grounded out to the infield.\n"
                            outWritten = True
                            playSound(canvas, "Commentary_Audio/Groundout.wav")
                    if (outs - 2) == initialOuts and key not in bases:
                        lastPlay += batterName + " grounded into a double play. " + key + " was thrown out at second.\n"
                        playSound(canvas, "Commentary_Audio/DoubPlay.wav")
                for key in bases: #player at bat reached base
                    if key not in currentBases:
                        if bases[key] == 1:
                            if oneBase == "walk":
                                lastPlay += key + " walked.\n"
                                randomBB = random.randint(1,2)
                                if randomBB == 1:
                                    playSound(canvas, "Commentary_Audio/Walk1.wav")
                                else:
                                    playSound(canvas, "Commentary_Audio/Walk2.wav")
                            elif oneBase == "hitBy":
                                lastPlay += key + " was hit by a pitch.\n"
                                playSound(canvas, "Commentary_Audio/Hitby.wav")
                            elif oneBase == "single":
                                if location == "Infield":
                                    lastPlay += key + " hit an infield single.\n"
                                    playSound(canvas, "Commentary_Audio/SingleIF.wav")
                                else:
                                    lastPlay += key + " hit a single to " + getOutfieldName(location) + ".\n"
                                    if location == "LeftField":
                                        playSound(canvas, "Commentary_Audio/SingleLF.wav")
                                    elif location == "CenterField":
                                        playSound(canvas, "Commentary_Audio/SingleCF.wav")
                                    else:
                                        playSound(canvas, "Commentary_Audio/SingleRF.wav")
                        else:
                            lastPlay += key + " hit a " + getHitName(bases[key]) + " to " + getOutfieldName(location) + ".\n"
                            if location == "LeftField":
                                if bases[key] == 2:
                                    playSound(canvas, "Commentary_Audio/DoubleLF.wav")
                                elif bases[key] == 3:
                                    playSound(canvas, "Commentary_Audio/TripleLF.wav")
                            elif location == "RightField":
                                if bases[key] == 2:
                                    playSound(canvas, "Commentary_Audio/DoubleRF.wav")
                                elif bases[key] == 3:
                                    playSound(canvas, "Commentary_Audio/TripleRF.wav")
                            elif location == "CenterField":
                                if bases[key] == 2:
                                    playSound(canvas, "Commentary_Audio/DoubleCF.wav")
                                elif bases[key] == 3:
                                    playSound(canvas, "Commentary_Audio/TripleCF.wav")
                            
            else:
                if len(bases) == 0 and isHomeRun == True:
                    if len(currentBases) == 3:
                        lastPlay += batterName + " hit a GRAND SLAM!\n"
                        playSound(canvas, "Commentary_Audio/4HR.wav")
                    else:
                        lastPlay += batterName + " hit a " + str(len(currentBases) + 1) + "- man homerun!\n"
                        if len(currentBases) == 0:
                            playSound(canvas, "Commentary_Audio/1HR.wav")
                        elif len(currentBases) == 1:
                            playSound(canvas, "Commentary_Audio/2HR.wav")
                        elif len(currentBases) == 2:
                            playSound(canvas, "Commentary_Audio/3HR.wav")
                            
                for key in currentBases: #CODE FOR DOUBLE PLAY WITH SCORE
                    isSacFly = False
                    if currentBases[key] == 3 and batterName not in bases and isHomeRun == False:
                        lastPlay += key + " scored on a sacrifice fly hit by " + batterName + ".\n"
                        isSacFly = True
                        playSound(canvas, "Commentary_Audio/Sacfly.wav")
                    if key not in bases and isSacFly == False:
                        lastPlay += key + " scored.\n"
                    if (outs - 2) == initialOuts and key not in bases and currentBases[key] == 1:
                        lastPlay += batterName + " grounded into a double play. " + key + " was thrown out at second. \n"
                        playSound(canvas, "Commentary_Audio/DoubPlay.wav")
                    if (outs - 2) == initialOuts and key not in bases and currentBases[key] == 3:
                        lastPlay += key + " scored. \n"
                    if key in bases and bases[key] != currentBases[key]:
                        lastPlay += key + " advanced from " + getBaseName(currentBases[key]) + " to " + getBaseName(bases[key]) + ".\n"
                for key in bases: #player at bat reached base
                    if key not in currentBases:
                        if bases[key] == 1:
                            if oneBase == "walk":
                                lastPlay += key + " walked.\n"
                                if random.randint(1,2) == 1:
                                    playSound(canvas, "Commentary_Audio/Walk1.wav")
                                else:
                                    playSound(canvas, "Commentary_Audio/Walk2.wav")
                            elif oneBase == "hitBy":
                                lastPlay += key + " was hit by a pitch.\n"
                                playSound(canvas, "Commentary_Audio/Hitby.wav")
                            elif oneBase == "single":
                                if location == "Infield":
                                    lastPlay += key + " hit an infield single.\n"
                                    playSound(canvas, "Commentary_Audio/SingleIF.wav")
                                else:
                                    lastPlay += key + " hit a single to " + getOutfieldName(location) + ".\n"
                                    if location == "LeftField":
                                        playSound(canvas, "Commentary_Audio/SingleLF.wav")
                                    elif location == "CenterField":
                                        playSound(canvas, "Commentary_Audio/SingleCF.wav")
                                    else:
                                        playSound(canvas, "Commentary_Audio/SingleRF.wav")
                        else:
                            lastPlay += key + " hit a " + getHitName(bases[key]) + " to " + getOutfieldName(location) + ".\n"
                            if location == "LeftField":
                                if bases[key] == 2:
                                    playSound(canvas, "Commentary_Audio/DoubleLF.wav")
                                elif bases[key] == 3:
                                    playSound(canvas, "Commentary_Audio/TripleLF.wav")
                            elif location == "RightField":
                                if bases[key] == 2:
                                    playSound(canvas, "Commentary_Audio/DoubleRF.wav")
                                elif bases[key] == 3:
                                    playSound(canvas, "Commentary_Audio/TripleRF.wav")
                            elif location == "CenterField":
                                if bases[key] == 2:
                                    playSound(canvas, "Commentary_Audio/DoubleCF.wav")
                                elif bases[key] == 3:
                                    playSound(canvas, "Commentary_Audio/TripleCF.wav")
    canvas.data["linesOfLastPlay"] = lastPlay.count("\n")
    if len(lastPlay) == 0:
        canvas.data["linesOfLastPlay"] = 1
    else:
        lastPlay = lastPlay[:len(lastPlay)-1]
    canvas.data["lastPlay"] = lastPlay
    canvas.data["allPlaysCombined"].append(lastPlay + "/n")

def runAtBat(single, bb, hitBy, SP9I, obp, range1,range2,range3,canvas,batterName,pitcher):
    canvas.data[batterName]['PA']+= 1
    canvas.data[batterName]['AB']+= 1
    canvas.data[pitcher]['battersFaced'] += 1
    bases = canvas.data["bases"]
    basesH = copy.deepcopy(canvas.data["bases"]) #need a deecopy to keep current state
    canvas.data["currentBases"] = basesH
    outsH = copy.deepcopy(canvas.data["outs"])
    canvas.data["initialOuts"] = outsH
    #canvas.data["currentBases"] = bases
    helperCopy = copy.deepcopy(canvas.data["Player1TotalRuns"])
    helper2Copy = copy.deepcopy(canvas.data["Player2TotalRuns"])
    canvas.data["initialScore"] = int(helperCopy) + int(helper2Copy)
    canvas.data["lastPlay"] = ""
    if random.random()<= obp:
        total = random.random()*obp
        if total <=range1: #single, walk, or hit by pitch, MAKE MORE COMPLICATED
            sbbhb = float(single + bb + hitBy) #sbbhb = single bb hitby
            rangeSin = single/ sbbhb
            rangeBB = (bb / sbbhb) + rangeSin
            rangeHitBy = (hitBy / sbbhb) + rangeBB
            hitChance = random.random()
            if  hitChance <= rangeSin: #single
                canvas.data[batterName]['H'] += 1
                hitLocation = getLocation(True)
                changeFieldColor(hitLocation, False, canvas)
                addHitsToScore(canvas)
                advanceRunners(1,batterName,canvas)
                updateLastPlay(canvas, hitLocation, isHomeRun = False, isStrikeout = False, oneBase = "single")
            elif  hitChance > rangeSin and hitChance <= rangeBB: #walk
                #canvas.data["currentBases"] = canvas.data["bases"]
                canvas.data[batterName]['AB']-= 1
                canvas.data[batterName]['BB'] += 1
                canvas.data[pitcher]['BB'] += 1
                forceMove(batterName,canvas)
                updateLastPlay(canvas, None, isHomeRun = False, isStrikeout = False, oneBase = "walk")
            else: #hit by pitch
                #canvas.data["currentBases"] = canvas.data["bases"]
                canvas.data[batterName]['AB']-= 1
                canvas.data[batterName]['HBP'] += 1
                canvas.data[pitcher]['HBP'] += 1
                forceMove(batterName,canvas)
                updateLastPlay(canvas, None, isHomeRun = False, isStrikeout = False, oneBase = "hitBy")
        elif total >range1 and total <=range2: #double
            #canvas.data["currentBases"] = canvas.data["bases"]
            canvas.data[batterName]['H'] += 1
            hitLocation = getLocation(False)
            changeFieldColor(hitLocation, False, canvas)
            addHitsToScore(canvas)
            advanceRunners(2,batterName,canvas)
            updateLastPlay(canvas, hitLocation)
        elif total > range2 and total<= range3: #triple
            #canvas.data["currentBases"] = canvas.data["bases"]
            canvas.data[batterName]['H'] += 1
            hitLocation = getLocation(False)
            changeFieldColor(hitLocation, False, canvas)
            addHitsToScore(canvas)
            advanceRunners(3,batterName,canvas)
            updateLastPlay(canvas, hitLocation)
        else: #home run
            canvas.data[batterName]['H'] += 1
            canvas.data[pitcher]['SO'] +=1
            addHitsToScore(canvas)
            advanceRunners(4,batterName,canvas)
            updateLastPlay(canvas, None, isHomeRun = True, isStrikeout = False, oneBase = None)
    else:
        if random.random()<=SP9I/27: #strikeout
            #canvas.data["currentBases"] = canvas.data["bases"]
            canvas.data["outs"] += 1
            canvas.data[pitcher]["IP"] += (1.0/3)
            canvas.data[pitcher]['SO'] +=1
            updateLastPlay(canvas, None, False, True, None)
            isBattingOver(canvas)
        else: #other kind of out
            outLocation = getLocation(True)
            location = outLocation
            changeFieldColor(outLocation, True, canvas)
            bases = canvas.data
            #HARD- CODE SPECIAL SCENARIOS
            if outLocation == "Infield":        
                #double play scenarios
                if checkForPlayer(True,False,False,canvas):
                    if canvas.data["outs"] <= 1:
                        canvas.data["outs"] += 2
                        canvas.data[pitcher]["IP"] += (2.0/3)
                        updateLastPlay(canvas, location)
                        #canvas.data["currentBases"] = canvas.data["bases"]
                        if isBattingOver(canvas) == False:
                            manualAdvance(1,1,True,canvas)
                    else:
                        canvas.data["outs"] += 1
                        canvas.data[pitcher]["IP"] += (1.0/3)
                        #canvas.data["currentBases"] = canvas.data["bases"]
                        updateLastPlay(canvas, location)
                        isBattingOver(canvas)
                elif checkForPlayer(True,True,False,canvas):
                    if canvas.data["outs"] <= 1:
                        canvas.data["outs"] += 2
                        canvas.data[pitcher]["IP"] += (2.0/3)
                        updateLastPlay(canvas, location)
                        #canvas.data["currentBases"] = canvas.data["bases"]
                        if isBattingOver(canvas) == False:
                            manualAdvance(2,1,False,canvas)
                            manualAdvance(1,1,True,canvas)
                    else:
                        canvas.data["outs"] += 1
                        canvas.data[pitcher]["IP"] += (1.0/3)
                        #canvas.data["currentBases"] = canvas.data["bases"]
                        updateLastPlay(canvas, location)
                        isBattingOver(canvas)
                            
                elif checkForPlayer(True,False,True,canvas):
                    if canvas.data["outs"] <= 1:
                        canvas.data["outs"] += 2
                        canvas.data[pitcher]["IP"] += (2.0/3)
                        updateLastPlay(canvas, location)
                        #canvas.data["currentBases"] = canvas.data["bases"]
                        if isBattingOver(canvas) == False:
                            manualAdvance(3,1,False,canvas)
                            manualAdvance(1,1,True,canvas)
                            canvas.data["bases"] = {}
                    else:
                        canvas.data["outs"] += 1
                        canvas.data[pitcher]["IP"] += (1.0/3)
                        #canvas.data["currentBases"] = canvas.data["bases"]
                        updateLastPlay(canvas, location)
                        isBattingOver(canvas)
                            
                elif checkForPlayer(True,True,True,canvas):
                    if canvas.data["outs"] <= 1:
                        canvas.data["outs"] += 2
                        canvas.data[pitcher]["IP"] += (2.0/3)
                        updateLastPlay(canvas, location)
                        #canvas.data["currentBases"] = canvas.data["bases"]
                        if isBattingOver(canvas)== False:
                            manualAdvance(3,1,False,canvas)
                            manualAdvance(2,1,False,canvas)
                            manualAdvance(1,1,True,canvas)
                    else:
                        canvas.data["outs"] += 1
                        canvas.data[pitcher]["IP"] += (1.0/3)
                        #canvas.data["currentBases"] = canvas.data["bases"]
                        updateLastPlay(canvas, location)
                        isBattingOver(canvas)
                            
                #other infield scenario
                elif checkForPlayer(False,True,False,canvas):
                    canvas.data["outs"] += 1
                    canvas.data[pitcher]["IP"] += (1.0/3)
                    #canvas.data["currentBases"] = canvas.data["bases"]
                    if isBattingOver(canvas) == False:
                        manualAdvance(2,1,False,canvas)
                    updateLastPlay(canvas, location)
                else:
                    canvas.data["outs"] += 1
                    canvas.data[pitcher]["IP"] += (1.0/3)
                    #canvas.data["currentBases"] = canvas.data["bases"]
                    updateLastPlay(canvas, location)
                    isBattingOver(canvas)
            else: #outfield scenarios, poor style
                canvas.data["outs"] += 1
                canvas.data[pitcher]["IP"] += (1.0/3)
                #canvas.data["currentBases"] = canvas.data["bases"]
                if isBattingOver(canvas)== False:
                    if checkForPlayer(False,False,True,canvas):
                        manualAdvance(3,1,False,canvas)
                        updateLastPlay(canvas, location)
                    if checkForPlayer(False,True,False,canvas):
                        if outLocation == "RightField":
                            manualAdvance(2,1,False,canvas)
                            updateLastPlay(canvas, location)
                    if checkForPlayer(True,True,True,canvas):
                        if outLocation == "RightField":
                            manualAdvance(3,1,False,canvas)
                            manualAdvance(2,1,False,canvas)
                            updateLastPlay(canvas, location)
                        else:
                            manualAdvance(3,1,False,canvas)
                            updateLastPlay(canvas, location)
                updateLastPlay(canvas, location)
    getBaseColors(canvas)
    calculateNewERA(canvas,pitcher)
    if checkIfWalkoff(canvas) == False:
        if canvas.data["outs"] < 3:
            goToNextBatter(canvas)

def calculateNewERA(canvas,pitcher):
    IP = canvas.data[pitcher]["IP"]
    RA = canvas.data[pitcher]['RA']
    if IP == 0:
        if RA == 0:
            canvas.data[pitcher]['ERA'] = 0
        else:
            canvas.data[pitcher]['ERA'] = 99.999
    else:
        era = round((RA/IP)*9,3)
        canvas.data[pitcher]['ERA'] = era
                
def goToNextBatter(canvas):
    if canvas.data["teamBatting"] == canvas.data["awayTeam"]:
        if canvas.data["Player" + str(canvas.data["awayTeam"]) + "Batting"] == 8:
            canvas.data["Player" + str(canvas.data["awayTeam"]) + "Batting"] = 0
        else:
            canvas.data["Player" + str(canvas.data["awayTeam"]) + "Batting"] += 1
    else:
        if canvas.data["Player" + str(canvas.data["homeTeam"]) + "Batting"] == 8:
            canvas.data["Player" + str(canvas.data["homeTeam"]) + "Batting"] = 0
        else:
            canvas.data["Player" + str(canvas.data["homeTeam"]) + "Batting"] += 1 
    
def swapTeams(battingTeam,pitchingTeam,canvas):
    if battingTeam == canvas.data["awayTeam"]:
        canvas.data["teamBatting"] = canvas.data["homeTeam"]
        canvas.data["teamPitching"] = canvas.data["awayTeam"]
    else:
        canvas.data["currentInning"] += 1
        canvas.data["teamBatting"] = canvas.data["awayTeam"]
        canvas.data["teamPitching"] = canvas.data["homeTeam"]   

def checkIfWalkoff(canvas):
    currentInning = canvas.data["currentInning"]
    awayRuns = canvas.data["Player" + str(canvas.data["awayTeam"]) + "TotalRuns"]
    homeRuns = canvas.data["Player" + str(canvas.data["homeTeam"]) + "TotalRuns"]
    if currentInning >= 8 and canvas.data["teamBatting"] == canvas.data["homeTeam"]:
        if homeRuns > awayRuns:
            canvas.data["isGameOver"] = True
            canvas.data["winner"] = canvas.data["homeTeam"]
            canvas.data["lastPlay"] = "The Home Team Wins"
            canvas.data["linesOfLastPlay"] = 1
            return True
    return False
    

def checkIfGameOver(canvas):
    currentInning = canvas.data["currentInning"]
    awayRuns = canvas.data["Player" + str(canvas.data["awayTeam"]) + "TotalRuns"]
    homeRuns = canvas.data["Player" + str(canvas.data["homeTeam"]) + "TotalRuns"]
    if currentInning >= 8:
        if canvas.data["teamBatting"] == canvas.data["awayTeam"]:
            if homeRuns > awayRuns:
                canvas.data["isGameOver"] = True
                canvas.data["winner"] = canvas.data["homeTeam"]
                canvas.data["lastPlay"] = "The Home Team Wins"
                canvas.data["linesOfLastPlay"] = 1
                return True
        else:
            if homeRuns > awayRuns:
                canvas.data["isGameOver"] = True
                canvas.data["winner"] = canvas.data["homeTeam"]
                canvas.data["lastPlay"] = "The Home Team Wins"
                canvas.data["linesOfLastPlay"] = 1
                return True
            elif awayRuns > homeRuns:
                canvas.data["isGameOver"] = True
                canvas.data["winner"] = canvas.data["awayTeam"]
                canvas.data["lastPlay"] = "The Away Team Wins"
                canvas.data["linesOfLastPlay"] = 1
                return True
            else:
                canvas.data['innings'] += 1
                canvas.data["Player1Runs"].append(None)
                canvas.data["Player2Runs"].append(None)
                return False
    return False

def runHalfInning(canvas):
    outs = canvas.data["outs"]
    ##################
    # set up variables
    ##################
    #reset outs if at the begining of a half inning
    if canvas.data["outs"] == 3:
        resetField(canvas)
        canvas.data["lastPlay"] = ""
        canvas.data["outs"] = 0
        battingTeam = canvas.data["teamBatting"]
        pitchingTeam = canvas.data["teamPitching"]
        if checkIfGameOver(canvas)== False:
            goToNextBatter(canvas)
            swapTeams(battingTeam, pitchingTeam, canvas) #switches which team is batting and pitching
        canvas.data["lastPlay"] = "Batting Team Change"
        canvas.data["linesOfLastPlay"] = 1
        return
    if canvas.data["teamBatting"] == canvas.data["awayTeam"]:
        if canvas.data["Player" + str(canvas.data["awayTeam"]) + "Runs"][canvas.data["currentInning"]] == None:
            canvas.data["Player" + str(canvas.data["awayTeam"]) + "Runs"][canvas.data["currentInning"]] = 0
            
    else:
        if canvas.data["Player" + str(canvas.data["homeTeam"]) + "Runs"][canvas.data["currentInning"]] == None:
            canvas.data["Player" + str(canvas.data["homeTeam"]) + "Runs"][canvas.data["currentInning"]] = 0
    resetField(canvas)      
    battingTeam = canvas.data["teamBatting"]
    pitchingTeam = canvas.data["teamPitching"]
    teambatterNames = canvas.data['startingLineOfPlayer' + str(battingTeam)]
    batterName = teambatterNames[currentbatterName(canvas)]
    pitcher = canvas.data['currentPitcherOfPlayer' + str(pitchingTeam)][0]
    # batting stats of current batterName
    avg = float(canvas.data[batterName]['battingAverage'])
    obp = float(canvas.data[batterName]['onBasePercentage'])
    plateAp = float(canvas.data[batterName]['plateAppearance'])
    hits = float(canvas.data[batterName]['hits'])
    hr = float(canvas.data[batterName]['homeRuns'])
    trip = float(canvas.data[batterName]['triples'])
    double = float(canvas.data[batterName]['doubles'])
    single = hits - (hr+trip+double)
    bb = float(canvas.data[batterName]['walks'])
    hitBy = float(canvas.data[batterName]['hitByPitches'])
    # pitching stats
    SP9I = float(canvas.data[pitcher]['strikeoutsPerNineInnings'])
    #WP9I = pitcher['walksPerNineInnings']
    whip = float(canvas.data[pitcher]['walks+HitsPerInningPitched'])
    battersFaced = float(canvas.data[pitcher]['battersFaced'])
    pitcherPosition = canvas.data[pitcher]['position']
    obp = float(getAdjustedobp(obp, whip, battersFaced, pitcherPosition))
    outs = 0
    totalOnBase = float(hits + bb + hitBy)
    range1 = ((single+hitBy+bb)/totalOnBase)*obp
    range2 = ((double/totalOnBase)*obp) + range1
    range3 = ((trip/totalOnBase)*obp) + range2
    ##################
    # play ball!
    ##################
    runAtBat(single, bb, hitBy,SP9I, obp, range1,range2,range3,canvas, batterName, pitcher)

def resetField(canvas):
    canvas.data["firstBaseColor"] = "white"
    canvas.data["secondBaseColor"] = "white"
    canvas.data["thirdBaseColor"] = "white"
    canvas.data["RightFieldColor"] = "green"
    canvas.data["LeftFieldColor"] = "green"
    canvas.data["CenterFieldColor"] = "green"
    canvas.data["InfieldColor"] = "darkgreen"

def terminateBatting(canvas):
    canvas.data["bases"] = {}
