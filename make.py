from PIL import Image, ImageFont, ImageDraw
canvasW, canvasH =(320, 240)
green = (34, 177, 76)
red = (222, 60, 60)
white = (255, 255, 255)
grey = (181, 181, 181)
black = (0,0,0)

bg = Image.new('RGB', (canvasW, canvasH), grey)

logo = Image.open("awt_logo.png")
logoW, logoH = logo.size
logoPastePos = (int((canvasW-logoW)/2), 3)

bg.paste(logo, logoPastePos, logo)

fontPath = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
fontSize = 17
font = ImageFont.truetype(fontPath, fontSize)
line = "this line of text fills the screen width"
textOverlay = ImageDraw.Draw(bg)

verticalLineSpace = 0.3 # multiplier ie: .3 means 30%

lineSpaceV = int((canvasH - (logoPastePos[1] + logoH)) / (fontSize+(fontSize*verticalLineSpace)))
for i in range(lineSpaceV):
    textOverlay.text((5, logoH+5+i*(fontSize+(fontSize*verticalLineSpace))), line, fill=black, font=font)


bg.show()
bg.save("new.png")
