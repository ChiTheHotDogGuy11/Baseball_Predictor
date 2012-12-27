import math

def drawSound(canvas):
    soundWidth = canvas.data["soundWidth"]
    soundHeight = canvas.data["soundHeight"]
    width = canvas.data["width"]
    height = canvas.data["height"]
    soundLeft = width - soundWidth
    soundBot = soundHeight
    msg = ""
    canvas.create_rectangle(soundLeft, 0, width, soundHeight, fill = "white")
    if canvas.data["isSoundOn"] == True:
        msg = "on"
    else:
        msg = "off"
    canvas.create_text(width - (soundWidth/2), soundHeight/2, text = "Sound is: " + msg, font = ("Helvetica", (15)))

def drawHelpButton(canvas):
    helpWidth = canvas.data["helpWidth"]
    helpHeight = canvas.data["helpHeight"]
    width = canvas.data["width"]
    height = canvas.data["height"]
    helpLeft = width - helpWidth
    top = canvas.data["soundHeight"]
    helpBot = helpHeight + top
    msg = ""
    canvas.create_rectangle(helpLeft, top, width, helpBot, fill = "white")
    canvas.create_text(width - (helpWidth/2), top + helpHeight/2, text = "Help Screen", font = ("Helvetica", (15)))

def clickdrawHelpButton(canvas,eventx,eventy):
    helpWidth = canvas.data["helpWidth"]
    helpHeight = canvas.data["helpHeight"]
    width = canvas.data["width"]
    height = canvas.data["height"]
    top = canvas.data["soundHeight"]
    bottom = helpHeight + top
    right = width
    left = width - helpWidth
    if eventx >= left and eventx <= right and eventy >= top and eventy <= bottom:
        canvas.data["duringGameHelpScreen"] = True

def drawHelpMenu(canvas):
    width = canvas.data["width"]
    height = canvas.data["height"]
    helpHeight = canvas.data["pauseHeight"]-250
    helpWidth = canvas.data["pauseWidth"]
    textHeight = 22
    topLeft = (width/2 - helpWidth/2, height/2 - helpHeight/2)
    botRight = (width/2 + helpWidth/2, height/2 + helpHeight/2)
    canvas.create_rectangle(topLeft, botRight, fill = "orange")
    message = "Press the right arrow key to play out an at bat. \n"
    message += "Make adjustments to your team in the pause screen. \n"
    message +=  canvas.data["player1TeamName"] +", press [q] to pause. \n"
    message +=  canvas.data["player2TeamName"] +", press [p] to pause. \n"
    message += "Click on the sound box to toggle sound on/off. \n"
    message += "Pitcher's performance decreases in direct proportion \n"
    message += "to the number of batters faced. \n"
    message += "Press [Return] to exit this help screen."
    
    
    canvas.create_text(width/2, height/2, text = message, font = ("Helvetica", textHeight))
    

def drawBackground(canvas):
    width = canvas.data['width']
    height = canvas.data['height']
    canvas.create_rectangle(0,0,width,height,fill="darkgray")

def drawMainScoreBoardParts(canvas,left,top,right,bottom, fill,width ):
    canvas.create_rectangle(left,top,right,bottom, fill=fill, width = width)

