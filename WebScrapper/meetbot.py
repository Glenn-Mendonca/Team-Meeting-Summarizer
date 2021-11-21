#imports here
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

# INIT CHROME OPTIONS
chrome_options = Options()
# 0 - Default, 1 - Allow, 2 - Block

# SET CHROME OPTIONS
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument('headless')

#specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome(
    executable_path='D:\Git_Repos\Team_Meetings_Summarizer\WebScrapper\chromedriver.exe',
    options=chrome_options
)

#open the webpage
driver.get("https://meet.google.com")
driver.find_element_by_xpath('/html/body/header/div[1]/div/div[3]/div[1]/div/span[1]/a').click()
email = driver.find_element_by_xpath('//*[@id="identifierId"]')
email.send_keys('se.meetingsummarizer@gmail.com')
driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button').click()
time.sleep(2.5)
pwd = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
pwd.send_keys('meeting@9272')
driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()
time.sleep(2.5)
meetcode = driver.find_element_by_xpath('//*[@id="i3"]')
meetcode.send_keys('njr-tmpq-gzc')
time.sleep(2.5)
driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[1]/div[3]/div/div[2]/div[2]/button').click()
time.sleep(2.5)
driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[1]/div[1]/div/div[4]/div[1]/div/div/div').click()
driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[1]/div[1]/div/div[4]/div[2]/div/div').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div[1]').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[2]/div/div[6]/div/div[3]/div[1]/span/button').click()
time.sleep(2.5)
driver.find_element_by_xpath('/html/body/div[3]/ul/li[5]').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/span/div/div/span/label[2]/div[1]/div/div[3]').click()
driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div/div[2]/div').click()
try:
    while True:
        captions = driver.find_elements_by_class_name('CNusmb')    
        for caps in captions:
            print(caps.text)
except:
        pass