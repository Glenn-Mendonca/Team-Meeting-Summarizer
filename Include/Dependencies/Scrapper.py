#imports here
from selenium import webdriver
import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os, time

# INIT load_env function
load_dotenv()

class Scrapper():
    
    # Start Scrapper
    def __init__(self):
        # INIT CHROME OPTIONS
        chrome_options = webdriver.ChromeOptions()

        # SET CHROME OPTIONS
        chrome_options.add_argument("--use-fake-ui-for-media-stream ")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--lang=en')
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument('headless')
        chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36")

        # Specify the path to chromedriver.exe
        self.driver = webdriver.Chrome(
            service = Service('.\Include\Dependencies\chromedriver.exe'),
            options = chrome_options
        )

        # Login Credentials
        self.EMAIL = os.getenv('EMAIL')
        self.PWD = os.getenv('PASSWORD')

        # Driver URL Path
        self.driver.get(r'https://accounts.google.com/signin/v2/identifier?continue='+\
                         'https://meet.google.com'
                        )     

    # Google Login
    def login(self, meet_code):
        self.meetcode = meet_code
        try:
            self.driver.implicitly_wait(15)
            loginBox = self.driver.find_element(By.XPATH,'//*[@id ="identifierId"]')
            loginBox.send_keys(self.EMAIL)
            nextButton = self.driver.find_elements(By.XPATH,'//*[@id ="identifierNext"]')
            nextButton[0].click()
            passWordBox = self.driver.find_element(By.XPATH,'//*[@id ="password"]/div[1]/div / div[1]/input')
            passWordBox.send_keys(self.PWD)
            nextButton = self.driver.find_elements(By.XPATH,'//*[@id ="passwordNext"]')
            nextButton[0].click()
            self.driver.find_element(By.XPATH,'//*[@id="i3"]')
            print('Login Successful...!!')
            return self.meetsetup()
        except NoSuchElementException:
            print('Login Failed')

    # Enter Meet Code
    def meetsetup(self):
        try:
            self.driver.implicitly_wait(15)
            meetcode = self.driver.find_element(By.XPATH,'//*[@id="i3"]')
            meetcode.send_keys(self.meetcode)
            joinButton = self.driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[1]/div[3]/div/div[2]/div[2]/button')
            joinButton.click()
            print("Meet Setup Done...!")
            return self.enterMeet()
        except:
            print("Error in Meet code")

    # Mute mic and stop video stream
    def enterMeet(self, loop=1):
        try:
            self.driver.implicitly_wait(15)
            time.sleep(15)
            muteButton = self.driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[1]/div[1]/div/div[4]/div[1]/div/div/div')
            muteButton.send_keys(Keys.ENTER)
            cameraOff = self.driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[1]/div[1]/div/div[4]/div[2]/div/div')
            cameraOff.send_keys(Keys.ENTER)
            tries = 0
            while(tries<3):
                try:
                    askjoinBtn = self.driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div[1]')
                    askjoinBtn.click()
                    print('Meet Joined...!!')
                    return self.startCaptions()
                except:
                    tries += 1
                    time.sleep(2.5)
            if(loop>0):
                self.driver.refresh()
                print("Trying to Join again")
                self.enterMeet(loop=loop-1)
            else:
                raise NoSuchElementException
        except NoSuchElementException:
            print('Code/ Meet Error')

    # Start Captions
    def startCaptions(self):
        try:
            self.driver.implicitly_wait(30)
            try:
                captions = self.driver.find_element(By.XPATH, '//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[2]/div/div[3]/div/span/button')
                captions.click()
                print("Captions turned on...!!")
                return True
            except:
                pass
            options = self.driver.find_element(By.CSS_SELECTOR,'[aria-label="More options"]')
            options.click()
            time.sleep(1.5)
            captions = self.driver.find_element(By.CSS_SELECTOR,'[jsname="ARMOIc"]')
            captions.click()
            time.sleep(1.5)
            langeng = self.driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/div[3]/div/div[2]/span/div/div/span/label[2]/div[1]')
            langeng.click()
            apply = self.driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div/div[2]/div')
            apply.click()
            print("Captions turned on...!!")
            return True
        except NoSuchElementException:
            print("Didn't Admit/ Captions didn't start")
            return False

    # Scrape Captions
    def extractcaptions(self, senddata):
        speaker, generated_transcript = "", ""
        try:
            div = self.driver.execute_script('var div = document.querySelector("#ow3 > div.T4LgNb > div > div:nth-child(9) > div.crqnQb > div.a4cQT > div:nth-child(1) > div:nth-child(1) > div");if (div.parentNode.hasChildNodes()) {html = div.innerHTML;div.parentNode.removeChild(div); return html;} else return "NULL";')
            if(div == "NULL"):
                raise NoSuchElementException
            soup = BeautifulSoup(div,features="html.parser")                     
            speaker = soup.div.contents[0]
            captions = [a.contents[0] for a in soup.findAll('span', {"class":"CNusmb"})]
            for caps in captions:
                generated_transcript += caps + " "
            senddata({'Speaker':speaker, 'Transcript':generated_transcript})
        except:
            senddata({'Speaker':"", 'Transcript':""})
        

        