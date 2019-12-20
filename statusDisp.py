from PIL import Image, ImageDraw, ImageFont
from showip.showIP import ShowIP
import subprocess
from subprocess import Popen, PIPE
import shlex
import sys, os
from time import sleep
from datetime import datetime

def _procCmds(cmds):
    p = [0 for c in cmds]
    for i,c in enumerate(cmds):
       args = shlex.split(c)
       if i == 0: # first cmd
           p[i] = Popen(args, stdout=PIPE)
       else:
           p[i] = Popen(args, stdin=p[i-1].stdout, stdout=PIPE)
    p[0].stdout.close()
    resp = str(p[len(p)-1].communicate()[0],'utf-8')
    return resp

def _gatherInfo():
    sip = ShowIP()
    hostname = sip.getHostname()
    connected, net, host = sip.getIPText()
    return connected, net, host, hostname

def _getTime():
    now = datetime.now()
    ascnow = now.strftime("%b %-d, %Y")
    asctime = now.strftime("%-I:%M %p")
    return (ascnow, asctime)

def makeImage():
    connected, net, host, hostname = _gatherInfo()
    dt, dtime = _getTime()

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 20)
    bigfont = ImageFont.truetype(font_path, 22)

    if connected:
        screenColor = "green.png"
    else:
        screenColor = "red.png"
    img = Image.open(screenColor)

    d = ImageDraw.Draw(img)
    fill = (255,255,255)
    d.text((8,110), "Network: {}".format(net), fill=fill, font=font)
    d.text((8,140), "IP: {}".format(host), fill=fill, font=font)
    d.text((8,180), "Hostname: {}".format(hostname), fill=fill, font=font)
    d.text((100,14), "{}".format(dt), fill=fill, font=bigfont)
    d.text((100,50), "{}".format(dtime), fill=fill, font=bigfont)
    img.save('pil_text.png')

def testActive():
    cmd1 = 'ps aux'
    cmd2 = 'grep fbi' 
    cmd3 = 'grep -o noverbose'
    cmds = [cmd1, cmd2, cmd3]
    resp = _procCmds(cmds)
    return 'noverbose' in resp

def main():
    cmd = 'fbi -d /dev/fb0 -noverbose -nocomments -T 1 -t 2 -cachemem 0 pil_text.png pil_text.png pil_text.png'
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    with open('fbi.log', 'wb') as fp:
       fp.write(stdout)
       if stderr:
           fp.write(stderr)

    while True:
       makeImage()
       sleep(1.1414)
       testRes = testActive()

       if not testRes:
          print("test output Failed: {}".format(testRes))
          cmd = 'fbi -d /dev/fb0 -noverbose -nocomments -T 1 -t 2 -cachemem 0 pil_text.png pil_text.png pil_text.png'
          args = shlex.split(cmd)
          sppid = subprocess.run(args, timeout=None)


if __name__ == "__main__":
    main()

