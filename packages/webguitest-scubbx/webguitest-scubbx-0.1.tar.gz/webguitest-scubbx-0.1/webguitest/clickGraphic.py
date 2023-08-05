#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
pyautoguiAvailable = False
seleniumAvailable = False

try:
    import pyautogui
    pyautoguiAvailable = True
except ImportError:
    pass

try:
    import selenium
    seleniumAvailable = True
except ImportError:
    pass

if pyautoguiAvailable:
    def clickGraphic(imagepath,delay=10,confidence=1,waitbetweentries=1,doubleclick=False,grayscale=False,debug=False):
        elemToClick = None
        numTries = 1
        if debug: print("    (0): locating {} ...".format(imagepath))
        while (elemToClick is None) and (numTries < delay):
            try:
                elemToClick = pyautogui.locateOnScreen(imagepath,confidence,grayscale=grayscale)
            except Exception as exp:
                if isinstance(exp, pyautogui.pyscreeze.ImageNotFoundException):
                    if debug: print("    ({}): locating {} ...".format(numTries,imagepath))
                else:
                    if debug: print(exp)
                    break
            finally:
                numTries += 1
                time.sleep(waitbetweentries)
        if elemToClick is None:
            if debug: print("    (x): could not locate image {}".format(imagepath))
            return False
        time.sleep(0.1)
        if doubleclick:
            pyautogui.doubleClick(pyautogui.center(elemToClick))
        else:
            pyautogui.click(pyautogui.center(elemToClick))
        if debug: print("    (✓): clicked {}".format(elemToClick))
        time.sleep(0.4)
        return True
else:
    def clickGraphic(imagepath,delay=10,confidence=1,waitbetweentries=1,doubleclick=False,grayscale=False,debug=False):
        if debug: print("ERROR: no module 'pyautogui' - 'clickGraphic()' is not available")
        if debug: print("       maybe you missed to also install the 'Xlib' library on which pyautogui depends on")
        return False
