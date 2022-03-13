import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv("tweets.csv")

# Texterkennung von Hashtags in Tweets

test = pd.DataFrame()
test["Tweet"] = [
    "hello students, lets learn Python #fiwi #fiwi #2021uni@home #1 #1 #1 https://moodle.uni-wuppertal.de/mod/folder/view.php?id=761821"]

test["Tweet"].apply(lambda x: re.split('https:\/\/.*?', str(x))[0])

h = re.findall(r'(?i)(?<=\#)\w+', test["Tweet"].iloc[0])

hashtag = []

for j in range(len(h)):
    print(h[j])
    hashtag.append(h[j])

Hash = pd.DataFrame()

Hash["Hashtags"] = hashtag

ht = Hash["Hashtags"].value_counts()

ht = ht[:2] #Top 2 Hashtags

sns.barplot(x = ht.values, y = ht.index, alpha=0.8)
plt.title("Top 2 Hashtags")
plt.ylabel("Hashtags from Tweet")
plt.xlabel("count")
plt.show()



