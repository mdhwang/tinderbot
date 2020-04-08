from selenium import webdriver
# from login_info import username, password
import sys
sys.path.append('/Users/AaronLee/Documents/GitHub/creds')
from login_info import username, password
from time import sleep

class BumbleBot():
    def __init__(self):
        self.driver = webdriver.Chrome('/Users/AaronLee/Documents/GitHub/chromedriver')

    def login(self):       
        
        self.driver.get('https://bumble.com')
        
        signin_btn = self.driver.find_element_by_xpath('//*[@id="page"]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]/a')
        signin_btn.click()

        sleep(8)

        fb_btn = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/div[2]/main/div/div[2]/form/div[1]/div')
        fb_btn.click()                              

        # switch to login popup
        base_window = self.driver.window_handles[0]
        popup = self.driver.window_handles[1]
        self.driver.switch_to.window(popup)

        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(username)

        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        login_btn.click() 

        # switch to original window
        self.driver.switch_to.window(base_window)

    def like(self):
        try:
            like_btn = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div/div[3]/div/span/span')
            like_btn.click()
        except Exception:
            like_btn = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div/div[2]/div/span/span')
            like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div/div[1]/div/span/span')
        dislike_btn.click()

    def boom_popup(self):
        boom_popup = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/main/div[2]/article/div/footer/div/div[2]/div/span/span/span')
        boom_popup.click()

    def auto_swipe(self):
        count = 0
        matches = 0
        # while count != 100:
        while True:
            sleep(1)
            try:
                self.like()
                count += 1
                print ('Like Counter: {} |  Match Counter: {}'.format(count, matches))
            except Exception:
                try:
                    self.boom_popup()
                    matches += 1
                    print ('---> Match Counter: {} <---'.format(matches))
                except Exception:
                    pass

    def send_message(self, id):
        icon_btn = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/aside[1]/div/div[3]/div/div/section[1]/div/section/section/div[1]/ul/li[{}]/div/div'.format(id))
        icon_btn.click()

        message_in = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/main/div[3]/div/div[1]/div/div/textarea[1]')
        message_in.send_keys('Hi, my name is Aaron and I am looking for job opportunities in the area of data science, data analyst, business analyst, etc. I have experience in SQL, Python, Statistics, and Data Visualizations. Hoping to hear from you soon!')
        
        send_btn = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/main/div[3]/div/div[3]/div/span/span/span')
        send_btn.click()

bot = BumbleBot()
bot.login()
sleep(4)
# bot.auto_swipe()

//*[@id="main"]/div/div[1]/aside/div/div[3]/div/div/section[1]/div/section/section/div[1]/ul/li[2]/div/div
//*[@id="main"]/div/div[1]/aside[1]/div/div[3]/div/div/section[1]/div/section/section/div[1]/ul/li[3]/div/div
//*[@id="main"]/div/div[1]/aside[1]/div/div[3]/div/div/section[1]/div/section/section/div[1]/ul/li[4]/div/div