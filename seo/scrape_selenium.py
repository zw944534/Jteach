from selenium import webdriver
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from lxml import html
import time
import io

driverPathFirefox=r'C:\\users\chu\Documents\for nku\paper\python'
driverPathGoogle=r'C:\\users\chu\Documents\for nku\paper\python\webdriver\chromedriver.exe'

driver = webdriver.Chrome(driverPathGoogle)

driver.get("http://mhdb.mh.sinica.edu.tw/mhpeople/index.php")
def tryclick(driver,selector,count=0):
    try:
        elem = driver.find_element_by_css_selector(selector)
        elem.click()
    except:
        time.sleep(2)
        count+=1
        if(count<2):
            tryclick(driver,selector,count)
        else:
            print("cannot locate element"+selector)
            
def isElementExist(driver,element):
    flag=True
    try:
        driver.find_element_by_css_selector(element)
        return flag
    except:
        flag=False
        return flag

testURL=""
nameFile = open(r'C:/Users/chu/Documents/for nku/paper/python/name.txt',encoding='utf-8')
nameArray = []
for line in nameFile:
    nameArray.append(line)
nameFile.close

i=0           
while(i<len(nameArray)):
    driver.find_element_by_id("inputPeopleName").send_keys(nameArray[i].strip())
    tryclick(driver,"#inputPeopleNameBtn")
    time.sleep(3)
    testURL= urlparse(driver.current_url).geturl().split("&",1)
#     print(testURL[1])
    if( isElementExist(driver,".toNext") and testURL[1] == "searchType=1"):
        print("in if")
        driver.find_element_by_class_name("toNext").click()
        time.sleep(2)
    if(i==0):
        tryclick(driver,".readmoreLink")
        driver.find_element_by_class_name("tmpUsername").send_keys("username")
        driver.find_element_by_class_name("tmpPassword").send_keys("password")
        driver.find_element_by_class_name("tmpSbumit").click()
        
    
    time.sleep(3)
    html=driver.page_source
#     print("============================")
    fp = io.open("C:/Users/chu/Documents/for nku/paper/python/textDataHtml/"+nameArray[i].strip()+"_html.txt","ab+")
    fp.write(html.encode('utf-8'))
    fp.close()
    
#     soup = BeautifulSoup(html,'html.parser')
#     selectData = ".basicData"
#     print(soup.select(selectData))
    driver.find_element_by_id("inputPeopleName").clear()
    i=i+1
driver.close()        