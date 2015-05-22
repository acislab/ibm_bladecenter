#!/usr/bin/python

import paramiko
import getpass
import sys
import time
import re

# Output the received data for every command
VERBOSE = True

host = sys.argv[1]
print "Enter ssh password for admin@" + host
pw = getpass.getpass()


def linesToDict(txt):
    dict = {}
    for l in txt.split("\r\n"):
            if ":" in l:
                words = l.split(":")
                if words[0].strip() in dict:
                    key = last_l.strip() + " " + words[0].strip()
                else:
                    key = words[0].strip()
                dict[ key ] = ":".join(words[1:]).strip()
            else:
                last_l = l
            
    return dict

ansi_pattern = '\033\[((?:\d|;)*)([a-zA-Z])'
ansi_eng = re.compile(ansi_pattern)

# Strip out ANSI and control characters from return
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
    global VERBOSE
    t = 0
    while not channel.recv_ready():
        time.sleep(1)
        while channel.recv_ready():
            recv = strip_escape(channel.recv(1024))
            if VERBOSE:
                print recv
            if str in recv:
                return True
        t += 1
        if (t > timeout):
            return False

def getOutput(channel):
    while not channel.recv_ready():
        time.sleep(1)
        
    txt = ""
    while channel.recv_ready():
            txt += channel.recv(1024)

    return strip_escape(txt)

def run(channel, cmd):
    channel.send(cmd + "\r\n")
    return linesToDict(getOutput(channel))

def press(channel, k):
    global VERBOSE
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
    txt = getOutput(channel)
    if VERBOSE:
        print txt

    return txt


def enable_vtd(channel):
    press(channel, 'down')
    press(channel, 'enter')
    press(channel, 'enter')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'enter')
    press(channel, 'up')
    press(channel, 'enter')
    press(channel, 'escape')
    press(channel, 'escape')
    # One extra escape, seems to be a timing bug somewhere
    # wait_for would be better but the ANSI stripper seems not 
    # quite right and this screen messes it up
    r = press(channel, 'escape')
    return r

def load_defaults(channel):
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'enter')
    wait_for(channel, 'Load Default Settings', 90)
    press(channel, 'up')
    press(channel, 'up')
    press(channel, 'up')
    press(channel, 'up')
    press(channel, 'up')
    press(channel, 'up')
    press(channel, 'up')
    press(channel, 'up')
    press(channel, 'up')

def enable_sol(channel):
    # http://www-01.ibm.com/support/knowledgecenter/SS9H2Y_4.0.1/com.ibm.dp.xi.doc/administratorsguide.xi50171.htm%23webgui_enableserialoverlanforbladeservers_task
    # Move to Console Redirect Settings page
    press(channel, 'down')
    press(channel, 'enter')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'enter')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'enter')
    # Enable Remote Console
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'enter')
    press(channel, 'up')
    press(channel, 'enter')
    # Set Com 2 settings
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'down')
    press(channel, 'enter')
    press(channel, 'up')
    press(channel, 'enter')
    press(channel, 'down')
    press(channel, 'enter')
    press(channel, 'down')
    press(channel, 'enter')
    # Back to main page
    time.sleep(3)
    press(channel, 'escape')
    time.sleep(3)
    press(channel, 'escape')
    time.sleep(3)
    press(channel, 'escape')


def save_exit(channel):
    press(channel, 'escape')
    time.sleep(3)
    r = press(channel, 'yes')
    return r


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(host, username='admin', password=pw)

channel = ssh.invoke_shell()

# http://www-01.ibm.com/support/knowledgecenter/SS9H2Y_4.0.1/com.ibm.dp.xi.doc/administratorsguide.xi50171.htm%23webgui_enableserialoverlanforbladeservers_task
# http://publib.boulder.ibm.com/infocenter/bladectr/documentation/index.jsp?topic=/com.ibm.bladecenter.advmgtmod.doc/kp1bc_bc_cli_console.html
# Eat the login messages
b_info = getOutput(channel)
# Set the timeout to 1 hour so things like the diagnostics boot and config don't time out
run(channel, 'tcpcmdmode -t 3600 -T system:mm[0]')


# Set the boot device to the media tray USB and move the media tray to this 
# blade
run(channel, 'bootseq cd -T system:blade[8]')
run(channel, 'mt -b 8 -T system')
# Power cycle and connect a console for commands
run(channel, 'power -cycle -T system:blade[8]')
run(channel, 'console -o -l -T system:blade[8]')

# Single debugging commands here
#load_defaults(channel)

# For debugging, will just print output of terminal
printDelayedOutput(channel, 10000)




# Update BIOS
#if wait_for(channel, '<F12> Select Boot Device', 9999):
#    press(channel, 'F12')

# expect, power cycle
# set media tray to none to indicate the firmware is done
run(channel, 'bootseq cd usb hd0 nw -T system:blade[8]')
run(channel, 'mt -b 0 -T system')

# Set BIOS options
#if wait_for(channel, '<F1> Setup', 9999):
#    press(channel, 'F1')
#    time.sleep(5)
#    load_defaults(channel)
#    enable_sol(channel)
#    enable_vtd(channel)
#    time.sleep(5)
#    save_exit(channel)

# Load diagnostics
if wait_for(channel, '<F2> Diagnostics', 9999):
    press(channel, 'F2')

    #printDelayedOutput(channel, 10000)

    if wait_for(channel, 'Esc=ExitMemoryTest', 9999):
        press(channel, 'escape')
        if wait_for(channel, 'Starting DSA Preboot', 9999):
            # Now we enter a Linux kernel that does not have a serial terminal set up
            # so we can't do anything further
            time.sleep(90)
            run(channel, 'cmd') # command line interface
            time.sleep(120)
            run(channel, '2') # diagnostics
            time.sleep(3)
            run(channel, '1') # execute diagnostic test
            time.sleep(60)
            run(channel, '46') # run all, hopefully
            time.sleep(3)
            run(channel, '1') # 1 loop

#time.sleep(5)
#while channel.recv_ready():
#    print channel.recv(1024)



#print run(channel, '\x1d' + '(')

#b_info = linesToDict(getOutput(channel))
#c_info = run(channel, "info")

#print "Hostname: %s   Model: %s   FRU: %s   Part: %s   Serial: %s" % \
#(b_info["Hostname"], c_info["Mach type/model"], c_info["FRU no."], c_info["Part no."], c_info["Mach serial number"])

#fmt_str = "%-5s %-14s %-28s %-8s %-20s %-20s %-20s %-14s %-14s %-14s"
#print fmt_str % \
#    ("Slot", "Name", "Mach type/model", "FRU no.", "Mach serial number", "MAC Address 1", "MAC Address 2", "FW/BIOS", "Diagnostics", "Mgmt Processor")
#
#for i in range(1,14+1):
#    cmd = "env -T system:blade[%s]\r\n" % i
#    try:
#        run(channel, cmd)
#        s_info = run(channel, "info")
#        print fmt_str % \
#            (str(i), s_info["Name"], s_info["Mach type/model"], s_info["FRU no."], s_info["Mach serial number"], s_info["MAC Address 1"], s_info["MAC Address 2"], s_info["Build ID"] + " " + s_info["Rev"], s_info["Diagnostics Build ID"] + " " + s_info["Diagnostics Rev"], s_info["Blade Sys Mgmt Processor Build ID"] + " " + s_info["Blade Sys Mgmt Processor Rev"])
#    except:
#        pass


#print run(channel, "exit")
channel.close()
ssh.close()
