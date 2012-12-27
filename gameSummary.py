import copy

def getTopRowForScoreboard(canvas):
    # lets get the dats for the top row
    topRow = ["Player Name"]
    topRow.extend(range(1,canvas.data["innings"]+1))
    topRow.extend(["Runs","Hits"])
    return topRow

def getMiddleOrBottomRowForScoreboard(canvas,player):
    # Makes sure the home team is displayed on the bottom
    middleRow = [canvas.data['player' + str(player)+'TeamName']]
    middleRow.extend(canvas.data["Player"+str(player)+"Runs"])
    middleRow.append(canvas.data["Player"+str(player)+"TotalRuns"])
    middleRow.append(canvas.data["Player"+str(player)+"TotalHits"])
    return middleRow

def getScoreBoard(canvas):
    content = ""
    content += '<table border="1" bordercolor="black"  align="center" >\n'
    topRow = getTopRowForScoreboard(canvas)
    middleRow = getMiddleOrBottomRowForScoreboard(canvas,canvas.data["awayTeam"])
    bottomRow = getMiddleOrBottomRowForScoreboard(canvas,canvas.data["homeTeam"])
    for row in range(3):
        content += "<tr>\n"
        for col in range(canvas.data["innings"]+3):
            if row == 0:
                content += '<td bgcolor="#FF9900" align="center" width='
                if col == 0: content += "125"
                else: content += "30"
                content += '>'
                content += str(topRow[col])
            elif row == 1:
                content += '<td bgcolor="#909090" align="center" width=30>'
                content += str(middleRow[col])
            else:
                content += '<td bgcolor="#787878" align="center" width=30>'
                if bottomRow[col] == None:
                    content += "-"
                else:
                    content += str(bottomRow[col])
            content += "</td>\n"
        content += "</tr>\n"
    return content

def getStatsOfBatter(canvas,player):
    stats = [player]
    stats.append(canvas.data[player]["AB"])
    stats.append(canvas.data[player]["PA"])
    stats.append(canvas.data[player]["HBP"])
    stats.append(canvas.data[player]["H"])
    stats.append(canvas.data[player]["RBI"])
    stats.append(canvas.data[player]["R"])
    stats.append(canvas.data[player]["BB"])
    return stats

def getBatterBoxInfo(canvas,player):
    content = ""
    content += '<table border="1" bordercolor="black"  align="center" >\n'
    ammountOfPlayers = len(canvas.data['startingLineOfPlayer' + str(player)])
    ammountOfPlayers += len(canvas.data['battingBenchOfPlayer' + str(player)])
    ammountOfPlayers += len(canvas.data['usedBattersOfPlayer' + str(player)])
    rows = ammountOfPlayers + 2
    cols = 7
    players = copy.copy(canvas.data['startingLineOfPlayer' + str(player)])
    players.extend(canvas.data['battingBenchOfPlayer' + str(player)])
    players.extend(canvas.data['usedBattersOfPlayer' + str(player)])
    for row in range(rows):
        content += "<tr>\n"
        if row == 0:
            content += '<td bgcolor="#FF9900" align="center" colspan="8" width=400>'
            content += canvas.data['player' + str(player)+'TeamName']
        elif row == 1:
            stats = ['Name','AB','PA','HBP','H','RBI','R','BB']
            for col in range(len(stats)):
                content += '<td bgcolor="#FF9900" align="center" width='
                
                if col == 0: content += "125"
                else: content += "50"
                content += '>'
                content += stats[col]
                content += "</td>\n"
        else:
            stats = getStatsOfBatter(canvas,players[row-2])
            for col in range(len(stats)):
                content += '<td bgcolor="#FF9900" align="center" width='
                
                if col == 0: content += "125"
                else: content += "50"
                content += '>'
                content += str(stats[col])
                content += "</td>\n"
        content += "</td>\n"
        content += "</tr>\n"
    return content

def getStatsOfPitcher(canvas,player):
    stats = [player]
    stats.append(canvas.data[player]["RA"])
    stats.append(canvas.data[player]["ERA"])
    stats.append(canvas.data[player]["BB"])
    stats.append(canvas.data[player]["HBP"])
    stats.append(canvas.data[player]["SO"])
    stats.append(canvas.data[player]["IP"])
    return stats

def getPitcherBoxInfo(canvas,player):
    content = ""
    content += '<table border="1" bordercolor="black"  align="center" >\n'
    ammountOfPlayers = len(canvas.data['currentPitcherOfPlayer' + str(player)])
    ammountOfPlayers += len(canvas.data['pitchingBenchOfPlayer' + str(player)])
    ammountOfPlayers += len(canvas.data['usedPitchersOfPlayer' + str(player)])
    rows = ammountOfPlayers + 2
    cols = 7
    players = copy.copy(canvas.data['currentPitcherOfPlayer' + str(player)])
    players.extend(canvas.data['pitchingBenchOfPlayer' + str(player)])
    players.extend(canvas.data['usedPitchersOfPlayer' + str(player)])
    for row in range(rows):
        content += "<tr>\n"
        if row == 0:
            content += '<td bgcolor="#FF9900" align="center" colspan="7" width=400>'
            content += canvas.data['player' + str(player)+'TeamName']
        elif row == 1:
            stats = ['Name','RA','ERA','BB','HBP','SO','IP']
            for col in range(len(stats)):
                content += '<td bgcolor="#FF9900" align="center" width='
                
                if col == 0: content += "125"
                else: content += "50"
                content += '>'
                content += stats[col]
                content += "</td>\n"
        else:
            stats = getStatsOfPitcher(canvas,players[row-2])
            for col in range(len(stats)):
                content += '<td bgcolor="#FF9900" align="center" width='
                
                if col == 0: content += "125"
                else: content += "50"
                content += '>'
                content += str(stats[col])
                content += "</td>\n"
        content += "</td>\n"
        content += "</tr>\n"
    return content
    

def createHtmlPage(canvas):
    page = '<html>\n'
    page += '<head>\n'
    page += '<title>' + "GAME REPORT" + '</title>\n'
    page += '</head>\n'
    page += '<body bgcolor="#D0D0D0"> \n' + getScoreBoard(canvas) + '<p><br>'
    page += getBatterBoxInfo(canvas,"1") + getBatterBoxInfo(canvas,"2") +getPitcherBoxInfo(canvas,"1") + getPitcherBoxInfo(canvas,"2") + '</body>\n'
    page += '</html>\n'
    return page

def saveText(text, fileName):
    fileHandler = open(fileName, "wt")
    fileHandler.write(text)
    fileHandler.close()

def loadHtmlPage(canvas):
    page = createHtmlPage(canvas)
    saveText(page, "htmlReport.html")
    import webbrowser
    webbrowser.open("htmlReport.html")
