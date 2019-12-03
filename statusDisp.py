from PIL import Image, ImageDraw, ImageFont
from showip.showIP import ShowIP
import subprocess
import shlex
import sys, os
from time import sleep

def makeImage():
    sip = ShowIP()
    hname = sip.getHostname()
    connected, net, host = sip.getIPText()

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 20)

    if connected:
        screenColor = "green.png"
    else:
        screenColor = "red.png"
    img = Image.open(screenColor)

    d = ImageDraw.Draw(img)
    d.text((8,110), "Network: {}".format(net), fill=(255,255,255), font=font)
    d.text((8,140), "IP: {}".format(host), fill=(255,255,255), font=font)
    d.text((8,180), "Hostname: {}".format(hname), fill=(255,255,255), font=font)
    img.save('pil_text.png')

def showImage():
    cmd = 'fbi -d /dev/fb0 -noverbose -nocomments -T 1 -t 5 -1 pil_text.png'
    args = shlex.split(cmd)
    sppid = subprocess.run(args)
#    print("subprocess pid = {}".format(sppid.pid))
def main():
    makeImage()
    showImage()


if __name__ == "__main__":

    while True:
       main()
       sleep(5)

