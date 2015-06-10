import paramiko
import getpass
import sys
import time
import re



# Strip out ANSI and control characters from return
ansi_pattern = '\033\[((?:\d|;)*)([a-zA-Z])'
ansi_eng = re.compile(ansi_pattern)
def strip_escape(string=''):
    lastend = 0
    matches = []
    newstring = str(string)
    for match in ansi_eng.finditer(string):
        start = match.start()
        end = match.end()
        matches.append(match)
    matches.reverse()
    for match in matches:
        start = match.start()
        end = match.end()
        string = string[0:start] + string[end:]
    return string


def printDelayedOutput(channel, timeout):
    t = 0
    while not channel.recv_ready():
        time.sleep(1)
        while channel.recv_ready():
            print strip_escape(channel.recv(1024))

        t += 1
        if (t > timeout):
            return True

def wait_for(channel, str, timeout):
    t = 0
    while not channel.recv_ready():
        time.sleep(1)
        while channel.recv_ready():
            recv = strip_escape(channel.recv(1024))
            if str in recv:
                return True
        t += 1
        if (t > timeout):
            return False

def get_output(channel):
    while not channel.recv_ready():
        time.sleep(1)
        
    txt = ""
    while channel.recv_ready():
            txt += channel.recv(1024)

    return strip_escape(txt)

def run(channel, cmd):
    channel.send(cmd + "\r\n")
    return get_output(channel)

def press(channel, k, wait_for_txt=""):
    # https://github.com/gooli/termenu/blob/master/keyboard.py
    keys = {
               'up':     '\x1b[A',
               'down':   '\x1b[B',
               'right':  '\x1b[C',
               'left':   '\x1b[D',
               'enter':  "\r",
               'escape': chr(27),
               'yes':    'Y',
               'F1':     '\x1bOP',
               'F2':     '\x1bOQ'
           }
    channel.send(keys[k])
    
    if wait_for_txt:
        wait_for(channel, wait_for_txt, 30)
        txt = get_output(channel)
    else:
        # eat any text that is generated
        txt = get_output(channel)

    return txt

def prompt_password(host):
    print "Enter ssh password for admin@" + host
    return getpass.getpass()
  
def get_channel(host, pw):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='admin', password=pw)
    channel = ssh.invoke_shell()
    return (channel, ssh)