def scoreboardVerticalLines(canvas,lines,left,top,right,bottom,cyOfTopRow,cyOfMiddleRow,cyOfBottomRow, width,color):
    width = canvas.data["width"]
    height = canvas.data["height"]
    homeTeam = canvas.data["homeTeam"]
    # Makes sure the home team is displayed on the bottom
    if homeTeam == 1:
        player2 = canvas.data["player1TeamName"]
        player1 = canvas.data["player2TeamName"]
    else:
        player1 = canvas.data["player1TeamName"]
        player2 = canvas.data["player2TeamName"]
    # Lets put the values of the top row into one list
    topRow = []
    last9Innings = canvas.data["innings"]-8
    last9Innings = range(last9Innings, canvas.data["innings"]+1)
    topRow += last9Innings
    topRow += ["Runs","Hits"]
    # Lets get the last 9 innings run totals for each team, and total runs and total hits
    awayPlayer = str(canvas.data["awayTeam"])
    awayPlayerData = []
    awayPlayerData += canvas.data["Player"+awayPlayer+"Runs"][canvas.data["innings"]-9:]
    awayPlayerData.append(canvas.data["Player"+awayPlayer+"TotalRuns"])
    awayPlayerData.append(canvas.data["Player"+awayPlayer+"TotalHits"])
    homePlayer = str(canvas.data["homeTeam"])
    homePlayerData = []
    homePlayerData += canvas.data["Player"+homePlayer+"Runs"][canvas.data["innings"]-9:]
    homePlayerData.append(canvas.data["Player"+homePlayer+"TotalRuns"])
    homePlayerData.append(canvas.data["Player"+homePlayer+"TotalHits"])
    # Width between each line
    widthBetweenEachLine = (right-left)/lines
    # Set the width at which the lines start
    left += widthBetweenEachLine
    canvas.create_text(left,cyOfMiddleRow,text=player1,font = 'bold')
    canvas.create_text(left,cyOfBottomRow,text=player2,font = 'bold')
    i=0
    # draw each line
    for col in range(1,lines-1):
        left +=widthBetweenEachLine
        right = left + widthBetweenEachLine
        cx = (left+right)/2
        canvas.create_line(left,top,left,bottom,width=2)
        # print inning
        msg = topRow[i]
        canvas.create_text(cx,cyOfTopRow,text=msg,font = 'bold')
        # print away team data
        msg = awayPlayerData[i]
        if msg == None:
            msg = "-"
        canvas.create_text(cx,cyOfMiddleRow,text=msg)
        #Print home team data
        msg = homePlayerData[i]
        if msg == None:
            msg = "-"
        canvas.create_text(cx,cyOfBottomRow,text=msg) 
        i += 1

def drawScoreBoard(canvas):
    width = canvas.data['width']
    height = canvas.data['height']
    # set bounds of scoreboard
    topOfScoreboard = height*0.25/12
    leftOfScoreboard = width*2.0/12
    bottomOfScoreboard = height*2.0/12
    rightOfScoreboard = width*10.0/12
    #box score
    drawMainScoreBoardParts(canvas,leftOfScoreboard,topOfScoreboard,rightOfScoreboard,bottomOfScoreboard,"white",5)
    # top row
    top = height*0.25/12
    bottom = height*0.80/12
    cyOfTopRow = (top+bottom)/2
    drawMainScoreBoardParts(canvas,leftOfScoreboard,top,rightOfScoreboard,bottom,"orange",0)
    # middle row
    top = height*0.80/12
    bottom = height*1.4/12
    cyOfMiddleRow = (top+bottom)/2
    drawMainScoreBoardParts(canvas,leftOfScoreboard,top,rightOfScoreboard,bottom,"gray90",0)
    # bottom row
    top = height*1.4/12
    bottom = height*2.0/12
    cyOfBottomRow = (top+bottom)/2
    drawMainScoreBoardParts(canvas,leftOfScoreboard,top,rightOfScoreboard,bottom,"gray80",0)
    # draw vertical lines
    cols = 13
    scoreboardVerticalLines(canvas,cols,leftOfScoreboard,topOfScoreboard,rightOfScoreboard,bottomOfScoreboard,cyOfTopRow,cyOfMiddleRow,cyOfBottomRow,width,"blue")
    

def drawOutfield(width, height, boundaries, canvas):
    #left field
    leftFieldColor = canvas.data["LeftFieldColor"]
    canvas.create_arc(boundaries, start = 105, extent = 30, fill = leftFieldColor, outline = leftFieldColor)
    #center field
    centerFieldColor = canvas.data["CenterFieldColor"]
    canvas.create_arc(boundaries, start = 75, extent = 30, fill = centerFieldColor, outline = centerFieldColor)
    #right field
    rightFieldColor = canvas.data["RightFieldColor"]
    canvas.create_arc(boundaries, start = 45, extent = 30, fill = rightFieldColor, outline = rightFieldColor)
    #left baseline arc
    #canvas.create_arc(boundaries, start = 135, extent = 5, fill = "green")
    #right baseline arc
    #canvas.create_arc(boundaries, start = 40, extent = 5, fill = "green")

