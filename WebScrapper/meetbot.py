#imports here
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os, time, sys

# INIT CHROME OPTIONS
chrome_options = Options()

# INIT load_env function
load_dotenv()

# SET CHROME OPTIONS
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('headless')

chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
'''
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
'''
# Specify the path to chromedriver.exe
driver = webdriver.Chrome(
    service = Service('D:\Git_Repos\Team_Meetings_Summarizer\WebScrapper\chromedriver.exe'),
    options = chrome_options
)

driver.get(r'https://accounts.google.com/signin/v2/identifier?continue='+\
        'https://meet.google.com')  

EMAIL = os.getenv('EMAIL')
PWD = os.getenv('PASSWORD')

# Google Login
def login(gmailId, passWord):
    try:
        driver.implicitly_wait(15)
        loginBox = driver.find_element(By.XPATH,'//*[@id ="identifierId"]')
        loginBox.send_keys(gmailId)
        nextButton = driver.find_elements(By.XPATH,'//*[@id ="identifierNext"]')
        nextButton[0].click()
        passWordBox = driver.find_element(By.XPATH,'//*[@id ="password"]/div[1]/div / div[1]/input')
        passWordBox.send_keys(passWord)
        nextButton = driver.find_elements(By.XPATH,'//*[@id ="passwordNext"]')
        nextButton[0].click()
        driver.find_element(By.XPATH,'//*[@id="i3"]')
        print('Login Successful...!!')
        return True
    except NoSuchElementException:
        print('Login Failed')
        return False

# Enter Meet Code
def meetsetup(code):
    try:
        driver.implicitly_wait(15)
        meetcode = driver.find_element(By.XPATH,'//*[@id="i3"]')
        meetcode.send_keys(code)
        joinButton = driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[1]/div[3]/div/div[2]/div[2]/button')
        joinButton.click()
        driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[1]/div[1]/div/div[4]/div[1]/div/div/div')
        print("Meet Setup Done...!")
        return True
    except:
        print("Error in Meet code")
        return False

# Mute mic and stop video stream
def enterMeet(loop = 1):
    try:
        driver.implicitly_wait(15)
        muteButton = driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[1]/div[1]/div/div[4]/div[1]/div/div/div')
        muteButton.click()
        cameraOff = driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[1]/div[1]/div/div[4]/div[2]/div/div')
        cameraOff.click()
        tries = 0
        while(tries<3):
            try:
                askjoinBtn = driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div[1]')
                askjoinBtn.click()
                print('Meet Joined...!!')
                return True
            except:
                tries += 1
                time.sleep(2.5)
        if(loop>0):
            driver.refresh()
            print("Trying to Join again")
            return enterMeet(loop=loop-1)
        else:
            raise NoSuchElementException
    except NoSuchElementException:
        print('Code/ Meet Error')
        return False

# Start Captions
def startCaptions():
    try:
        driver.implicitly_wait(30)
        options = driver.find_element(By.CSS_SELECTOR,'[jsname="NakZHc"]')#By.XPATH,'//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[2]/div/div[6]/div/div[3]/div[1]/span/button')
        options.click()
        time.sleep(1.5)
        captions = driver.find_element(By.CSS_SELECTOR,'[jsname="ARMOIc"]')#By.XPATH,'/html/body/div[3]/ul/li[5]')
        captions.click()
        time.sleep(1.5)
        #langeng = driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/div[3]/div/div[2]/span/div/div/span/label[2]/div[1]/div/div[3]')
        langeng = driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/div[3]/div/div[2]/span/div/div/span/label[2]/div[1]')
        langeng.click()
        apply = driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div/div[2]/div')
        apply.click()
        print("Captions turned on...!!")
        time.sleep(5)
        driver.get_screenshot_as_file("screenshot.png")
        return True
    except NoSuchElementException:
        print("Didn't Admit/ Captions didn't start")
        return False

# Scrape Captions
def extractcaptions():
    running = True
    conversation, speaker = "", ""
    while running:
        try:
            driver.find_element(By.CSS_SELECTOR,'[jsname="NeC6gb"]')
        except NoSuchElementException:
            running = False
        try:
            #div = (driver.find_element(By.XPATH,'//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[7]/div[1]')).get_attribute('innerHTML')
            div = (driver.find_element(By.CSS_SELECTOR,'[class="TBMuR bj4p3b"]')).get_attribute('innerHTML')
            driver.execute_script(
                'console.log("Trying to remove Div");var div = document.querySelector("#ow3 > div.T4LgNb > div > div:nth-child(9) > div.crqnQb > div.a4cQT > div:nth-child(1)");if (div.parentNode.hasChildNodes()) {div.parentNode.removeChild(div);console.log("Div removed");} else console.log("No div found");'
            )
            soup = BeautifulSoup(div,features="html.parser")                     
            temp_speaker = soup.div.contents[0]
            captions = [a.contents[0] for a in soup.findAll('span', {"class":"CNusmb"})]
            if(temp_speaker!=speaker):
                conversation += "\n"+temp_speaker+":\n"
                speaker = temp_speaker
            for caps in captions:
                conversation += caps + " "
            time.sleep(2)
        except:
            #print(sys.exc_info()[0])
            pass
    print(conversation)
    


#open the webpage
if(login(EMAIL,PWD)):
    if(meetsetup('ywb-cghb-mss')):#'ywb-cghb-mss'
        if(enterMeet()):
            if(startCaptions()):
                extractcaptions()
