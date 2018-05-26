import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024, 768))
display.start()

#browser = webdriver.Firefox(capabilities=cap, executable_path="C:\\path\\to\\geckodriver.exe")
#browser.implicitly_wait(100)
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = False
browser.maximize_window()
browser.get('https://kite.zerodha.com')

#print browser.find_element_by_class_name("login-form")
#print browser.find_element_by_class_name("uppercase su-input-group")

try:
    elem = browser.find_element_by_xpath("//input[@type='text']")
    elem.send_keys(USERNAME)
except:
    print 'Username not found'

try:
    elem = browser.find_element_by_xpath("//input[@type='password']")
    elem.send_keys(PASSWORD + Keys.RETURN)
except:
    print 'Password not found'

try:
    elem = browser.find_element_by_xpath("//button[@type='submit']")
    #elem.send_keys(Keys.RETURN)
    elem.click()
except:
    print 'Unable to submit the form.'

#WebDriverWait(browser, 100)
#WebDriverWait(browser, 100).until(EC.title_contains("Kite at Zerodha - The fast, elegant HTML5 trading platform"))
while True:
    try:
	elem = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, 'container')))
	print "Page is ready!"
	time.sleep(5)
	browser.save_screenshot('/home/somasm/GITRepo/PythonTrade/BETA/1.png')
	break
    except:
	print "Page dint load"
	time.sleep(5)

exit(0)

#delay = 3

print browser.page_source.encode('utf-8')

for twofa in (0, 1, 2, 3, 4):
    try:
	elem = browser.find_element_by_xpath("//div[contains(.,'%s'%questions[twofa])]")
        elem.send_keys(answers[twofa] + Keys.RETURN)
    except:
        print questions[twofa], "not-found"
        continue

browser.close()
display.stop()
browser.quit()
