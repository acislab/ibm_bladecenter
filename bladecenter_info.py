#!/usr/bin/python

import paramiko
import getpass
import sys
import time

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


def getOutput(channel):
    while not channel.recv_ready():
        time.sleep(1)
        
    txt = ""
    while channel.recv_ready():
            txt += channel.recv(1024)

    return txt


def run(channel, cmd):
    channel.send(cmd + "\r\n")
    return linesToDict(getOutput(channel))


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(host, username='admin', password=pw)
channel = ssh.invoke_shell()

b_info = linesToDict(getOutput(channel))
c_info = run(channel, "info")

print "Hostname: %s   Model: %s   FRU: %s   Part: %s   Serial: %s" % \
(b_info["Hostname"], c_info["Mach type/model"], c_info["FRU no."], c_info["Part no."], c_info["Mach serial number"])

fmt_str = "%-5s %-14s %-28s %-8s %-20s %-20s %-20s %-14s %-14s %-14s"
print fmt_str % \
    ("Slot", "Name", "Mach type/model", "FRU no.", "Mach serial number", "MAC Address 1", "MAC Address 2", "FW/BIOS", "Diagnostics", "Mgmt Processor")

for i in range(1,14+1):
    cmd = "env -T system:blade[%s]\r\n" % i
    try:
        run(channel, cmd)
        s_info = run(channel, "info")
        print fmt_str % \
            (str(i), s_info["Name"], s_info["Mach type/model"], s_info["FRU no."], s_info["Mach serial number"], s_info["MAC Address 1"], s_info["MAC Address 2"], s_info["Build ID"] + " " + s_info["Rev"], s_info["Diagnostics Build ID"] + " " + s_info["Diagnostics Rev"], s_info["Blade Sys Mgmt Processor Build ID"] + " " + s_info["Blade Sys Mgmt Processor Rev"])
    except:
        pass


run(channel, "exit")
channel.close()
ssh.close()
