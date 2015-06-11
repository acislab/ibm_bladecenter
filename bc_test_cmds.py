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
ssh.run(chan, 'console -o -l')


bios.load_defaults(chan)
bios.enable_sol(chan)
bios.enable_vtd(chan)

chan.close()
sess.close()