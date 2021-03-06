# #Importing all needed libraries
# from selenium import webdriver
# import time
# import os
# import time
# import requests
# from pprint import pprint
# from bs4 import BeautifulSoup
# import pandas as pd

# import json
# from lxml import html
# import re
# import csv
# import numpy as np

# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import (
#     NoSuchElementException,
#     TimeoutException,
#     WebDriverException,
#     )

# import pandas as pd

# WAIT_TIME   = 10
# WAIT_TIME_2 = 5
# WAIT_TIME_3 = 3
# WAIT_TIME_4 = 0.5
# WAIT_TIME_5 = 1

# chromedriver_path = '/home/omar/Descargas/chromedriver2022'

# PASSWORD = 'test'
# USERNAME = 'test'

# def load_instagram():
#     """
#     Function to initialize Instagram and launch it in a browser using Selenium
#     """
#     # Chrome driver should be in
#     executable_path=os.path.join(chromedriver_path)

#     options = webdriver.ChromeOptions()
#     options.add_argument('--ignore-certificate-errors')
#     options.add_argument('--disable-notifications')

#     # 1-Allow, 2-Block, 0-default
#     preferences = {
#         "profile.default_content_setting_values.notifications" : 2,
#         "profile.default_content_setting_values.location": 2,
#         # We don't need images, only the URLs.
#         "profile.managed_default_content_settings.images": 2,
#         }
#     options.add_experimental_option("prefs", preferences)


#     browser = webdriver.Chrome(
#         executable_path=executable_path,
#         chrome_options=options,
#         )
#     browser.wait = WebDriverWait(browser, WAIT_TIME)   
    
#     #Opening the browser and getting the url

#     url = "https://www.instagram.com/p/B166OkVBPJR/"
#     browser.get(url)
    
#     #wait 5 seconds to load
#     time.sleep(WAIT_TIME_2)
    
#     # Accept cookies
#     cookies = WebDriverWait(browser, WAIT_TIME_3).until(
#         EC.element_to_be_clickable((By.XPATH,'//button[contains(text(), "Aceptar")]'))).click()
    
#     return browser


# def instagram_login(driver):
#     """
#     Login to Instagram using username and password.
    
#     Variables:
#         - browser: webdriver
#             Used to manage browser functionalities
#     """
#     usr = driver.find_element_by_name("username")
#     usr.send_keys(USERNAME)
#     password = driver.find_element_by_name("password")
#     password.send_keys(PASSWORD)
#     password.send_keys(Keys.RETURN)
#     time.sleep(WAIT_TIME_2)
    
    
# def get_info_by_tag(keyword,browser,max_number_images):
#     """
#     Function to retrieve all the information from different posts by tag
    
#     Variables:
#         - keyword: str
#             Tag used to filter or search images or posts
#         - browser: webdriver
#             Used to manage browser functionalities
#         - max_number_images: int
#             Maximum number of images or post to retrieve information from
#     """

#     print(f"Scraping all the info. It will take at around {WAIT_TIME_5*max_number_images} seconds")
    
#     # Get the search box
#     searchbox = WebDriverWait(browser,WAIT_TIME).until(
#         EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Busca']")))
    
#     searchbox.clear()

#     # Search by tag
#     searchbox.send_keys(keyword)
#     time.sleep(WAIT_TIME_3)
#     searchbox.send_keys(Keys.ENTER)
#     time.sleep(WAIT_TIME_3)
#     searchbox.send_keys(Keys.ENTER)
#     time.sleep(WAIT_TIME_3)
    
    
#     image_urls = []
#     likes_lst  = []
#     comments_lst = []
#     img_urls_err =[]
    
#     image_count = 0
#     first_time  = True
#     while image_count < max_number_images:
#         #scroll to the end
#         scroll_to_end(browser)
        
#         # Fetch src attributes from images
#         images    = fetch_images(browser,first_time)
#         firs_time = False
        
#         # Get comments and likes from the images or posts
#         likes_comments = fetch_likes_comments(browser,image_urls)
            
#         likes    = likes_comments[1]
#         comments = likes_comments[0]
#         img_err  = likes_comments[2]

#         # Add these items to the rest of previous scrolldowns
#         comments_lst += comments
#         likes_lst    += likes
#         img_urls_err += img_err
#         image_urls   += images
        
#         image_count = len(image_urls)
        
#         # Exit the while loop if number of images > maximum number of images
#         if image_count >= max_number_images:
#             print(f"Found: {image_count} image links, done!")
#             break
     
        
#     print('Number of scraped images: ', len(likes_lst))
    
#     return {'Image URL':image_urls[:len(likes_lst)],'Likes':likes_lst,'Comments':comments_lst}    

# def scroll_to_end(driver):
#     """
#     Funtion used to scrolldown to the end of the window
#     """
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(WAIT_TIME_4)
    
