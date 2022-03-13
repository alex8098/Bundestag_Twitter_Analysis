import numpy as np
import pandas as pd
# Nur für versteckte Passwort Eingabe notwendig
import keyring

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Attention first step: import numpy, use numpy statement and accept the use scientific mode pop up
a = 1

print("Hello students")

df = pd.read_csv("data/MDB_Twitter.csv", encoding="latin")

# Attention we need a webdriver.exe and selenium extension for the next steps
driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\chromedriver.exe")
sleep(3)
driver.maximize_window()

# navigate to the coolest chair of the world; next to twitter
# driver.get("https://schneider.wiwi.uni-wuppertal.de")

driver.get("https://twitter.com/login")

sleep(5)

username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
# insert your username in ""
username.send_keys("AlexJohae")
password = driver.find_element_by_xpath('//input[@name="session[password]"]')
#insert your password in ""
password.send_keys("80982000svzWER")

# Close Cookies
driver.find_element_by_xpath(
    '//div[@class="css-901oao r-1awozwy r-jwli3a r-6koalj r-18u37iz r-16y2uox r-1qd0xha r-a023e6 r-b88u0q r-1777fci '
        'r-rjixqe r-dnmrzs r-bcqeeo r-q4m81j r-qvutc0"]').click()

sleep(2)

password.send_keys(Keys.RETURN)

sleep(3)

# Navigate to twitteraccount

search_profile = "https://twitter.com/@Karl_Lauterbach"
driver.get(search_profile)

sleep(3)

# class to get ort "css-901oao css-16my406 r-m0bqgq r-4qtqp9 r-poiln3 r-1b7u577 r-bcqeeo r-qvutc0"
ort_element = driver.find_element_by_xpath(
    '//span[@class="css-901oao css-16my406 r-m0bqgq r-4qtqp9 r-poiln3 r-1b7u577 r-bcqeeo r-qvutc0"]')

# convert to 1 variable called ort from webdriver element "ort_element"
ort = ort_element.text

# class to get followers "css-901oao css-16my406 r-18jsvk2 r-poiln3 r-b88u0q r-bcqeeo r-qvutc0"
following_element = driver.find_element_by_xpath(
    '//span[@class="css-901oao css-16my406 r-18jsvk2 r-poiln3 r-b88u0q r-bcqeeo r-qvutc0"]')

# convert to 1 variable called following from webdriver element "following_element"
following = following_element.text