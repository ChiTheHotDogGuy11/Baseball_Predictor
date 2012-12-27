def makeBatterDictionary(canvas,batter):
    name = batter[1]
    name = {}
    name["position"] = batter[0]
    name["age"] = batter[2]
    name['games'] = batter[3]
    name['plateAppearance'] = batter[4]
    name['atBats'] = batter[5]
    name['runs'] = batter[6]
    name['hits'] = batter[7]
    name['doubles'] = batter[8]
    name['triples'] = batter[9]
    name['homeRuns'] = batter[10]
    name['runsBattedIn'] = batter[11]
    name['stolenBases'] = batter[12]
    name['caughtStealing'] = batter[13]
    name['walks'] = batter[14]
    name['strikeouts'] = batter[15]
    name['battingAverage'] = batter[16]
    name['onBasePercentage'] = batter[17]
    name['slugging'] = batter[18]
    name['onBasePlusSlugging'] = batter[19]
    name['adjustedOPS'] = batter[20]
    name['totalBases'] = batter[21]
    name['groundIntoDoublePlays'] = batter[22]
    name['hitByPitches'] = batter[23]
    name['sacrificeHits'] = batter[24]
    name['sacrificeFlies'] = batter[25]
    name['intentionalWalks'] = batter[26]
    name['AB'] = 0
    name['PA'] = 0
    name['HBP'] = 0
    name['H'] = 0
    name['RBI'] = 0
    name['R'] = 0
    name['BB'] = 0
    canvas.data[batter[1]] = name

def makePitcherDictionary(canvas,pitcher):
    name = pitcher[1]
    name = {}
    name['position'] = pitcher[0]
    name['age'] = pitcher[2]
    name['wins'] = pitcher[3]
    name['losses'] = pitcher[4]
    name['winLossPercentage'] = pitcher[5]
    name['earnedRunAverage'] = pitcher[6]
    name['games'] = pitcher[7]
    name['gamesStarted'] = pitcher[8]
    name['gamesFinished'] = pitcher[9]
    name['completeGames'] = pitcher[10]
    name['shutoutGames'] = pitcher[11]
    name['saves'] = pitcher[12]
    name['inningsPitched'] = pitcher[13]
    name['hits'] = pitcher[14]
    name['runs'] = pitcher[15]
    name['earnedRuns'] = pitcher[16]
    name['homeRuns'] = pitcher[17]
    name['walks'] = pitcher[18]
    name['intentionalWalks'] = pitcher[19]
    name['strikeouts'] = pitcher[20]
    name['hitByPitches'] = pitcher[21]
    name['balks'] = pitcher[22]
    name['wildPitches'] = pitcher[23]
    name['battersFaced'] = pitcher[24]
    name['earnedRunAverage+'] = pitcher[25]
    name['walks+HitsPerInningPitched'] = pitcher[26]
    name['hitsPerNineInnings'] = pitcher[27]
    name['homeRunsPerNineInnings'] = pitcher[28]
    name['walksPerNineInnings'] = pitcher[29]
    name['strikeoutsPerNineInnings'] = pitcher[30]
    name['strikeoutPerWalkRatio'] = pitcher[31]
    name['RA'] = 0
    name['battersFaced'] = 0
    name['ERA'] = 0.00
    name['BB'] = 0
    name['HBP'] = 0
    name['SO'] = 0
    name['IP'] = 0
    canvas.data[pitcher[1]] = name
    
def storePlayers(canvas,starters,pitcher):
    starters = starters.split("#")
    actualLineup = []
    # remove empty strings
    while "" in starters:
        starters.remove("")
    for starter in starters:
        starter = starter.split("\n")
        while "" in starter:
            starter.remove("")
        # We have the starter, so lets put it into a dictionary
        if starter != []:
            if pitcher == False:
                actualLineup.append(starter[1])
                makeBatterDictionary(canvas,starter)
            else:

                actualLineup.append(starter[1])
                makePitcherDictionary(canvas,starter)
    return actualLineup

def getPlayers(canvas,batters,pitcher):
    # seperate the starters and the bench
    index1 = batters.find("###")
    starters = batters[0:index1]
    bench = batters[index1+3:] #why +3?
    starters  = storePlayers(canvas,starters,pitcher)
    bench = storePlayers(canvas,bench,pitcher)
    return (starters,bench)

def getTeam(canvas,teamName,player):
    fileHandler = open("Teams" + '/' + teamName,"r")
    source = fileHandler.read().split("@@@") #@@@ separates batters and pitchers
    fileHandler.close()
    batters = source[0]
    pitchers = source[1]
    # Get the starters and the bench
    (battingStarters,battingBench) = getPlayers(canvas,batters,False)
    (startingPitcher,pitchingbench) = getPlayers(canvas,pitchers,True)
    canvas.data['startingLineOfPlayer' + str(player)] = battingStarters
    canvas.data['battingBenchOfPlayer' + str(player)] = battingBench
    canvas.data['currentPitcherOfPlayer' + str(player)] = startingPitcher
    canvas.data['pitchingBenchOfPlayer' + str(player)] = pitchingbench
    canvas.data['usedBattersOfPlayer' + str(player)] = []
    canvas.data['usedPitchersOfPlayer' + str(player)] = []

    teamName = teamName.split(".")
    teamName = teamName[0]
    canvas.data['player' + str(player)+'TeamName'] = teamName
