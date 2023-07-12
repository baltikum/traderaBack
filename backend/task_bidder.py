
from selenium.webdriver.common.by import By
import time, os
from datetime import timedelta
from selenium.common.exceptions import NoSuchElementException

#TIMES
BID_GAP_SECONDS = 1.0
LOAD_TIME = 0.5
#URLS
LOGIN_URL = "https://www.tradera.com/login?returnUrl=%2F&login-modal=true"
BASE_ITEM_URL = "https://www.tradera.com/item/"
#CREDENTIALS
USERNAME = os.environ['TRAD_USER']
PASSWORD = os.environ['TRAD_PASS']
#XPATHS
ACCEPT_COOCKIES_XPATH = 'html/body/div[1]/div/div/div/div[2]/div/button[2]'
USERNAME_XPATH = "//*[@id=\"login-box-mail\"]"
PASSWORD_XPATH = "//*[@id=\"login-box-password\"]"
LOGIN_BUTTON_XPATH ="/html/body/div[1]/div/div/div/div[1]/div[1]/div[2]/form/div[1]/div[2]/button"
BID_BUTTON_XPATH = "/html/body/div[1]/div/div[3]/div[2]/div/div[4]/div/aside/div[1]/section[2]/form/button"
AMMOUNT_XPATH ="/html/body/div[6]/div/div[3]/section[2]/form/div/input"
PLACE_BID_XPATH = "/html/body/div[6]/div/div[3]/section[2]/form/button"
ENDS_IN_XPATH = "/html/body/div[6]/div/div[3]/section[1]/div[2]/div[2]/p/span"
  
#Login and accept coockies. 
def login_function(browser):
	global LOAD_TIME,LOGIN_URL,ACCEPT_COOCKIES_XPATH, \
 			USERNAME_XPATH,PASSWORD_XPATH,USERNAME,PASSWORD, \
   			LOGIN_BUTTON_XPATH
	try:
		#LOAD LOGIN PAGE
		browser.get(LOGIN_URL)
		time.sleep(LOAD_TIME)

		#ACCEPT COOCKIES
		button = browser.find_element(By.XPATH,ACCEPT_COOCKIES_XPATH)
		button.click()

		#LOGIN
		uname = browser.find_element(By.XPATH, USERNAME_XPATH)
		passw = browser.find_element(By.XPATH, PASSWORD_XPATH)
		uname.send_keys(USERNAME)
		passw.send_keys(PASSWORD)
		login_button = browser.find_element(By.XPATH,LOGIN_BUTTON_XPATH)
		login_button.click()
		time.sleep(LOAD_TIME)
		return True
		
	except NoSuchElementException as e :
		print(e)
	except Exception as e :
		print(e)
	return False
#Load an itempage
def load_item(browser, item):
	global LOAD_TIME,BASE_ITEM_URL
	item_url = BASE_ITEM_URL + str(item)
	browser.get(item_url)
	time.sleep(LOAD_TIME)
#Place a bid, returns True or False	
def bid_function(browser, item, bid):
	global LOAD_TIME,BID_BUTTON_XPATH,AMMOUNT_XPATH,PLACE_BID_XPATH, ENDS_IN_XPATH, BID_GAP_SECONDS
	load_item(browser,item)
	print( 'Bidding ' + str(bid) + ' at item ' + str(item) )

	#BIDDING
	bid_button = browser.find_element(By.XPATH, BID_BUTTON_XPATH)
	bid_button.click()
	time.sleep(LOAD_TIME)
	ends_in = browser.find_element(By.XPATH, ENDS_IN_XPATH)
	split_time_parts = ends_in.text.split()
	print("tid kvar är" + int(split_time_parts[0]))
 
	if len(split_time_parts) == 2 and int(split_time_parts[0]) < 15:
		print( 'tid mindre än 15 sekunder och i 2 delar.')
		countdown = timedelta(seconds=split_time_parts[0])
		time.sleep((countdown.total_seconds()-BID_GAP_SECONDS))
		ammount_path = browser.find_element(By.XPATH, AMMOUNT_XPATH)
		ammount_path.send_keys(bid)
		bid_button = browser.find_element(By.XPATH, PLACE_BID_XPATH)
		ends_in = browser.find_element(By.XPATH, ENDS_IN_XPATH)
		split_time_parts = ends_in.text.split()
		print('button click klockan är '+ split_time_parts[0])
		#bid_button.click()
		return True
	else:
		return False


