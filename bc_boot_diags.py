#!/usr/bin/python
import sys
import time
import lib.ssh_helper as ssh
import lib.bios_cmd_hs22 as bios

host = sys.argv[1]
blade = sys.argv[2]

pw = ssh.prompt_password(host)
chan, sess = ssh.get_channel(host, pw)

# Eat the initial welcome text
ssh.get_output(chan)

ssh.run(chan, 'tcpcmdmode -t 3600 -T system:mm[0]')
ssh.run(chan, 'env -T system:blade[' + blade + ']')
# Set the boot sequence to our default
ssh.run(chan, 'bootseq cd usb hd0 nw')
ssh.run(chan, 'power -cycle')
ssh.run(chan, 'console -o -l')

# Enter Diags
if ssh.wait_for(chan, '<F2> Diagnostics', 900):
    ssh.press(chan, 'F2')
    
    if ssh.wait_for(chan, 'Esc=ExitMemoryTest', 900):
        ssh.press(chan, 'escape')
    
chan.close()
sess.close()