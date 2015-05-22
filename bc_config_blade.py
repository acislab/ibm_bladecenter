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

# Set BIOS options
if ssh.wait_for(chan, '<F1> Setup', 900):
    ssh.press(chan, 'F1')
    time.sleep(5)
    bios.load_defaults(chan)
    bios.enable_sol(chan)
    bios.enable_vtd(chan)
    time.sleep(5)
    bios.save_exit(chan)
    time.sleep(15)
    # Power off when done
    ssh.run(chan, 'power -off')

chan.close()
sess.close()