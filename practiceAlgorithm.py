import random

def atBat():
    #slugging = (1*single+2*double+3*trip+4*hr+1*bb+1*hitBy)/float(plateAp)
    counter = 0
    testNum = 1000
    # batting stats
    avg = .319
    obp = .400
    plateAp = 696.0
    hits = 200
    hr = 29
    trip = 3
    double = 41
    single = hits - (hr+trip+double)
    bb = 57
    hitBy = 8  
    # Pitching
    SP9I = 4.8
    whip = 1.0
    # Z Score logic
    OBPStdDev = 0.049774891317
    OBPmean = 0.313796064401
    WHIPStdDev = 0.24552379969
    WHIPmean = 1.37148041237
    OBPZScore = (obp - OBPmean)/OBPStdDev
    WHIPZScore = (whip - WHIPmean)/WHIPStdDev
    # MAke sure we are in bounds
    print "OBPZScore = ", OBPZScore
    print "WHIPZScore = ", WHIPZScore
    # Penalize bad players
    obp += (OBPZScore)*abs(OBPZScore)*(0.02)
    obp += ((WHIPZScore)*abs(WHIPZScore)*(0.086))
    if obp > 0.85:
        obp = 0.85
    if obp < 0.02:
        obp = 0.02
    print "obp = ", obp
    print "whip = ", whip
    oneb = 0
    twob = 0
    threeb = 0
    hr = 0
    so = 0
    go = 0
    outs = 0
    totalOnBase = float(hits + bb + hitBy)
    range1 = ((single+hitBy+bb)/totalOnBase)*obp
    range2 = ((double/totalOnBase)*obp) + range1
    range3 = ((trip/totalOnBase)*obp) +range2

    print range1,range2,range3
    for i in xrange(testNum):
        if random.random()<= obp:
            counter+=1
            #range4 = (hr/obp) + range3
            total = random.random()*obp
            #print range1,range2,range3,total
            if total <=range1:
                #print "single, walk, or hit by pitch"
                oneb += 1.
            elif total >range1 and total <=range2:
                #print "double"
                twob += 1
            elif total > range2 and total<= range3:
                #print "triple"
                threeb += 1
            else:
                #print "HOOOOOOME RUN!"
                hr += 1
        else:
            outs += 1
            if random.random()<=SP9I/27:
                #print "Strikeout"
                so += 1
            else:
                #print "Groundout"
                go += 1
    print "OBP from tests = " + str(float(counter)/testNum)
    print float(oneb)/testNum, float(twob)/testNum, float(threeb)/testNum, float(hr)/testNum,
    print float(so)/outs, float(go)/outs

atBat()

