import pandas as pd
# packages for session 3
import re
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Lese die Gesamtdatei ein
# df = pd.read_csv(".\data\Alle.csv")

"""
# Ziehe zufällig ohne zurücklegen eine 1 % Stichprobe
test_df = df.sample(frac=0.01, replace=False, random_state=0)

#Speicher die Stichprobe als csv ab
test_df.to_csv(".\\tweets.csv")

"""

# Einlesen der Stichprobe
df = pd.read_csv(".\\data\\tweets.csv")

# Lösche Links http
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html
# Lambda function https://www.w3schools.com/python/python_lambda.asp
# https://docs.python.org/3/library/re.html
df['cleanComment'] = df['Comment'].apply(lambda x: re.split('http:\/\/.*', str(x))[0])
# Lösche Links https
df['cleanComment'] = df['cleanComment'].apply(lambda x: re.split('https:\/\/.*', str(x))[0])

print(df)
print(df['Date'])

# df.to_csv("cleanComment.csv", index=False)
hashtag = []
hashdate = []
i = 0
while i < len(df):
    # Finde alle Hashtags
    p = re.findall(r'(?i)(?<=\#)\w+', df['cleanComment'].iloc[i])  # will not include #
    print(p)
    print(range(len(p)))
    if len(p) > 0:
        for j in range(len(p)):
            hashtag.append(p[j])
            hashdate.append(df.Date.iloc[i])
    i = i + 1

# print(hashtag)
# print(hashdate)
hashdate = pd.DataFrame(hashdate, columns=['Date'])
hashdate['Date'] = pd.to_datetime(hashdate['Date'])
hashdate['Hashtag'] = hashtag
hashdate.to_csv(".\\data\\clean.csv", index=False)

clean = pd.read_csv(".\\data\\clean.csv")

ht = clean["Hashtag"].value_counts()

# Stack overflow hilft ,,immer''
# https://stackoverflow.com/questions/64130332/seaborn-futurewarning-pass-the-following-variables-as-keyword-args-x-y

ht = ht[:20, ]  # Top 20 Begriffe
plt.figure(figsize=(20, 10))
sns.barplot(x=ht.values, y=ht.index, alpha=0.8)
plt.title('Top 20 Hashtags Overall\n')
plt.ylabel('Hashtag from Tweet', fontsize=12)
plt.xlabel('Count of Hashtag', fontsize=12)
plt.savefig(".\\plots\\tophash.png")
plt.show()
