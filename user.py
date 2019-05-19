#import pynput
import numpy as np
from pynput import keyboard
from pynput import mouse

def welcomeUser():
    print("Welcome to Alex, Harry and Ryan's CS221 Project")
    print("Please enter your password (hint, it's \".tie5Roan1\") ")

def push_down(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def release(key):
    if key == keyboard.Key.esc:
        # Terminating.
        # Stop listener
        return False
    print('{0} released'.format(
        key))

welcomeUser()
with keyboard.Listener(on_press=push_down, on_release=release) as listener:
    listener.join()

#listener = mouse.Listener(on_press=on_press, on_release=on_release)
#listener.start()