# def download_images(keyword,images):
#     """
#     Funtion used to download  images
#     """
#     fpath = os.getcwd()
#     fpath = os.path.join(fpath, keyword[1:])
  
#     if(not os.path.isdir(fpath)):
#         os.mkdir(fpath)
    
#     #download images
#     counter = 0
#     image_name_lst = []
#     for image in images:
#         persist_image(fpath,image,counter,image_name_lst)
#         counter += 1
#     return image_name_lst

# def persist_image(folder_path:str,url:str, counter,image_name_lst):
#     """
#     Funtion used to persist physically in locahost an image from a url
#     """
#     try:
#         image_content = requests.get(url).content

#     except Exception as e:
#         print(f"ERROR - Could not download {url} - {e}")

#     try:
#         img_name =  'jpg' + "_" + str(counter) + ".jpg"
#         f = open(os.path.join(folder_path,img_name), 'wb')
#         f.write(image_content)
#         f.close()
#         print(f"SUCCESS - saved {url} - as {folder_path}")
#         image_name_lst.append(img_name)
#     except Exception as e:
#         print(f"ERROR - Could not save {url} - {e}")
        

# def fetch_comments(browser,comment_lst):
#     """
#     Function that fetchs comments from a post
    
#     """
#     comment = [["None"]]
#     try:
#         comment_elements = browser.find_elements_by_css_selector(".eo2As .gElp9 .C4VMK")
#         comment = [element.find_elements_by_tag_name('span')[1].text for element in comment_elements]
      
#     except Exception as e:  
#         print(f"ERROR - Could not fetch comment  {e}") 
        
#     comment_lst.append(comment)   
#     return comment_lst



# def process_info(insta_info):
#     """
#     Function that process the info retrieved from posts
    
#     """
    
#     df = pd.DataFrame(insta_info)
    
#     # The first comment is considered as a title
#     df["Title"]    = [i[0] for i in list(df["Comments"])] 
#     df["Comments"] = [i[1:] for i in list(df["Comments"])]
    
#     # Get all the hashtags from the title
#     df["Principal Hashtags"] = [ re.findall("#(\w+)", title)  for title in list(df["Title"])]
    
#     return df
   
    

# def scrapping_instagram(keyword,max_number_images = 100,download=False):
#     """
#     Function to perform an Instagram scraping 
    
#     Variables:
#         - keyword: str
#             Tag used to filter or search images or posts
#         - browser: webdriver
#             Used to manage browser functionalities
#         - max_number_images: int
#             Maximum number of images or post to retrieve information from
#         - download: boolean
#             Boolean to download images and export dataframe as a .xlsx file  
    
#     """
#     browser = load_instagram()
#     instagram_login(browser)
#     insta_info = get_info_by_tag(keyword,browser,max_number_images)
#     browser.close()

#     # Process the info and get a Pandas dataframe
#     df = process_info(insta_info)
    
#     if download:
#         df["Download name"] = download_images(keyword,list(df["Image URL"]))
#         df.to_csv(str(keyword)+'.csv',index=False, header=True)
    
   
#     return df

# df = scrapping_instagram("#vacations",max_number_images =50,download=False)

from random import randint, random
import unittest
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select

PASSWORD = 'test'
USERNAME = 'test'
class usando_unittest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_manejando_mouse(self):
        self.driver.get("https://www.instagram.com/p/B166OkVBPJR/")
        movim = ActionChains(self.driver)
        time.sleep(3)
        # mouse_move = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button/div/svg')
        # movim = ActionChains(self.driver)
        # movim.move_to_element(mouse_move).click().perform()
        usr = self.driver.find_element(By.NAME, "username")
        usr.send_keys(USERNAME)
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(PASSWORD)
        password.send_keys(Keys.RETURN)
        time.sleep(4)
        password = self.driver.find_element(By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/button")
        movim.move_to_element(password).click().perform()
        time.sleep(5)
        
        try:
            m = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]')
            self.driver.execute_script("arguments[0].scrollIntoView();",m)
            time.sleep(1)
            load_more_comment = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button/div/svg")
            print("Found {}".format(str(load_more_comment)))
            
            while load_more_comment.is_displayed():
                load_more_comment.click()
                time.sleep(1.5)
                load_more_comment = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button/div/svg")
                print("Found {}".format(str(load_more_comment)))
                
        except Exception as e:
            print(e)
            pass


        # comment_elements = self.driver.find_elements(By.CSS_SELECTOR, "._a9zs")
        # print(len(comment_elements))
        # time.sleep(4)
        # for a in comment_elements:
        #     print(a)
        #     time.sleep(0.5)
        #     print('hello world')
        # time.sleep(5)
    
    def tearDown(self):
        self.driver.close()
if __name__ ==  "__main__":
    unittest.main()
