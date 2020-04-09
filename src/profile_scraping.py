from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def profile_pic_urls(page):
    images = set()
    slideshow = page.find_element_by_class_name('react-swipeable-view-container')
    num_images = len(slideshow.find_elements_by_tag_name('div'))-3
    print('NUMBER OF IMAGES FOUND: '+str(num_images))
    for _ in range(num_images):
        self.next_image()
        sleep(0.25)
        all_image = page.find_elements_by_class_name('profileCard__slider__img')
        print("images in loop: "+ str(len(all_image)))
        print("---STARTLOOP---")
        for each in all_image:
            print(each.get_attribute('style'))
            url = each.get_attribute('style').split('"')[1]
            print(url)
            images.add(url)
    print(len(images))
    return list(images)


def profile_scrape2(self):
        self.open_profile()
        
        profile_data = {}

        images = set()

        slideshow = self.driver.find_element_by_class_name('react-swipeable-view-container')
        num_images = len(slideshow.find_elements_by_tag_name('div'))-3
        print('NUMBER OF IMAGES FOUND: '+str(num_images))
        for _ in range(num_images):
            self.next_image()
            sleep(0.25)
            all_image = self.driver.find_elements_by_class_name('profileCard__slider__img')
            print("images in loop: "+ str(len(all_image)))
            print("---STARTLOOP---")
            for each in all_image:
                print(each.get_attribute('style'))
                url = each.get_attribute('style').split('"')[1]
                print(url)
                images.add(url)
        print(len(images))
        profile_data['profile_pic_urls'] = list(images)
    

        # Profile Name
        try:
            css_path = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div.D\(f\).Jc\(sb\).Us\(n\).Px\(16px\).Py\(10px\) > div > div.My\(2px\).C\(\$c-base\).Us\(t\).D\(f\).Ai\(b\).Maw\(90\%\) > div > h1'
            profile_name_elem = self.driver.find_element_by_css_selector(css_path)
            profile_name = profile_name_elem.text
        except:
            print('Failed to get Name')
            profile_name = None

        profile_data['name'] = profile_name

        # Profile Age
        try:
            css_path = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div.D\(f\).Jc\(sb\).Us\(n\).Px\(16px\).Py\(10px\) > div > div.My\(2px\).C\(\$c-base\).Us\(t\).D\(f\).Ai\(b\).Maw\(90\%\) > span'
            profile_age_elem = self.driver.find_element_by_css_selector(css_path)
            profile_age = profile_age_elem.text
        except:
            print('Failed to get Age')
            profile_age = None

        profile_data['age'] = profile_age


        # ICON INFO
        job_icon = 'M7.15 3.434h5.7V1.452a.728.728 0 0 0-.724-.732H7.874a.737.737 0 0 0-.725.732v1.982z'
        college_icon = 'M11.87 5.026L2.186 9.242c-.25.116-.25.589 0 .705l.474.204v2.622a.78.78 0 0 0-.344.657c0 .42.313.767.69.767.378 0 .692-.348.692-.767a.78.78 0 0 0-.345-.657v-2.322l2.097.921a.42.42 0 0 0-.022.144v3.83c0 .45.27.801.626 1.101.358.302.842.572 1.428.804 1.172.46 2.755.776 4.516.776 1.763 0 3.346-.317 4.518-.777.586-.23 1.07-.501 1.428-.803.355-.3.626-.65.626-1.1v-3.83a.456.456 0 0 0-.022-.145l3.264-1.425c.25-.116.25-.59 0-.705L12.13 5.025c-.082-.046-.22-.017-.26 0v.001zm.13.767l8.743 3.804L12 13.392 3.257 9.599l8.742-3.806zm-5.88 5.865l5.75 2.502a.319.319 0 0 0 .26 0l5.75-2.502v3.687c0 .077-.087.262-.358.491-.372.29-.788.52-1.232.68-1.078.426-2.604.743-4.29.743s-3.212-.317-4.29-.742c-.444-.161-.86-.39-1.232-.68-.273-.23-.358-.415-.358-.492v-3.687z'
        city_icon = 'M19.695 9.518H4.427V21.15h15.268V9.52zM3.109 9.482h17.933L12.06 3.709 3.11 9.482z'
        location_icon = 'M11.436 21.17l-.185-.165a35.36 35.36 0 0 1-3.615-3.801C5.222 14.244 4 11.658 4 9.524 4 5.305 7.267 2 11.436 2c4.168 0 7.437 3.305 7.437 7.524 0 4.903-6.953 11.214-7.237 11.48l-.2.167zm0-18.683c-3.869 0-6.9 3.091-6.9 7.037 0 4.401 5.771 9.927 6.897 10.972 1.12-1.054 6.902-6.694 6.902-10.95.001-3.968-3.03-7.059-6.9-7.059h.001z'
        gender_icon = 'M15.507 13.032c1.14-.952 1.862-2.656 1.862-5.592C17.37 4.436 14.9 2 11.855 2 8.81 2 6.34 4.436 6.34 7.44c0 3.07.786 4.8 2.02 5.726-2.586 1.768-5.054 4.62-4.18 6.204 1.88 3.406 14.28 3.606 15.726 0 .686-1.71-1.828-4.608-4.4-6.338'

        try:
            css_path = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div.D\(f\).Jc\(sb\).Us\(n\).Px\(16px\).Py\(10px\) > div > div.Fz\(\$ms\)'
            info_table = self.driver.find_element_by_css_selector(css_path)
            info_rows = info_table.find_elements_by_class_name('Row')
            print(str(len(info_rows))+" - INFO ELEMENTS")
            for i,row in enumerate(info_rows):
                path_elem = row.find_element_by_tag_name('path')
                iterable_path = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div.D\(f\).Jc\(sb\).Us\(n\).Px\(16px\).Py\(10px\) > div > div.Fz\(\$ms\) > div:nth-child({}) > div.Us\(t\).Va\(m\).D\(ib\).My\(2px\).NetWidth\(100\%\,20px\).C\(\$c-secondary\)'.format(i+1)
                content = row.find_element_by_css_selector(iterable_path).text
                if path_elem.get_attribute('d') == college_icon:
                    print("FOUND COLLEGE")
                    profile_data['college'] = content

                if path_elem.get_attribute('d') == job_icon:
                    print("FOUND JOB")
                    profile_data['job'] = content

                if path_elem.get_attribute('d') == city_icon:
                    print("FOUND CITY")
                    profile_data['city'] = content

                if path_elem.get_attribute('d') == gender_icon:
                    print("FOUND GENDER")
                    profile_data['gender'] = content

                if path_elem.get_attribute('d') == location_icon:
                    print("FOUND DISTANCE")
                    profile_data['distance'] = content

                

        except:
            print('Profile Info BROKEN')


        # Profile Details
        try:
            print("---TRYING FOR DETAILS---")
            details_path = '#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.profileCard.Pos\(r\).D\(f\).Ai\(c\).Fld\(c\).Expand--s.Mt\(a\) > div.Pos\(r\)--ml.Z\(1\).Bgc\(\#fff\).Ov\(h\).Expand.profileContent.Bdrs\(8px\)--ml.Bxsh\(\$bxsh-card\)--ml > div > div.Bgc\(\#fff\).Fxg\(1\).Z\(1\).Pb\(100px\) > div.P\(16px\).Ta\(start\).Us\(t\).C\(\$c-secondary\).BreakWord.Whs\(pl\).Fz\(\$ms\)'
            profile_details_elem = self.driver.find_element_by_css_selector(details_path)
            print('Got details container')
            contents = profile_details_elem.find_elements_by_tag_name('span')
            print(len(contents))
            details = ""
            for each in contents:
                print(each.text)
                details += (each.text + " ")
        except:
            print('Failed to get Details')
            details = None

        profile_data['details'] = details
#

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
            pass



        print('DATA SO FAR')
        print(profile_data)
        self.like_key()
