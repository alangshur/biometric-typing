import numpy as np
from pynput import keyboard
from pynput import mouse
import datetime
import time

def welcomeUser():
    print("Welcome to Alex, Harry and Ryan's CS221 Project")
    print("Please enter your password (hint, it's \".tie5Roanl\") ")
    print("If you're a bitch, press enter to exit and submit your password so far")

welcomeUser()

rawData = []
startTime = None
endTime = None
shiftModifier = False


#
# General notes on the below code:
# Relies heavily on atomicity of Python list operations.  Operations within list
# indices are not guaranteed to be atomic, but we never modify data here in multiple
# threads - only add to it.
#

def push_down(key):
    global startTime
    global rawData
    global shiftModifier
    
    # potentially exit the listener
    if key == keyboard.Key.enter:
        print("Terminating.")
        endTime = time.time()
        return False
    
    # if alphanumeric, process it as such
    try:
        print("Standard alphanumeric key {} pressed.".format(key.char))
        if startTime == None:
            startTime = time.time()
        rawData.append( (key.char, "DOWN", time.time() - startTime) )
    except AttributeError:
        #print("special key {} pressed".format(key))
        if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            print("EAT MY ASS")
            shiftModifier = True

def release(key):
    global startTime
    global rawData
    global shiftModifier
    
    try:
        print("Standard alphanumeric key {} released.".format(key.char))
        if shiftModifier:
            rawData.append( (rawData[-1][0], "UP", time.time() - startTime) )
            shiftModifier = False
        else:
            rawData.append( (key.char, "UP", time.time() - startTime) )
    except AttributeError:
        pass
        #print("special key {} released".format(key))

def entryClosed(index, opener):
    global rawData
    for newIndex in range(index, len(rawData)):
        potentialCloser = rawData[newIndex]
        if potentialCloser[1] == "DOWN" and potentialCloser[0] == opener[0]:
            return True
    return False


def ensureCompleted():
    global endTime
    global startTime
    global rawData
    for index, opener in enumerate(rawData):
        # if this is already a closing entry, ignore it
        if opener[1] == "UP": continue
        
        # otherwise, check it's closed.  if not, close it at the end time
        if not entryClosed(index, opener):
            rawData.append((opener[0], "UP", endTime - startTime))

with keyboard.Listener(on_press=push_down, on_release=release) as listener:
    listener.join()

print("Done reading input")
endTime = time.time()

# ensure that all entries in the data are closed
ensureCompleted()
#clearRogueDowns()
print(rawData)
