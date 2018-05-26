import os, sys, time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from pyvirtualdisplay import Display

MY_MOD_PATH="%s" % os.getcwd()
sys.path.append(MY_MOD_PATH)

from credentials import MyUsername, MyPassword, MyQuestions, MyAnswers

def main():
    #print MyUsername
    #print MyPassword
    #print MyQuestions
    #print MyAnswers

    display = Display(visible=0, size=(1024, 768))
    display.start()

    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = False
    browser = webdriver.Firefox(capabilities=cap, executable_path="C:\\path\\to\\geckodriver.exe")
    browser.maximize_window()
    #browser.implicitly_wait(100)
    browser.get('https://kite.zerodha.com')

    #cap = DesiredCapabilities().FIREFOX
    #cap["marionette"] = False
    #browser = webdriver.Firefox(capabilities=cap)
    ##browser = webdriver.Firefox(capabilities=cap, executable_path="/usr/bin/geckodriver")
    ##browser = webdriver.Firefox(capabilities=cap, executable_path="C:\\path\\to\\geckodriver.exe")
    #browser.maximize_window()
    #browser.get('https://kite.zerodha.com')

    browser.save_screenshot('/home/somasm/GITRepo/PythonTrade/BETA/1.png')

    # Enter Username
    try:
	elem = browser.find_element_by_xpath("//input[@type='text']")
	elem.send_keys(USERNAME)
    except:
	print 'Unable to find username'
	return False
    
    # Enter Password
    try:
	elem = browser.find_element_by_xpath("//input[@type='password']")
	elem.send_keys(PASSWORD + Keys.RETURN)
    except:
	print 'Unable to enter password'
	return False
    
    # Submit first page/form to move on to next password screen
    try:
	elem = browser.find_element_by_xpath("//button[@type='submit']")
	elem.click()
    except:
	print 'Unable to submit the first page/form.'
	return False
    
    # Wait for next page to load
    wait_loop=1
    while True:
	try:
	    elem = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, 'container')))
	    time.sleep(5)
	    browser.save_screenshot('/home/somasm/GITRepo/PythonTrade/BETA/2.png')
	    break
	except:
	    print "Page dint load"
	    if wait_loop > 5:
		break
	    time.sleep(5)
	    wait_loop+=1
    
    # Enter next set of passwords
    all_elements = browser.find_elements_by_xpath("//*[@type='password']")
    for e in all_elements:
	label=e.get_attribute('label')
	print "LABEL=%s" % label
	for twofa in (0, 1, 2, 3, 4):
    	    if questions[twofa] in label:
		print "FOUND: LABEL", label, "QUESITON=", questions[twofa], "ANSWER=", answers[twofa]
		e.send_keys(answers[twofa] + Keys.RETURN)
		break
    
    browser.save_screenshot('/home/somasm/GITRepo/PythonTrade/BETA/3.png')
    
    # Finally submit the 2nd page/form and complete login phase
    try:
	elem = browser.find_element_by_xpath("//button[@type='submit']")
	elem.click()
    except:
	print 'Unable to submit the form.'
	return False
    
    time.sleep(5)
    browser.save_screenshot('/home/somasm/GITRepo/PythonTrade/BETA/4.png')
    
    KiteLink='https://kite.trade/connect/login?api_key=xh7iuhiwsnjwo0mi'
    browser.get(KiteLink)
    print(browser.current_url)
    
    browser.close()
    display.stop()
    browser.quit()

if __name__ == '__main__':
    main()
