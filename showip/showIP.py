from PIL import Image, ImageFont, ImageDraw
import subprocess as sp
from subprocess import Popen, PIPE
import shlex
import re


class ShowIP:
   def __init__(self):

#ip route response:
#default via 192.168.4.1 dev eth0 proto dhcp src 192.168.4.115 metric 203
#192.168.4.0/24 dev eth0 proto dhcp scope link src 192.168.4.115 metric 203
 
     self.cmds_2 = []
     self.cmds_2.append("ip route")
     self.cmds_2.append("grep -E '^(([[:digit:]]{1,3}\.){3}[[:digit:]]{1,3}/[0-9]{1,2})'")
     self.cmds_2.append("cat")

   def _getPipedResp(self, cmds):
     p = [0 for c in cmds]
     for i,c in enumerate(cmds):
         args = shlex.split(c)
         if i == 0: # first time
              p[i] = Popen(args, stdout=PIPE)
         else:
              p[i] = Popen(args, stdin=p[i-1].stdout, stdout=PIPE)
     p[0].stdout.close()
     resp = str(p[len(p)-1].communicate()[0], 'utf-8')
     return resp

   def getIPText(self):
     resp = self._getPipedResp(self.cmds_2)
     pat = "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}"
     net = re.findall(pat, resp)

     pat = "link src ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"
     host = re.findall(pat, resp)
     if not net or not host or "169" in host:
        net = ''
        host = ''
        connected = False
     else:
        net = net[0]
        host = host[0]
        connected = True
     return connected, net, host

   def getHostname(self):
     p = sp.run("hostname", capture_output=True)
     pstr = str(p.stdout, 'utf-8')
     hnText = pstr
     return hnText


if __name__ == "__main__":
   sip = ShowIP()
   res = sip.getIPText()
   host = sip.getHostname()
   print("IP: {}, host: {}".format(res,host))
