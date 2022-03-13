import pandas as pd
# Nur für versteckte Passwort Eingabe notwendig
import keyring

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date

print("Hello students")
#speichere das Datum ab
today = date.today()

d1 = today.strftime('%d_%m_%Y')
print('d1=', d1)
df = pd.read_csv("data/MDB_Twitter.csv", encoding="latin")

# Attention we need a webdriver.exe and selenium extension for the next steps
driver = webdriver.Chrome("C:\\Program Files (x86)\\Google\\Chrome\\chromedriver.exe")
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
# insert your password in ""
password.send_keys("80982000svzWER")

# Close Cookies
driver.find_element_by_xpath(
    '//div[@class="css-901oao r-1awozwy r-jwli3a r-6koalj r-18u37iz r-16y2uox r-1qd0xha r-a023e6 r-b88u0q r-1777fci '
        'r-rjixqe r-dnmrzs r-bcqeeo r-q4m81j r-qvutc0"]').click()

sleep(2)

password.send_keys(Keys.RETURN)

sleep(3)

# Navigate to twitteraccount
"""
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
"""
# speichere die Spalte Twitteraccount in list
list = df["Twitteraccount"]

#entferne alle nan Einträge
list_acc = list.dropna()

ort = []
follow = []
following = []
following_all = []

follower = []
follower_all = []

i = 0

df_temp = pd.DataFrame(columns =["Twitteraccount", "Following" + d1, "Follower" + d1, "Ort"]).fillna(value="nan")
df_temp["Twitteraccount"] = list_acc

# w3school for loop
for acc in list_acc:
    if i<8:
        search_profile = "https://twitter.com/" + acc
        driver.get(search_profile)

        sleep(6)

        # class to get ort "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"
        ort_element = driver.find_element_by_xpath(
            '//span[@class="css-901oao css-16my406 r-m0bqgq r-4qtqp9 r-poiln3 r-1b7u577 r-bcqeeo r-qvutc0"]')

        sleep(3)
        # ort = ort_element.text
        ort.append(ort_element.text)

        # class to get followers "css-901oao css-16my406 r-18jsvk2 r-poiln3 r-b88u0q r-bcqeeo r-qvutc0"
        follow_element = driver.find_element_by_xpath(
            '//div[@class="css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"]')

        sleep(3)
        follow.append(follow_element.text)
        follower = follow[i].split("\n", 1)

        follower[0] = follower[0].replace(" Following", "")
        follower[0] = follower[0].replace(",", "")
        follower[0] = follower[0].replace(".", "")
        follower[0] = follower[0].replace("K", "00")
        print(follower[0])
        following_all.append(follower[0])
        # save to dataframe
        df_temp["Following" + d1][i] = follower[0]

        follower[1] = follower[1].replace(" Followers", "")
        follower[1] = follower[1].replace(",", "")
        # 1K ist zwar = 1000 aber hier wird .x angegeben was ist mit abcK
        # txt = "Hello, welcome to my world." x = txt.find("e") returns 1
        follower[1] = follower[1].replace(".", "")
        follower[1] = follower[1].replace("K", "00")
        print(follower[1])
        follower_all.append(follower[1])
        # save to dataframe
        df_temp["Follower" + d1][i] = follower[1]

        i=i+1
        print(i)
        print(acc)
    else:
        break

print("The End")