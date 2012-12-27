# scrape.py
# 11/14/2010
# Part of the Baseball Sinulation
# Made by Akash Katipally and Justin Greet
# 1) Gets the list of all the teams in the league.
# 2) Gets the players from all of the team.
# 3) Batters stored must have a minimum ammount of at bats.
# 4) Pitches must have at least 20 innings pitched.
# 5) Stores each player in their respective position folder
# 6) Also calculates the mean and st dev of OBP and WHIP

import urllib2
import math

def substringBetween(string, leftDelimiter, rightDelimiter):
    index1 = string.find(leftDelimiter) + len(leftDelimiter)
    index2 = string.find(rightDelimiter)
    return string[index1:index2]

def getTeamList():
    # Get a list of the 30 teams
    url = "http://www.baseball-reference.com/teams/"
    urlHandler = urllib2.urlopen(url)
    source = urlHandler.readlines()
    urlHandler.close()
    teams = {}
    for line in source:
        # Once we have 30 teams, return the dictionary
        if len(teams) == 30:
            return teams
        # Look for the team name and the acronym
        if 'class=" franchise_names"><a href=' in line:
            parts = line.rstrip().split("/")
            teamAcronym = parts[2]
            # Some teams have different ancronyms between the teams page and the team statistic page.
            if teamAcronym == "TBD":
                teamAcronym = "TBR"
            if teamAcronym == "ANA":
                teamAcronym = "LAA"
            string = parts[3]
            teamName = substringBetween(string, ">", "<")
            teams[teamAcronym] = teamName

def storeData(data,pitcher):
    # Stores the player information. If we are storing batters, the pitcher's batting statistics arent recorded
    position = data[0]
    player = data[1]
    if pitcher == 1 or position != 'P':
        # Stores them in the position folder and the file name is the player name
        fileHandler = open("Statistics" + '/' + position+'/'+player+".txt","w")
        for line in data:
            fileHandler.write(line + '\n')
        fileHandler.close()

def convertData(rawStatistics,pitcher = 0):
    global OBP
    global OBPcounter
    global WHIP
    global WHIPcounter
    # This stores all the data into a nice list that can be used for storing
    dataToStore = []
    # Gets the position, we have 2 cases as half are formatted differently
    if '<strong>' in rawStatistics[0]:
        dataToStore.append(substringBetween(rawStatistics[0], '<strong>', '</strong>'))
    else:
        dataToStore.append(substringBetween(rawStatistics[0], '">', '</td'))
    # Gets the player name
    dataToStore.append(substringBetween(rawStatistics[1], 'shtml">', '</a>'))
    # Gets rest of the statistics
    for line in rawStatistics[2:]:
        dataToStore.append(substringBetween(line, '<td align="right" >', '</td>'))
    # Some pitchers have no positition listed, so we make them as P
    if dataToStore[0] == "":
        dataToStore[0] = 'P'
    #Batters must have a minimum ammount of At-bats
    # Pitchers must have minimum ammount of innings pitched
    if pitcher == 0:
        if float(dataToStore[5])>=40:
            storeData(dataToStore,pitcher)
            OBP.append(float(dataToStore[17]))          
    else:
        if float(dataToStore[13]) >=20:
            storeData(dataToStore, pitcher)
            WHIP.append(float(dataToStore[26]))

def getTeamPlayers(url,batterOrPitcher):
    urlHandler = urllib2.urlopen(url)
    source = urlHandler.readlines()
    urlHandler.close()
    counter = 0
    inData = False
    inPlayer = False
    pitcher = 0
    counter = 0
    if batterOrPitcher == "pitcher":
        codeToLookFor = '<th align="center"  class="tooltip hide_non_quals"  tip="<strong>SO/BB</strong><br>For recent years, leaders need 1 IP<br>per team game played">SO/BB</th>'
        pitcher = 1
    else:
        codeToLookFor = '<th align="center"  class="tooltip"  tip="<strong>Intentional Bases on Balls</strong><br>First tracked in 1955.">IBB</th>'    
    for line in source:
        # This line ensures that we got to the part of the code that we are looking for.
        # The for loop stops once we found our data
        if codeToLookFor in line:
            inData = True
            if batterOrPitcher == "batter":
                counter += 1
                if counter == 3:
                    return
        if batterOrPitcher == "pitcher":
            if '</div><!-- table_wrapper -->' in line:
                return
        if inData == True:
            # If we are in midst of a player's code, gather data. Once done, go into the helper function and store the data for the player
            if inPlayer == True:
                if '</tr>' in line:
                    inPlayer = False
                    convertData(rawStatistics,pitcher)
                rawStatistics.append(line.rstrip())
            # We found the player data, so start storing data.
            elif '<td align="left"  csk="' in line:
                rawStatistics = []
                inPlayer = True
                rawStatistics.append(line.rstrip())

def standardDev(aList):
    totalOBP = 0
    sqrdDif = 0
    for item in aList:
        totalOBP += item
    mean = float(totalOBP) / len(aList)
    for item in aList:
        sqrdDif += (item - mean)**2
    stdDev = math.sqrt(sqrdDif / len(aList))
    return (stdDev, mean)

def getAllData(teams):
    global OBP
    global WHIP
    OBP = []
    WHIP = []
    acronyms = teams.keys()
    for team in acronyms:
        #get the url of the team     
        urlPitcher = "http://www.baseball-reference.com/teams/" + team + "/2010-pitching.shtml"
        urlBatter = "http://www.baseball-reference.com/teams/" + team + "/2010-batting.shtml"
        getTeamPlayers(urlPitcher,"pitcher")
        getTeamPlayers(urlBatter,"batter")
    print "All Done!"
    (OBPstdDev, OBPmean) = standardDev(OBP)
    (WHIPstdDev, WHIPmean) = standardDev(WHIP)
    fileHandler = open("LeagueStats.txt", "wt")
    fileHandler.write("OBP Std Dev = " + str(OBPstdDev) + "\n")
    fileHandler.write("OBP mean = " + str(OBPmean) + "\n")
    fileHandler.write("WHIP Std Dev = " + str(WHIPstdDev) + "\n")
    fileHandler.write("WHIP mean = " + str(WHIPmean) + "\n")
    fileHandler.close()

