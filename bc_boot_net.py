#!/usr/bin/python
import sys
import lib.ssh_helper as ssh

host = sys.argv[1]
blade = sys.argv[2]

pw = ssh.prompt_password(host)
chan, sess = ssh.get_channel(host, pw)

# Eat the initial welcome text
ssh.get_output(chan)

ssh.run(chan, 'tcpcmdmode -t 3600 -T system:mm[0]')
ssh.run(chan, 'env -T system:blade[' + blade + ']')
ssh.run(chan, 'bootseq legacy nw')
ssh.run(chan, 'power -cycle')

chan.close()
sess.close()
