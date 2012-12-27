import gameSummary

def drawBackground(canvas):
    width = canvas.data['width']
    height = canvas.data['height']
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
    box1Top = height/2 - 150
    box2Top = box1Top + boxHeight + margin
    box3Top = box2Top + boxHeight + margin
    box4Top = box3Top + boxHeight + margin
    canvas.create_rectangle(left, box1Top, right, box1Top + boxHeight, fill = "red")
    msg1 = "Play Game Again"
    canvas.create_text(width/2,box1Top + boxHeight/2, text=msg1, font=("Helvetica", 20))
    canvas.create_rectangle(left, box2Top, right, box2Top + boxHeight, fill = "red")
    msg2 = "Restart Team Creation"
    canvas.create_text(width/2,box2Top + boxHeight/2, text=msg2, font=("Helvetica", 20))
    canvas.create_rectangle(left, box3Top, right, box3Top + boxHeight, fill = "red")
    msg3 = "Create Game Report"
    canvas.create_text(width/2,box3Top + boxHeight/2, text=msg3, font=("Helvetica", 20))
    canvas.create_rectangle(left, box4Top, right, box4Top + boxHeight, fill = "red")
    msg4 = "Run Multiple Simulations"
    canvas.create_text(width/2,box4Top + boxHeight/2, text=msg4, font=("Helvetica", 20))

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
    box1Top = height/2 - 150
    box2Top = box1Top + boxHeight + margin
    box3Top = box2Top + boxHeight + margin
    box4Top = box3Top + boxHeight + margin
    if eventx <= right and eventx >= left:
        if eventy >= box1Top and eventy <= box1Top + boxHeight:
            canvas.data["exportTeams"] = True
        elif eventy >= box2Top and eventy <= box2Top + boxHeight:
            canvas.data["state"] = "creation"
        elif eventy >= box3Top and eventy <= box3Top + boxHeight:
            gameSummary.loadHtmlPage(canvas)
        elif eventy >= box4Top and eventy <= box4Top + boxHeight:
            canvas.data["meanScoreReport"] = True
