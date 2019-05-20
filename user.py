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

index = 0

def push_down(key):
    global previousKey
    global currentKeyInfo
    global sparse_vector
    global index
    # filter out auxillary key presses (shift, capslock, etc.)
    try:
        print('Standard alphanumeric key {0} pressed'.format(key.char))
        currentKeyDepressedTime = time.time()
        #print(previousKey)
        if previousKey != (None, None, None):
            # this is not the first key press - generate data that relies on prev
            print("not first key")
            # what do we need to configure given that this is not the first key?
        else:
            print("First key pressed")
            # only add a vector representing itself
        # generate data that is just reliant on this key presed
        
        currentKeyInfo = (key.char, time.time())
        index += 1

    except AttributeError: print('special key {0} pressed'.format(key))

def release(key):
    global previousKey
    global currentKeyInfo
    global sparse_vector
    global index
    
    # potentially stop the listening program
    if key == keyboard.Key.esc:
        print("Terminating.")
        return False
    
    # ensuring that the character input was alphanumeric
    try:
        if key.char == currentKeyInfo[0]:
            timing = time.time() - currentKeyInfo[1]
            print(' released after {1} seconds'.format(key.char, timing))
            
            # add the sparse vector for 'H'
            sparse_vector[(None, key.char, 'H', index, round(timing, 2))] = 1
            print(sparse_vector)

    except AttributeError: print('special key {0} released'.format(key))

with keyboard.Listener(on_press=push_down, on_release=release) as listener:
    listener.join()

print("Done reading input")