def drawInfield(width, height, x0, y0, x1, y1, canvas):
    infieldColor = canvas.data["InfieldColor"]
    #infield arc
    newBoundingRectangle = x0 + .18*width, y0 + .18*height, x1- .18*width, y1 - .18*height
    canvas.create_arc(newBoundingRectangle, start = 45, extent = 90, fill = infieldColor, outline = infieldColor)

    #inner rectangle
    xmid = x0 + width/2
    ymid = y0 + .34*height
    yinit = y0 + .20*height
    xinit = x0 + .36*width
    dist = .28
    canvas.create_polygon(xmid, yinit, xinit, ymid, xmid, yinit + dist*height, xinit +dist*width, ymid,
                          fill = "orange", width = 0)

    #arcs around the rectangle
    radius = .04
    rw = radius*width
    rh = radius*height
    #top
    canvas.create_arc(xmid - rw, yinit - rh, xmid + rw, yinit + rh, start = 225, extent = 90,
                      fill = infieldColor, outline = infieldColor)
    #left
    canvas.create_arc(xinit - rw, ymid - rh, xinit + rw, ymid + rh, start = 315, extent = 90,
                      fill = infieldColor, outline = infieldColor)
    #right
    canvas.create_arc(xinit + dist*width - rw, ymid - rh, xinit +dist*width + rw, ymid + rh,
                      start = 135, extent = 90, fill = infieldColor, outline = infieldColor)

    #circles on/ around the rectangle
    #center
    canvas.create_oval(xmid - rw, ymid - rh, xmid + rw, ymid + rh, fill = infieldColor, width = 0)
    #bottom
    canvas.create_oval(xmid - rw, yinit + dist*height - rh, xmid + rw, yinit + dist*height + rh, fill = infieldColor, width = 0)
    
    #bases
    baseLength = 12
    baseHorizon = math.sqrt(2*(baseLength**2))
    baseDispl = ((y0+((y1-y0)/2) - (yinit + dist*height))/2) # find dist. from inner infield to outer, and get the
                                                                   # side length
    #1st
    rightSideX = (xinit +dist*width)+baseDispl
    rightSideY = ymid + baseDispl
    firstColor = canvas.data["firstBaseColor"]
    canvas.create_polygon(rightSideX , rightSideY, rightSideX - baseHorizon/2, rightSideY - baseHorizon/2,rightSideX - baseHorizon,
                          rightSideY, rightSideX - baseHorizon/2, rightSideY + baseHorizon/2, fill = firstColor, width = 0)
    #2nd
    secondColor = canvas.data["secondBaseColor"]
    canvas.create_polygon(xmid, yinit, xmid - baseHorizon/2, yinit + baseHorizon/2, xmid, yinit + baseHorizon,
                          xmid + baseHorizon/2, yinit + baseHorizon/2, fill = secondColor, width = 0)
    #3rd
    thirdColor = canvas.data["thirdBaseColor"]
    leftSideX = (xinit)-baseDispl
    leftSideY = ymid + baseDispl
    canvas.create_polygon(leftSideX , leftSideY, leftSideX + baseHorizon/2, leftSideY - baseHorizon/2,leftSideX + baseHorizon,
                          leftSideY, leftSideX + baseHorizon/2, leftSideY + baseHorizon/2, fill = thirdColor, width = 0)
    #home
    homeLength = 7
    sideLength = 5
    BD = math.sqrt(2*(baseLength**2))
    canvas.create_polygon(xmid, yinit + dist*height+BD-sideLength, xmid+homeLength, (yinit + dist*height) - homeLength+BD-sideLength,
                          xmid - homeLength, (yinit + dist*height) - homeLength+BD-sideLength, fill = "white", width = 0)
    canvas.create_rectangle(xmid - homeLength, ((yinit + dist*height) - homeLength) - 2*sideLength+BD, xmid + homeLength,
                            ((yinit + dist*height) - homeLength)-sideLength+BD, fill = "white", width = 0)
    #pitcher's mound
    moundW = 9
    moundH = 3
    canvas.create_rectangle(xmid - moundW, ymid - moundH, xmid + moundW, ymid + moundH, fill = "white", width = 0)

def drawField(canvas):
    width = canvas.data["width"]
    height = canvas.data["height"]
    rectanglex0 = (13/32.0)*width
    rectangley0 = (5/16.0)*height
    rectanglex1 = width + (3/32.0)*width
    rectangley1 = height + (7/16.0)*height
    boundingRectangle = rectanglex0, rectangley0, rectanglex1, rectangley1
    boundingWidth = rectanglex1 - rectanglex0
    boundingHeight = rectangley1 - rectangley0
    drawOutfield(width, height, boundingRectangle, canvas)
    drawInfield(boundingWidth, boundingHeight, rectanglex0, rectangley0, rectanglex1, rectangley1, canvas)

