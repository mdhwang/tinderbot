from selenium import webdriver
import sys
sys.path.insert(1,'/Users/mattd/Documents/Resources')
from login import user, passw
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome('/Users/mattd/Documents/Resources/chromedriver')

    def login(self):
        self.driver.get('https://tinder.com')
        sleep(3)
        
        try:
            string = "//button[contains(.,'More Options')]"
            moreops = self.driver.find_element_by_xpath(string)
            moreops.click()
            sleep(0.25)
            fb_path = '//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[3]/button'
            fb_btn = self.driver.find_element_by_xpath(fb_path)
            fb_btn.click()
        except:
            fb_path = '//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button'
            fb_btn = self.driver.find_element_by_xpath(fb_path)
            fb_btn.click()       

        # switch to login popup
        base_window = self.driver.window_handles[0]
        popup = self.driver.window_handles[1]
        self.driver.switch_to.window(popup)

        sleep(0.5)

        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(user)

        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(passw)

        login_btn = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        login_btn.click()

        sleep(2)
        # switch to original window

        self.driver.switch_to.window(base_window)

        sleep(1)

        loc_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        loc_popup.click()

        notif_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        notif_popup.click()

    def profile_scrape(self):
        self.open_profile()
        
        profile_data = {}

        # Profile Name
        try:
            css_path = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div.D\(f\).Jc\(sb\).Us\(n\).Px\(16px\).Py\(10px\) > div > div.My\(2px\).C\(\$c-base\).Us\(t\).D\(f\).Ai\(b\).Maw\(90\%\) > div > h1'
            profile_name_elem = self.driver.find_element_by_css_selector(css_path)
            profile_name = profile_name_elem.text
        except:
            profile_name = None

        profile_data['name'] = profile_name

        # Profile Age
        try:
            css_path = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div.D\(f\).Jc\(sb\).Us\(n\).Px\(16px\).Py\(10px\) > div > div.My\(2px\).C\(\$c-base\).Us\(t\).D\(f\).Ai\(b\).Maw\(90\%\) > span'
            profile_age_elem = self.driver.find_element_by_css_selector(css_path)
            profile_age = profile_age_elem.text
        except:
            profile_age = None

        profile_data['age'] = profile_age


        # ICON INFO
        job_icon = 'M7.15 3.434h5.7V1.452a.728.728 0 0 0-.724-.732H7.874a.737.737 0 0 0-.725.732v1.982z'
        college_icon = 'M11.87 5.026L2.186 9.242c-.25.116-.25.589 0 .705l.474.204v2.622a.78.78 0 0 0-.344.657c0 .42.313.767.69.767.378 0 .692-.348.692-.767a.78.78 0 0 0-.345-.657v-2.322l2.097.921a.42.42 0 0 0-.022.144v3.83c0 .45.27.801.626 1.101.358.302.842.572 1.428.804 1.172.46 2.755.776 4.516.776 1.763 0 3.346-.317 4.518-.777.586-.23 1.07-.501 1.428-.803.355-.3.626-.65.626-1.1v-3.83a.456.456 0 0 0-.022-.145l3.264-1.425c.25-.116.25-.59 0-.705L12.13 5.025c-.082-.046-.22-.017-.26 0v.001zm.13.767l8.743 3.804L12 13.392 3.257 9.599l8.742-3.806zm-5.88 5.865l5.75 2.502a.319.319 0 0 0 .26 0l5.75-2.502v3.687c0 .077-.087.262-.358.491-.372.29-.788.52-1.232.68-1.078.426-2.604.743-4.29.743s-3.212-.317-4.29-.742c-.444-.161-.86-.39-1.232-.68-.273-.23-.358-.415-.358-.492v-3.687z'
        city_icon = 'M19.695 9.518H4.427V21.15h15.268V9.52zM3.109 9.482h17.933L12.06 3.709 3.11 9.482z'
        location_icon = 'M11.436 21.17l-.185-.165a35.36 35.36 0 0 1-3.615-3.801C5.222 14.244 4 11.658 4 9.524 4 5.305 7.267 2 11.436 2c4.168 0 7.437 3.305 7.437 7.524 0 4.903-6.953 11.214-7.237 11.48l-.2.167zm0-18.683c-3.869 0-6.9 3.091-6.9 7.037 0 4.401 5.771 9.927 6.897 10.972 1.12-1.054 6.902-6.694 6.902-10.95.001-3.968-3.03-7.059-6.9-7.059h.001z'
        gender_icon = 'M15.507 13.032c1.14-.952 1.862-2.656 1.862-5.592C17.37 4.436 14.9 2 11.855 2 8.81 2 6.34 4.436 6.34 7.44c0 3.07.786 4.8 2.02 5.726-2.586 1.768-5.054 4.62-4.18 6.204 1.88 3.406 14.28 3.606 15.726 0 .686-1.71-1.828-4.608-4.4-6.338'

        try:
            profile_data['college'] = None
            profile_data['job'] = None
            profile_data['city'] = None
            profile_data['gender'] = None
            profile_data['distance'] = None
            css_path = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div.D\(f\).Jc\(sb\).Us\(n\).Px\(16px\).Py\(10px\) > div > div.Fz\(\$ms\)'
            info_table = self.driver.find_element_by_css_selector(css_path)
            info_rows = info_table.find_elements_by_class_name('Row')
            for i,row in enumerate(info_rows):
                path_elem = row.find_element_by_tag_name('path')
                iterable_path = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div.D\(f\).Jc\(sb\).Us\(n\).Px\(16px\).Py\(10px\) > div > div.Fz\(\$ms\) > div:nth-child({}) > div.Us\(t\).Va\(m\).D\(ib\).My\(2px\).NetWidth\(100\%\,20px\).C\(\$c-secondary\)'.format(i+1)
                content = row.find_element_by_css_selector(iterable_path).text
                if path_elem.get_attribute('d') == college_icon:
                    profile_data['college'] = content

                if path_elem.get_attribute('d') == job_icon:
                    profile_data['job'] = content

                if path_elem.get_attribute('d') == city_icon:
                    profile_data['city'] = content

                if path_elem.get_attribute('d') == gender_icon:
                    profile_data['gender'] = content

                if path_elem.get_attribute('d') == location_icon:
                    profile_data['distance'] = content
        except:
            pass

        # Profile Details
        try:
            details_path = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div.P\(16px\).Ta\(start\).Us\(t\).C\(\$c-secondary\).BreakWord.Whs\(pl\).Fz\(\$ms\)'
            profile_details_elem = self.driver.find_element_by_css_selector(details_path)
            contents = profile_details_elem.find_elements_by_tag_name('span')
            details = ""
            for each in contents:
                details += (each.text + " ")
        except:
            details = None

        profile_data['details'] = details

        # SPOTIFY DATA
        anthem_artist_selector = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div:nth-child(5) > div > div > div > div.D\(f\).Fz\(\$s\).C\(\$c-secondary\) > span'
        anthem_song_selector = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div:nth-child(5) > div > div > div > div.Mb\(4px\).Ell.Fz\(\$ms\)'

        try:
            anthem_artist_elem = self.driver.find_element_by_css_selector(anthem_artist_selector)
            anthem_artist = anthem_artist_elem.text
            anthem_song_elem = self.driver.find_element_by_css_selector(anthem_song_selector)
            anthem_song = anthem_song_elem.text
            profile_data['anthem'] = (anthem_song,anthem_artist)
        except:
            profile_data['anthem'] = None

        # Profile Picture URLs
        try:
            images = set()
            slideshow = self.driver.find_element_by_class_name('react-swipeable-view-container')
            num_images = len(slideshow.find_elements_by_tag_name('div'))-3
            for _ in range(num_images):
                self.next_image()
                sleep(0.25)
                all_image = self.driver.find_elements_by_class_name('profileCard__slider__img')
                for each in all_image:
                    url = each.get_attribute('style').split('"')[1]
                    images.add(url)
        except:
            images = None

        profile_data['profile_pic_urls'] = list(images)
    

        csv_columns = ['name','age','college','job','city','gender','distance','details','anthem','profile_pic_urls']
        csv_filename = 'data/profile_data_pc.csv'
        
        # First Time Initialize
        # with open(csv_filename,'w',encoding="utf-8") as file:
        #     writer = csv.DictWriter(file, fieldnames=csv_columns)
        #     writer.writeheader()
        #     writer.writerow(profile_data)
        
        # # Update data/profile_data.csv
        with open(csv_filename,'a',encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writerow(profile_data)

        self.like_key()

    def open_profile(self):
        ActionChains(self.driver).send_keys(Keys.ARROW_UP).perform()

    def like_key(self):
        ActionChains(self.driver).send_keys(Keys.ARROW_RIGHT).perform()

    def dislike_key(self):
        ActionChains(self.driver).send_keys(Keys.ARROW_LEFT).perform()

    def next_image(self):
        ActionChains(self.driver).send_keys(Keys.SPACE).perform()

    def like(self):
        like_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')
        dislike_btn.click()

    def match_popup(self):
        m_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        m_btn.click()

    def homescreen_popup(self):
        hs_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]/span')
        hs_btn.click()

    def plus_popup(self):
        plus_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[3]/button[2]')
        plus_popup.click()

    def ausw(self):
        count, matches = 0, 0
        stopper = int(input('How many swipes do we stop at? '))
        message = int(input('Message people after? '))
        while count != stopper:
            sleep(1)
            try:
                self.profile_scrape()
                count += 1
                print ('Like Counter: {} |  Match Counter: {}'.format(count, matches))
                if message == 1:
                    if count == stopper:
                        self.auto_message()
            except Exception:
                sleep (0.5)
                try:
                    self.homescreen_popup()
                except Exception:
                    try:
                        self.match_popup()
                        matches += 1
                        print ('---> Match Counter: {} <---'.format(matches))
                    except Exception:
                        pass                    

    def send_messages(self):
        match_btn = self.driver.find_element_by_xpath('//*[@id="matchListNoMessages"]/div[1]/div[2]/a/div[1]')
        match_btn.click()

        sleep(1)

        # You can change the message to say whatever you want
        message_in = self.driver.find_element_by_xpath('//*[@id="chat-text-area"]')
        message_in.send_keys('I was told to expand my job search, so I did. Hi Im Aaron!')

        sleep(1)

        send_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/button/span')
        send_btn.click()

    def match_tab(self):
        mt_btn = self.driver.find_element_by_xpath('//*[@id="match-tab"]')
        mt_btn.click()

    def close_tab(self):
        close_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[1]/a/button')
        close_btn.click()

    # automatically messages people
    def auto_message(self):
        sent = 0
        while True:
            sleep(1)
            try:
                self.match_tab()
                self.send_messages()
                sent += 1
                print ('Messages sent: {}'.format(sent))
            except Exception:
                pass


bot = TinderBot()
bot.login()
sleep(5)
# bot.auto_swipe()
# bot.auto_message()