#                                           ___   ___
#     //   / /                                / /                                    //  ) )
#    //   / /  ___      ___      __          / /      __   __  ___  ___      __   __//__  ___      ___      ___
#   //   / / ((   ) ) //___) ) //  ) )      / /    //   ) ) / /   //___) ) //  ) ) //   //   ) ) //   ) ) //___) )
#  //   / /   \ \    //       //           / /    //   / / / /   //       //      //   //   / / //       //
# ((___/ / //   ) ) ((____   //         __/ /___ //   / / / /   ((____   //      //   ((___( ( ((____   ((____

# don't uncomment unless you're Ryan and cannot care for your computer properly
# import sys
# sys.path.append('/usr/local/lib/python3.7/site-packages')

import numpy as np
from pynput import keyboard
from pynput import mouse
import datetime
import time
from data import data
import os
import sys

# global constants (required for weird multithreading that pynput seems to rely upon)
rawData = []
startTime = None
endTime = None
shiftModifier = False
numKeyPresses = 0
counter = 0
actualPassword = ".tie5Roanl"

#
# General notes on the below code:
# Relies heavily on atomicity of Python list operations.  Operations within list
# indices are not guaranteed to be atomic, but we never modify data here in multiple
# threads - only add to it.
#

# Welcome the user to the program
def welcomeUser():
    print("Welcome to Alex, Harry and Ryan's CS221 Project.")
    print("We will now gather your biometric data - strap in, you're going to need a few minutes!")
    print("Please enter your password (hint, it's \".tie5Roanl\" - for now!)")
    print("Press enter to submit your password entry.")

# Intercept keyboard events using pynput handler, perform basic error checking and update global data repo
def push_down(key):
    global startTime
    global rawData
    global shiftModifier
    global numKeyPresses
    global counter
    
    # potentially exit the listener
    if key == keyboard.Key.enter:
        #print("Terminating.")
        endTime = time.time()
        #counter += 1
        numKeyPresses = 0
        #print("Thank you.  Now, please re-enter the password (iteration {} of 40)".format(counter))
        return False
    
    # if alphanumeric, process it as such
    try:
        #print("Standard alphanumeric key {} pressed.".format(key.char))
        if startTime == None:
            startTime = time.time()
        rawData.append( (key.char, "DOWN", time.time() - startTime) )
        numKeyPresses += 1
        print("\r" + "*" * numKeyPresses, end ="")
    except AttributeError:
        #print("special key {} pressed".format(key))
        if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            shiftModifier = True

def release(key):
    global startTime
    global rawData
    global shiftModifier
    
    try:
        #print("Standard alphanumeric key {} released.".format(key.char))
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

def findPrevious(key):
    global rawData
    first = True
    for entry in rawData[::-1]:
        if first:
            first = False
            continue
        if entry[0] == key and entry[1] == "DOWN": return entry
        if entry[0] == key and entry[1] == "UP": return None
    return None

def findPreviousFromIndex(key, index):
    global rawData
    first = True
    index -= 1
    while index >= 0:
        entry = rawData[index]
        if entry[0] == key and entry[1] == "DOWN": return entry
        if entry[0] == key and entry[1] == "UP": return None
        index -=1
    return None

def clearRogueUps():
    global rawData
    if rawData[-1][1] == "UP":
        data = findPrevious(rawData[-1][0])
        if data == None or data[1] == "UP":
            del rawData[-1]
    
    index = 0
    while True:
        if index == len(rawData): break
        entry = rawData[index]
        if entry[1] == "UP":
            data = findPreviousFromIndex(entry[0], index)
            if data == None or data[1] == "UP":
                del rawData[index]
                continue
        index += 1

def passwordProperlyEntered():
    global rawData
    global actualPassword
    
    buildString = ""

    for entry in rawData:
        if entry[1] == "DOWN":
            buildString += entry[0]

    return buildString == actualPassword

def welcomeUserAndCollectUserPasswordData(numPasswordsNeeded):
    global rawData
    global endTime
    global startTime
    global shiftModifier
    global numKeyPresses
    global counter
    
    welcomeUser()
    
    totalData = []

    i = 0
    while i < numPasswordsNeeded:
        
        with keyboard.Listener(on_press=push_down, on_release=release) as listener:
            listener.join()

        # ensure that all entries in the data are closed
        ensureCompleted()
        clearRogueUps()
        print()
        #print(rawData)
        
        # clear the global variables again
        
        startTime = None
        endTime = None
        shiftModifier = False
        numKeyPresses = 0
        counter = 0
        
        if passwordProperlyEntered():
            totalData.append(rawData)
            print("Fantastic, now enter the password again!  (Trial {} of {}).".format(i + 1, numPasswordsNeeded))
            i += 1
        else:
            print("Password mis-entered.  Try again:")
        rawData = []

    print("Great - we've finished gathering training data from you.  Please wait while we process this information")
    print(totalData)
    return totalData

print("And now: the unholy union of Ryan and Harry's work...")
userData = welcomeUserAndCollectUserPasswordData(3)
featureVectors = []
for attempt in userData:
    features = data.getFeaturesFromList(attempt)
    featureVectors.append(features)
print(featureVectors)
