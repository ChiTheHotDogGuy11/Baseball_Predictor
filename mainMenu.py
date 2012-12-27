
def drawBackground(canvas):
    width = canvas.data['width']
    height = canvas.data['height']
    #canvas.create_rectangle(0,0,width,height,fill="darkgray")
    image = canvas.data["image"]
    canvas.create_image(width/2, height/2, image=image)

def drawBoxes(canvas):
    width = canvas.data['width']
    height = canvas.data['height']
    boxWidth = canvas.data["boxWidth"]
    boxHeight = canvas.data["boxHeight"]
    margin = canvas.data["boxMargin"]
    left = width/2 - (boxWidth/2)
    right = width/2 + (boxWidth/2)
    box1Top = height/2 + 40
    box2Top = box1Top + boxHeight + margin
    box3Top = box2Top + boxHeight + margin
    canvas.create_rectangle(left, box1Top, right, box1Top + boxHeight, fill = "red")
    msg1 = "Play Ball!"
    canvas.create_text(width/2,box1Top + boxHeight/2, text=msg1, font=("Helvetica", boxHeight-5))
    canvas.create_rectangle(left, box2Top, right, box2Top + boxHeight, fill = "red")
    msg2 = "Help"
    canvas.create_text(width/2,box2Top + boxHeight/2, text=msg2, font=("Helvetica", boxHeight-5))
 #   canvas.create_rectangle(left, box3Top, right, box3Top + boxHeight, fill = "red")
  #  msg3 = "Options"
   # canvas.create_text(width/2,box3Top + boxHeight/2, text=msg3, font=("Helvetica", boxHeight-5))

def makeHelpScreen(canvas):
    width = canvas.data['width']
    height = canvas.data['height']
    helpLeft = width/2 - width/ 4
    helpTop = height/2 - height/4
    helpRight = width/2 + width/4
    helpBot = height/2 + height/4
    canvas.create_rectangle(helpLeft, helpTop, helpRight, helpBot, fill = "orange")
    message = ""
    message += "            Welcome to Baseball Simulator 2010!           \n"
    message += "You can use this tool to simulate an actual baseball game.\n"
    message += "You can create your own teams from a list of eligible    \n"
    message += "players who competed during the 2010 MLB Season.       \n"
    message += "              Click \"Play Ball!\" to begin the game!           "
    canvas.create_text((helpLeft + helpRight)/2, (helpTop + helpBot)/2, text = message, font = ("Helvetica", 14))
    #make box to exit help screen and return to main menu
    exitBoxWidth = 140
    exitBoxHeight = 30
    exitBoxLeft = helpRight - width/4
    exitBoxTop = helpBot - (15 + exitBoxHeight)
    exitShift = 80
    canvas.create_rectangle(exitBoxLeft + exitShift, exitBoxTop, exitBoxLeft + exitBoxWidth + exitShift, exitBoxTop + exitBoxHeight, fill = "red")
    canvas.create_text(exitBoxLeft + exitBoxWidth/2 + exitShift, exitBoxTop + exitBoxHeight/2, text="Back to Main Menu", font=("Helvetica", 12))

def mousePressedInHelp(canvas,eventx,eventy):
    width = canvas.data['width']
    height = canvas.data['height']
    helpLeft = width/2 - width/ 4
    helpTop = height/2 - height/4
    helpRight = width/2 + width/4
    helpBot = height/2 + height/4
    exitBoxWidth = 140
    exitBoxHeight = 30
    exitShift = 80
    exitBoxLeft = helpRight - width/4 + exitShift
    exitBoxTop = helpBot - (15 + exitBoxHeight)
    if eventx <= exitBoxLeft + exitBoxWidth and eventx >= exitBoxLeft and eventy <= exitBoxTop + exitBoxWidth and eventy >= exitBoxTop:
        canvas.data["displayHelpScreen"] = False
        
def mousePressedInMenu(canvas, eventx, eventy):
    width = canvas.data['width']
    height = canvas.data['height']
    boxWidth = canvas.data["boxWidth"]
    boxHeight = canvas.data["boxHeight"]
    margin = canvas.data["boxMargin"]
    left = width/2 - (boxWidth/2)
    right = width/2 + (boxWidth/2)
    box1Top = height/2 + 20
    box2Top = box1Top + boxHeight + margin
    box3Top = box2Top + boxHeight + margin
    if eventx <= right and eventx >= left:
        if eventy >= box1Top and eventy <= box1Top + boxHeight:
            canvas.data["displayHelpScreen"] = False
            canvas.data["state"] = "creation"
        elif eventy >= box2Top and eventy <= box2Top + boxHeight:
            canvas.data["displayHelpScreen"] = True
        #elif eventy >= box3Top and eventy <= box3Top + boxHeight:
            #makeOptionsScreen(canvas) 
