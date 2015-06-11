import time
import ssh_helper as ssh

# wait for test leaves off the first and last chars because sometimes they 
# split lines

def enable_vtd(chan):
    ssh.press(chan, 'down')
    ssh.press(chan, 'enter')
    ssh.press(chan, 'enter')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'enter')
    ssh.press(chan, 'up')
    ssh.press(chan, 'enter')
    ssh.press(chan, 'escape', 'ystem Setting')
    r = ssh.press(chan, 'escape', 'ystem Configuration and Boot Managemen')
    return r

def load_defaults(chan):
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'enter')
    ssh.wait_for(chan, 'oad Default Setting', 90)
    ssh.press(chan, 'up')
    ssh.press(chan, 'up')
    ssh.press(chan, 'up')
    ssh.press(chan, 'up')
    ssh.press(chan, 'up')
    ssh.press(chan, 'up')
    ssh.press(chan, 'up')
    ssh.press(chan, 'up')
    ssh.press(chan, 'up')

def enable_sol(chan):
    # http://www-01.ibm.com/support/knowledgecenter/SS9H2Y_4.0.1/
    # com.ibm.dp.xi.doc/administratorsguide.xi50171.htm
    # %23webgui_enableserialoverlanforbladeservers_task
    # Move to Console Redirect Settings page
    ssh.press(chan, 'down')
    ssh.press(chan, 'enter')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'enter')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'enter')
    # Enable Remote Console
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'enter')
    ssh.press(chan, 'up')
    ssh.press(chan, 'enter')
    # Set Com 2 settings
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'down')
    ssh.press(chan, 'enter')
    ssh.press(chan, 'up')
    ssh.press(chan, 'enter')
    ssh.press(chan, 'down')
    ssh.press(chan, 'enter')
    ssh.press(chan, 'down')
    ssh.press(chan, 'enter')
    # Back to main page
    ssh.press(chan, 'escape', 'evices and I/O Port')
    ssh.press(chan, 'escape', 'ystem Setting')
    ssh.press(chan, 'escape', 'ystem Configuration and Boot Managemen')

def save_exit(chan):
    ssh.press(chan, 'escape')
    time.sleep(3)
    r = ssh.press(chan, 'yes')
    return r