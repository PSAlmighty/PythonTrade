import os, sys, time
import urllib2, re

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from pyvirtualdisplay import Display

MY_MOD_PATH="%s" % os.getcwd()
sys.path.append(MY_MOD_PATH)

from credentials import MyUsername, MyPassword, MyQuestions, MyAnswers

from pprint import pprint

def main():
    #print MyUsername
    #print MyPassword
    #print MyQuestions
    #print MyAnswers

    display = Display(visible=0, size=(1024, 768))
    display.start()

    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    browser = webdriver.Chrome(chrome_options=chrome_options)

    #browser = webdriver.Chrome()
    browser.set_page_load_timeout(10)
    browser.get('https://kite.zerodha.com')

    time.sleep(2)

    browser.save_screenshot('/home/somasm/GITRepo/PythonTrade/BETA/1.png')

    # Enter Username
    try:
	elem = browser.find_element_by_xpath("//input[@type='text']")
	elem.send_keys(MyUsername)
	print 'Usernme entered'
    except:
	print 'Unable to find username'
	return ''

    # Enter Password
    try:
	elem = browser.find_element_by_xpath("//input[@type='password']")
	elem.send_keys(MyPassword)
	print 'Password entered'
    except:
	print 'Unable to enter password'
	return ''
    
    # Submit first page/form to move on to next password screen
    try:
	elem = browser.find_element_by_xpath("//button[@type='submit']")
	elem.click()
	print 'First form submitted'
    except:
	print 'Unable to submit the first page/form.'
	return ''
    
    # Wait for next page to load
    wait_loop=1
    while True:
	try:
	    elem = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, 'container')))
	    time.sleep(2)
	    browser.save_screenshot('/home/somasm/GITRepo/PythonTrade/BETA/2.png')
	    break
	except:
	    print "Page dint load"
	    if wait_loop > 5:
		break
	    time.sleep(2)
	    wait_loop+=1
    
    # Enter next set of passwords
    all_elements = browser.find_elements_by_xpath("//*[@type='password']")
    for e in all_elements:
	label=e.get_attribute('label')
	print "LABEL=%s" % label
	for twofa in (0, 1, 2, 3, 4):
    	    if MyQuestions[twofa] in label:
		#print "FOUND: LABEL", label, "QUESITON=", MyQuestions[twofa], "ANSWER=", MyAnswers[twofa]
		e.send_keys(MyAnswers[twofa])
		print 'Password entered'
		break
    
    browser.save_screenshot('/home/somasm/GITRepo/PythonTrade/BETA/3.png')
    
    # Finally submit the 2nd page/form and complete login phase
    try:
	elem = browser.find_element_by_xpath("//button[@type='submit']")
	elem.click()
	print '2nd form submitted'
    except:
	print 'Unable to submit the form.'
	return ''
    
    time.sleep(3)
    #browser.save_screenshot('/home/somasm/GITRepo/PythonTrade/BETA/4.png')
    
    KiteLink='https://kite.trade/connect/login?api_key=xh7iuhiwsnjwo0mi'
    browser.set_page_load_timeout(2)
    rurl = ''
    browser.get(KiteLink)
    #browser.execute_script("window.open('%s');" % KiteLink)
    wait = WebDriverWait(browser, 10)
    wait.until(lambda browser: browser.current_url != KiteLink)
    rurl = browser.current_url
    print rurl
    #browser.save_screenshot('/home/somasm/GITRepo/PythonTrade/BETA/5.png')

    token=''
    m = re.search('.*request_token=([^&]*)&.*', rurl)
    if m:
	print m.group(1)
	token=m.group(1)

    browser.close()
    display.stop()
    browser.quit()

    return token

if __name__ == '__main__':
    main()
