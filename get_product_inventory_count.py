from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

#export PATH=$PATH:/Users/leo/Desktop/selenium


#####################################
#for learning purposes only
#This script automates the task of retrieving an Amazon product listing's inventory data
#Which take advantage of a well known '999 cart tricks' to qualifying sales of a potential competitor.
#By tracking the quantity available of the product over several days or weeks, 
#one can have good idea of how many units your potential competition is selling per day.
#####################################


toCheck = [] #input list of product ASIN 
result = []
num = 1
for ASIN in toCheck:
	
	#launch web browser
	driver = webdriver.Firefox()
	driver.implicitly_wait(30)
	driver.maximize_window()
	
	#go to amazon product page
	driver.get('https://www.amazon.ca/dp/product/' + ASIN + '/')
	print(num)
	num = num + 1
	
	try:
		#add to cart
		addtocartBtn = driver.find_element_by_xpath('//*[@id="add-to-cart-button"]')
		actions = ActionChains(driver)
		actions.click(addtocartBtn).perform()
		print(addtocartBtn)
	
		time.sleep(1)
		
		#view Cart
		viewCart = driver.find_element_by_xpath('//*[@id="hlb-view-cart-announce"]')
		viewCart.click()
		print(viewCart)

		time.sleep(1)
		
		# find quantity box and set Quantity 
		quantity_box = driver.find_element_by_xpath('//*[@id="activeCartViewForm"]/div[2]/div/div[4]/div/div[3]/div/div/span')
		print(quantity_box)
		time.sleep(2)
		quantity_box.click()

		quantity_dropdown = driver.find_element_by_xpath('//*[@id="a-popover-3"]/div/div/ul/li[10]')
		quantity_dropdown.click()
		#actions.click(quantity_dropdown).perform()
	
		time.sleep(2)

		quantity_input = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[4]/div/div[2]/div[4]/form/div[2]/div/div[4]/div/div[3]/div/div/input')
		quantity_input.send_keys('999')
		quantity_input.send_keys(Keys.ENTER)
	
		time.sleep(2)
	
		#get result from quantity box
		text = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[4]/div/div[2]/div[4]/form/div[2]/div/div[4]/div[1]/div/div/div/span').text
		print(text)
		result.append(text)
		time.sleep(1)
	#pass if product is not available
	except NoSuchElementException:
		text = 'NA'
		result.append(text)
		pass
	driver.quit()
	

print(result)

# strip text and get number of inventory
numList=[]
for i in result:
	try:
		tem = i.split('only ')[1]
		final = tem.split(' of')[0]
	except IndexError:
		final = 'NA'
		pass
	numList.append(final)
print(numList)