def drawBattingScoreRows(canvas,left,right,top,bottom,rows):
    counter = 0
    totalHeight = (bottom-top)
    heightOfEachRow = totalHeight/rows
    topOfRow = top
    for row in range(rows):
        
        # first row is orange and every row thereafter alternates between two colors
        if counter == 0:
            color = "orange"
        else:
            if counter % 2 == 1:
                color = "gray90"
            else:
                color = "gray80"
        # color the batter who is on
        playerBatting = str(canvas.data["teamBatting"])
        whoIsUp = canvas.data["Player"+playerBatting +"Batting"] + 1
        if counter == whoIsUp:
            color = "red"
    

        canvas.create_rectangle(left,topOfRow,right,topOfRow + heightOfEachRow, fill=color, width = 2)
        counter += 1
        topOfRow += heightOfEachRow

def drawBattingScoreCols(canvas,left,right,top,bottom,cols):
    midx = (left+right)/2
    widthOfEachCol = (right-midx)/cols
    xLine = midx
    for col in range(cols):
        canvas.create_line(xLine,top,xLine,bottom,width=2)
        xLine += widthOfEachCol

def drawBattingScoreStats(canvas,left,right,top,bottom,cols):
    midx= (right+left)/2
    totalHeight = (bottom-top)
    topOfScoreboard = top
    heightOfEachRow = totalHeight/10
    top += (heightOfEachRow)/2
    # Lets put the player names
    playercx = (midx+left)/2
    lineup = ["Player Name"]
    playerBatting = canvas.data["teamBatting"]
    playerLineup = canvas.data["startingLineOfPlayer" + str(playerBatting)]
    lineup += playerLineup
    for row in range(10):
        msg = lineup[row]
        canvas.create_text(playercx,top,text=msg)
        top += (heightOfEachRow)
    # Lets put the other starts
    top = topOfScoreboard
    top += (heightOfEachRow)/2
    widthOfEachStatCol = (right-midx)/cols
    for row in range(10):
        statcx = midx + widthOfEachStatCol/2
        # Display the stats it represents in the top row
        if row == 0:
            stats = ["POS","AB","H","RBI","R","BB"]
        # Get the statistics of each player
        else:
            player = lineup[row]
            stats = []
            stats.append(str(canvas.data[player]["position"]))
            stats.append(str(canvas.data[player]["AB"]))
            stats.append(str(canvas.data[player]["H"]))
            stats.append(str(canvas.data[player]["RBI"]))
            stats.append(str(canvas.data[player]["R"]))
            stats.append(str(canvas.data[player]["BB"]))
        for col in range(cols):
            canvas.create_text(statcx,top,text=stats[col])
            statcx += widthOfEachStatCol
        top += (heightOfEachRow)
        
def drawBattingScore(canvas):
    width = canvas.data["width"]
    height = canvas.data["height"]
    left = width * 0.25/15
    right = width * 4.75/15
    top = height * 4.0/15
    bottom = height * 12.0/15
    canvas.create_rectangle(left,top,right,bottom, fill="black", width = 5)
    # create Rows
    rows = 10
    drawBattingScoreRows(canvas,left,right,top,bottom,rows)
    # Create Cols
    cols = 6
    drawBattingScoreCols(canvas,left,right,top,bottom,cols)
    # Write Batting Lineup and Stats
    drawBattingScoreStats(canvas,left,right,top,bottom,cols)

def drawLastPlay(canvas):
    lastPlay = canvas.data["lastPlay"]
    width = canvas.data["width"]
    height = canvas.data["height"]
    top = height-100
    rows = canvas.data["linesOfLastPlay"]
    bottom = top + (25)*rows
    left = 10
    right = width/2+ 100
    canvas.create_rectangle(left,top,right,bottom, fill="orange", width = 2)
    cx = (left+right)/2
    cy = (top+bottom)/2
    canvas.create_text(cx,cy,text=lastPlay,font=("Helvetica", 13))

def drawCurrentPitchingScoreRows(canvas,left,right,top,bottom,rows):
    counter = 0
    totalHeight = (bottom-top)
    heightOfEachRow = totalHeight/rows
    topOfRow = top
    for row in range(rows):
        
        # first row is orange and every row thereafter alternates between two colors
        if counter == 0:
            color = "orange"
        else:
            if counter % 2 == 1:
                color = "gray90"
            else:
                color = "gray80"
        canvas.create_rectangle(left,topOfRow,right,topOfRow + heightOfEachRow, fill=color, width = 2)
        counter += 1
        topOfRow += heightOfEachRow

