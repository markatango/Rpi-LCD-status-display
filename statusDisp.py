from PIL import Image, ImageDraw, ImageFont
from showip.showIP import ShowIP
import subprocess
from subprocess import Popen, PIPE
import shlex
import sys, os
from time import sleep
from datetime import datetime
import hashlib


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
    connected, net, host, mac = sip.getIPText()
    return connected, net, host, mac, hostname

def _getTime():
    now = datetime.now()
    ascnow = now.strftime("%b %-d, %Y")
    asctime = now.strftime("%-I:%M %p")
    return (ascnow, asctime)

def makeImage():
    connected, net, host, mac, hostname = _gatherInfo()
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
    d.text((8,105), "Network: {}".format(net), fill=fill, font=font)
    d.text((8,131), "IP: {}".format(host), fill=fill, font=font)
    d.text((8,157), "MAC: {}".format(mac), fill=fill, font=font)
    d.text((8,183), "Hostname: {}".format(hostname), fill=fill, font=font)
    d.text((100,14), "{}".format(dt), fill=fill, font=bigfont)
    d.text((100,50), "{}".format(dtime), fill=fill, font=bigfont)
#    cmd = 'rm ./pil*'
#    args = shlex.split(cmd)
#    p = subprocess.Popen(args, stdout=subprocess.DEVNULL)
    img.save('pil_text.png')
    # cmd = 'mv pil_text.temp.png pil_text.png'
    # args = shlex.split(cmd)  
    # p = subprocess.Popen(args, stdout=subprocess.DEVNULL)

def testActive():
    cmd1 = 'ps aux'
    cmd2 = 'grep fbi' 
    cmd3 = 'grep -o noverbose'
    cmds = [cmd1, cmd2, cmd3]
    resp = _procCmds(cmds)
    return 'noverbose' in resp

def main():
    # cli commands
    updateDisplayCmd = 'fbi -d /dev/fb0 -noverbose -once -cachemem 1 -nocomments -readahead -T 1 pil_text.png'
    killFbiCmd = 'pkill fbi'
    getFbiPid = 'pgrep fbi'
    killPid = 'kill {}'

    # internal function to execute cli commands
    def execute_cmd(cmd):
        args = shlex.split(cmd)
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        return p.communicate()
        #stdout, stderr = p.communicate()

    # first things first.. lets start with a clean slate.. no running fbi processes
    execute_cmd(killFbiCmd)
           
    
    imageHashWas=None
    imageHashNow=None

    # get two instances of fbi running initially.  this, for some reason, prevents killing
    # the fbi processes from blanking out the display and showing "oops terminated" in console
    makeImage()
    logger.debug("starting the first fbi processes now..")
    execute_cmd(updateDisplayCmd)
    pid, _ = execute_cmd(getFbiPid)
    #mainPid = pid.pop(0).strip().decode('utf-8')
    pid = pid.strip().decode('utf-8').split('\n')
    if len(pid) > 1:
        logger.debug("what the heck?! ..there should only be one fbi process running")
    mainPid = pid.pop(0)
    logger.debug("main fbi PID: {}".format(mainPid))

    while True:
        # the display, once written to by fbi, does not need fbi running in the
        # background, so we just just blindly issue a command to kill it.
        #execute_cmd(killFbiCmd)

        # make a new image every loop and capture an sha1 hash of the image
        makeImage()
        imageHashNow=hashlib.sha1(open('pil_text.png', 'rb').read()).hexdigest()

        # here we detect if the image has changed
        # we dont write to the display unless the image has changed 
        if imageHashNow != imageHashWas:
            execute_cmd(updateDisplayCmd)
            pid, _ = execute_cmd(getFbiPid)
            pid = pid.decode('utf-8').strip().split('\n')
            logger.debug("fbi processes: {}".format(pid))
            pid.remove(mainPid)
            if pid:
                for n in pid:
                #for n in pid[1:]: 
                    logger.debug("killing fbi process: {}".format(n))
                    execute_cmd(killPid.format(n))
        imageHashWas = imageHashNow
        
        sleep(1)


if __name__ == "__main__":
    import logging
    import logging.handlers
    import sys

    #create local logger
    logger = logging.getLogger(__name__)
    LOG_TO_CONSOLE = True

    if LOG_TO_CONSOLE:
        handler = logging.StreamHandler(stream=sys.stdout)
    else:
        handler = logging.handlers.RotatingFileHandler(__file__+'.log', maxBytes=5000000, backupCount=1)

    formatter = logging.Formatter(fmt='%(asctime)s %(name) -55s %(levelname)-9s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    #create a logging whitelist - (comment out code in ~~ block to enable all child loggers)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    loggingWhitelist = ('root', '__main__')
    class Whitelist(logging.Filter):
        def __init__(self, *whitelist):
            self.whitelist = [logging.Filter(name) for name in whitelist]
        
        def filter(self, record):
            return any(f.filter(record) for f in self.whitelist)
    #add the whitelist filter to the handler
    handler.addFilter(Whitelist(*loggingWhitelist))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #assign the handler to root logger (we use the root logger so that we get output from all child logger used in other modules)
    logging.root.addHandler(handler)
    #set the logging level for root logger
    logging.root.setLevel(logging.DEBUG)

    main()

