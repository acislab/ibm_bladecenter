import time
import ssh_helper as ssh

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
    ssh.press(chan, 'escape')
    ssh.press(chan, 'escape')
    # One extra escape, seems to be a timing bug somewhere
    # wait_for would be better but the ANSI stripper seems not 
    # quite right and this screen messes it up
    r = ssh.press(chan, 'escape')
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
    ssh.wait_for(chan, 'Load Default Settings', 90)
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
    time.sleep(3)
    ssh.press(chan, 'escape')
    time.sleep(3)
    ssh.press(chan, 'escape')
    time.sleep(3)
    ssh.press(chan, 'escape')

def save_exit(chan):
    ssh.press(chan, 'escape')
    time.sleep(3)
    r = ssh.press(chan, 'yes')
    return r