def drawCurrentPitcher(canvas):
    width = canvas.data["width"]
    height = canvas.data["height"]
    rows = 6
    top = 4.0*height/15
    bottom = top + (37.5)*rows
    left = 5.0*width/15
    right = left + 150
    canvas.create_rectangle(left,top,right,bottom, fill="orange", width = 2)
    #lets paint the rows
    drawCurrentPitchingScoreRows(canvas,left,right,top,bottom,rows)
    #lets put the stats of the pitcher
    totalHeight = (bottom-top)
    heightOfEachRow = totalHeight/rows
    cy = top + heightOfEachRow/2
    cx = (right+left)/2
    text = []
    text.append("Current Pitcher")
    # get the current pitcher
    currentPitchingTeam = canvas.data["teamPitching"]
    player = canvas.data["currentPitcherOfPlayer" + str(currentPitchingTeam)][0]
    #add the stats and then print out the stats
    text.append(player)
    text.append("Runs Allowed: " + str(canvas.data[player]["RA"]))
    text.append("Earned Run Average: " + str(canvas.data[player]["ERA"]))
    text.append("Strikeouts: " + str(canvas.data[player]["SO"]))
    text.append("Walks: " +str(canvas.data[player]["BB"]))
    for row in range(rows):
        canvas.create_text(cx,cy,text=text[row])
        cy +=  heightOfEachRow
        
def drawOuts(canvas):
    width = canvas.data["width"]
    height = canvas.data["height"]
    inningWidth=70
    heightOfBox = 60
    widthOfBox = 130 + inningWidth
    top = height*3/15
    bottom = top+heightOfBox
    left = width*11/15
    right = left+widthOfBox
    canvas.create_rectangle(left,top,right,bottom, fill="gray90", width = 2)
    if canvas.data["isGameOver"] == False:
        # inning signs
        cy = (top+bottom)/2
        rightEdgeOfInningLabel = left + inningWidth/2

        if canvas.data["teamBatting"] == canvas.data["awayTeam"]:
            topInning = "red"
            bottomInning = "black"
        else:
            topInning = "black"
            bottomInning = "red"
        canvas.create_polygon(left+5,cy-2,inningWidth/4+left,cy-28,rightEdgeOfInningLabel-5,cy-2,fill=topInning)
        canvas.create_polygon(left+5,cy+2,inningWidth/4+left,cy+28,rightEdgeOfInningLabel-5,cy+2,fill=bottomInning)
        # inning label
        cx = left + inningWidth*3.0/4
        currentInning = int(canvas.data["currentInning"] + 1)
        canvas.create_text(cx,cy,text=currentInning,font=("Helvetica", 25))
        ## Out text
        cx = (left+right)/2  + inningWidth/2
        cy = top + heightOfBox/5.0
        canvas.create_text(cx,cy,text="Outs")
        ## Draw out boxes
        radius = 15
        widthBetweenCircle = 10
        topOfCircle = top + 1.5*heightOfBox/4.0
        bottomOfCircle = topOfCircle + 2*radius
        leftOfCircle = left + 10 + inningWidth
        rightOfCircle = leftOfCircle + 2*radius
        for circle in range(1,4):
            color = "black"
            if circle <= canvas.data["outs"]:
                color = "red"
            canvas.create_oval(leftOfCircle,topOfCircle,rightOfCircle,bottomOfCircle,fill=color)
            leftOfCircle = leftOfCircle + (2*radius) + widthBetweenCircle
            rightOfCircle = leftOfCircle + 2*radius
    else:
        cy = (top+bottom)/2
        cx = (left+right)/2
        msg = "Game Over"
        canvas.create_text(cx,cy, text=msg, font=("Helvetica", 25))
        
def drawHitAndOutColors(canvas):
    width = canvas.data["width"]
    height = canvas.data["height"]
    heightOfBox = 20
    widthOfBox = 20
    #draw out
    top = height * 12.5/15
    bottom = heightOfBox + top
    left = width * 13.5/15
    right = left + widthOfBox
    canvas.create_rectangle(left,top,right,bottom, fill="red", width = 0)
    cy = (top+bottom)/2
    cx = right + 25
    msg = "= out"
    canvas.create_text(cx,cy, text=msg, font=("Helvetica", 13))
    top = bottom + heightOfBox
    bottom = heightOfBox + top
    canvas.create_rectangle(left,top,right,bottom, fill="blue", width = 0)
    cy = (top+bottom)/2
    msg = "= hit"
    canvas.create_text(cx,cy, text=msg, font=("Helvetica", 13))
