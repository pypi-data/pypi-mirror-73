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
    from selenium.webdriver.common.keys import Keys
    #from selenium.webdriver.support.ui import Select
    seleniumAvailable = True
except ImportError:
    pass


if seleniumAvailable:
    def clickInputValue(driver,inputType,valueToSelect,delay=10,elementnumber=-1,debug=False):
        numTries = 1
        elemToClick = None
        cssToSelect = 'input[type="{}"][value="{}"]'.format(inputType,valueToSelect)
        if debug: print("    (0): locating {} ...".format(cssToSelect))
        while (elemToClick is None) and (numTries < delay):
            try:
                if elementnumber >= 0:
                    elemToClick = driver.find_elements_by_css_selector(cssToSelect)[elementnumber]
                else:
                    elemToClick = driver.find_element_by_css_selector(cssToSelect)
            except Exception as exp:
                print (exp)
                if isinstance(exp, selenium.common.exceptions.NoSuchElementException):
                    if debug: print("    ({}) locating {} ...".format(numTries,cssToSelect))
                elif isinstance(exp, selenium.common.exceptions.ElementNotInteractableException):
                    if debug: print("    ({}) locating {} ...".format(numTries,cssToSelect))
                else:
                    if debug: print(exp)
                    break
            finally:
                numTries += 1
                time.sleep(0.5)
        if elemToClick is None:
            if debug: print("    (x): could not locate css={}".format(cssToSelect))
            return False
        elemToClick.click()
        if debug: print("    (✓): selected on {}".format(valueToSelect))
        return True

else:
    def clickInputValue(driver,valueToSelect,delay=10,elementnumber=-1,debug=False):
        if debug: print("ERROR: no module 'selenium' - 'enterValueToName()' is not available")
        return False
