from PIL import Image, ImageDraw, ImageFont
from showip.showIP import ShowIP
import subprocess
from subprocess import Popen, PIPE
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

def testActive():
    cmd1 = 'ps aux'
    cmd2 = 'grep fbi' 
    cmd3 = 'grep -o noverbose'
    cmds = [cmd1, cmd2, cmd3]
    p = [0 for c in cmds]
    for i,c in enumerate(cmds):
       args = shlex.split(c)
       if i == 0: # first cmd
           p[i] = Popen(args, stdout=PIPE)
       else:
           p[i] = Popen(args, stdin=p[i-1].stdout, stdout=PIPE)
    p[0].stdout.close()
    resp = str(p[len(p)-1].communicate()[0],'utf-8')
 #   print("test output: {}, bool:{}".format(resp, 'noverbose' in resp))
    return 'noverbose' in resp

def main():
    cmd = 'fbi -d /dev/fb0 -noverbose -nocomments -T 1 -t 2 -cachemem 0 pil_text.png pil_text.png pil_text.png'
    args = shlex.split(cmd)
    sppid = subprocess.run(args, timeout=None)

    while True:
       makeImage()
       sleep(1)
       testRes = testActive()

       if not testRes:
          print("test output Failed: {}".format(testRes))
          cmd = 'fbi -d /dev/fb0 -noverbose -nocomments -T 1 -t 2 -cachemem 0 pil_text.png pil_text.png pil_text.png'
          args = shlex.split(cmd)
          sppid = subprocess.run(args, timeout=None)


if __name__ == "__main__":
    main()

