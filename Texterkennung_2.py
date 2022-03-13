import re
import pandas as pd
import spacy
import os

import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

start = datetime.now()

print(spacy.__version__)

def createfolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

createfolder(".\\plots")

# Hier wird die zugrundeliegende Datenbank von spaCy spezifiziert
nlp = spacy.load('de_core_news_lg-3.0.0/de_core_news_lg-3.0.0/de_core_news_lg/de_core_news_lg-3.0.0')

# Einlesen der Stichprobe
df = pd.read_csv(".\\data\\tweets.csv")

# Einlesen des Gesamtdatensatz
#df = pd.read_csv(".\\data\\Alle.csv")

# Lösche Links http
df['cleanComment'] = df['Comment'].apply(lambda x: re.split('http:\/\/.*', str(x))[0])
# Lösche Links https
df['cleanComment'] = df['cleanComment'].apply(lambda x: re.split('https:\/\/.*', str(x))[0])

df.to_csv(".\\data\\cleanComment.csv", index=False)

clean = pd.read_csv(".\\data\\cleanComment.csv")

i = 0
ent_text = []
ent_label = []

while i < len(clean):
    text = str(clean['cleanComment'].iloc[i])
    doc = nlp(text)

    for token in doc:
    #    print(token)
    # Greife auf den Text, die Wortart und die Dependenzrelation des Tokens zu
        token_text = token.text
    #    print(token_text)
        token_pos = token.pos_
    #    print(token.pos_)
        token_dep = token.dep_
        print("Text: ", token.text, "Tag: ", token.pos_, "Dependencie: ", token.dep_)

        for ent in doc.ents:
                print(ent.text, ent.label_)
                ent_text.append(ent.text + " ")
                ent_label.append(ent.label_ + " ")

    i=i+1

ent = pd.DataFrame(list(zip(ent_text, ent_label)), columns=["ent_text", "ent_label"])

#for line in range(len(ent)):
#    ent["ent_text"] = ent["ent_text"].iloc[line].rstrip()
#    ent["ent_label"] = ent["ent_label"].iloc[line].rstrip()

entitäten = ['ORG ', 'LOC ', 'MISC ', 'PER ']

for enti in entitäten:
    df1 = ent.where(ent['ent_label'] == enti)
    df1 = df1['ent_text'].value_counts()
    if enti == 'PER':
        df1 = df1.drop(index='Corona ')
        df1 = df1.drop(index='Danke ')
        df1 = df1.drop(index='BuReg ')
    df = df1[:20, ]
    plt.figure(figsize=(20, 10))
    sns.barplot(x = df.values,y = df.index, alpha=0.8)
    plt.ylabel('Word from Tweet', fontsize=12)
    plt.xlabel('Count of Words', fontsize=12)
    if enti == 'ORG ':
        plt.title('Top 20 Organizations Mentioned\n')
        plt.savefig(".\\plots\\" + enti + ".png")
    elif enti == 'PER ':
        plt.title('Top 20 People Mentioned\n')
        plt.savefig(".\\plots\\" + enti + ".png")
    elif enti == 'LOC ':
        plt.title('Top 20 Locations Mentioned\n')
        plt.savefig(".\\plots\\" + enti + ".png")
    else:
        plt.title('Top 20 MISC Mentioned\n')
        plt.savefig(".\\plots\\" + enti + ".png")

    plt.show()

end = datetime.now()
runtime = end - start
print("Die Laufzeit beträgt", runtime)
