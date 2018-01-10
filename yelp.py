from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
location = "Vancouver"
province = "BC"
filenamestr = "yelp_check" + location + ".csv"
filename = filenamestr


def getShopName(entries):
	shopnameContainer = entries.findAll("a",{"class":"biz-name js-analytics-click"})
	trimmedName = shopnameContainer[0].text
	print(trimmedName)
	return trimmedName

def getCategory(entries):
	categoryContainer = entries.findAll("span",{"class":"category-str-list"})
	trimmedCategory = categoryContainer[0].a.text.replace(" ","")
	print(trimmedCategory)
	return trimmedCategory
	
def getRating(entries):
	ratingContainer = entries.findAll("div",{"class":"biz-rating biz-rating-large clearfix"})
	trimmedRating = ratingContainer[0].div['title']
	print(trimmedRating)
	return trimmedRating

def getAddress(entries):
	addressContainer = entries.findAll("div",{"class":"secondary-attributes"})
	try:
		address = addressContainer[0].address.text.strip()
		address = address.replace(',', '')
		address = address.replace(location,' '+location)
	except AttributeError:
		address = "NA"
	print(address)
	return address

def getReviewCount(entries):
	numrevContainer = entries.findAll("span",{"class":"review-count rating-qualifier"})
	trimmedNumrev = numrevContainer[0].text.strip()
	trimmedNumrev = trimmedNumrev.replace("reviews","")
	print(trimmedNumrev)
	return(trimmedNumrev)



f = open(filename,"w")
headers = "Shopname, Category, Rating, Address, Num_review\n"
f.write(headers)
f.close()

targeturl = "https://www.yelp.ca/search?find_desc=&find_loc="+ location +"%2C+" + province +"&ns=1"

uClient = uReq(targeturl)
page_html = uClient.read()
uClient.close()

f = open(filename,"a")
page_soup = soup(page_html, "html.parser")

#Scrap first page of Yelp search result
containers = page_soup.findAll("li",{"class":"regular-search-result"})
for entries in containers:
	
	shopname = getShopName(entries)
	category = getCategory(entries)
	rating = getRating(entries)
	address = getAddress(entries)
	numrev = getReviewCount(entries)
	
	
	f.write(shopname +',' + category + ','+ rating + ',' + address + ',' + numrev + ',' + '\n')
f.close()

f = open(filename,"a")

#get first 18 pages of Yelp search result
for k in range(1,18):

	targeturl = "https://www.yelp.ca/search?find_loc="+ location + ",+"  + province + "&start=" + str(10*k) 

	uClient = uReq(targeturl)
	page_html = uClient.read()
	uClient.close()
	
	page_soup = soup(page_html, "html.parser")
	containers = page_soup.findAll("li",{"class":"regular-search-result"})
	
	for entries in containers:
	
		shopname = getShopName(entries)
		category = getCategory(entries)
		rating = getRating(entries)
		address = getAddress(entries)
		numrev = getReviewCount(entries)
	
	
		f.write(shopname +',' + category + ','+ rating + ',' + address + ',' + numrev + ',' + '\n')
	k += 1

f.close()
