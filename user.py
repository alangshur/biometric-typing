import numpy as np
from pynput import keyboard
from pynput import mouse
import datetime
import time

def welcomeUser():
    print("Welcome to Alex, Harry and Ryan's CS221 Project")
    print("Please enter your password (hint, it's \".tie5Roanl\") ")
    print("If you're a bitch, press esc to exit")

welcomeUser()

# create the sparse vector to be populated
sparse_vector = {}
#          what key | time pressed down  | time released (if it exists)
#               v      v                      v
previousKey = (None, None,                  None)

#            what key | time pressed down
#                  v      v
currentKeyInfo = (None, None)

def push_down(key):
    global previousKey
    global currentKeyInfo
    global sparse_vector
    # filter out auxillary key presses (shift, capslock, etc.)
    try:
        print('Standard alphanumeric key {0} pressed'.format(key.char))
        currentKeyDepressedTime = time.time()
        print(previousKey)
        if previousKey != (None, None, None):
            # this is not the first key press - generate data that relies on prev
            print("    not first key")
        # generate data that is just reliant on this key press
        print("Updating this bad boy")
        
        currentKeyInfo = (key.char, time.time())
        
    except AttributeError: print('special key {0} pressed'.format(key))

def release(key):
    global previousKey
    global currentKeyInfo
    global sparse_vector
    print("")
    print("")
    print("")
    print("")
    if key == keyboard.Key.esc:
        print("Terminating.")
        # Stop listener
        return False
    print(currentKeyInfo)
    if currentKeyInfo[1] != None:
        print('{0} released after {1} seconds'.format(key.char, time.time() - currentKeyInfo[1]))

with keyboard.Listener(on_press=push_down, on_release=release) as listener:
    listener.join()
