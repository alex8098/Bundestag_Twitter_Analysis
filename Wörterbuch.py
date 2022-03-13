import pandas as pd
from os import walk
import re
import spacy
# !!! install xlrd (version >= 1.0.0) und openpyxl

#Pfad zu den Wörterbüchern
mypath="data/Wörterbuch/"

# lege leere Liste f an
f = []

# speichere filenames aus mypath in f ab
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break

# erzeuge leeres Dataframe
df_all = pd.DataFrame()

# Füge die Wörterbücher zusammen und speichere unter df_all
for file in f:
    df = pd.read_excel("data/Wörterbuch/" + file)
#   print(df)
    df_all = df_all.append(df, ignore_index=True)
#   print(df_all)

# speichere die Spaltennamen
column_names = df_all.columns.tolist()

for anz in range(1, len(column_names)):
    print(str(column_names[anz]))

# lösche nan und speichere in Liste
Bildung_list = df_all["Bildung"].dropna().tolist()
# Übergebe jeden Eintrag mit Leerzeichen getrennt
Bildung = ' '.join(Bildung_list)

# Wiederhole für alle weiteren Kategorien
Umwelt_list = df_all["Umwelt"].dropna().tolist()
Umwelt = ' '.join(Umwelt_list)

Digitalisierung_list = df_all["Digitalisierung"].dropna().tolist()
Digi = ' '.join(Digitalisierung_list)

SozialeMedien_list = df_all["Soziale Medien"].dropna().tolist()
SoMe = ' '.join(SozialeMedien_list)

SozialeSicherung_list = df_all["Soziale Sicherung"].dropna().tolist()
SoSi = ' '.join(SozialeSicherung_list)

Steuern_list = df_all["Steuern "].dropna().tolist()
Steuern = ' '.join(Steuern_list)

Haushaltskonsolidierung_list = df_all["Haushaltskonsolidierung"].dropna().tolist()
HHkon = ' '.join(Haushaltskonsolidierung_list)

# Lade NLP Spacy (3.0.0) Media und News Deutschland
nlp = spacy.load('de_core_news_lg-3.0.0/de_core_news_lg-3.0.0/de_core_news_lg/de_core_news_lg-3.0.0')

# Übergebe das Wörterbuch an SpaCy
docbildung = nlp(Bildung)
documwelt = nlp(Umwelt)
docdigi = nlp(Digi)
docsome = nlp(SoMe)
docsosi = nlp(SoSi)
docsteuern = nlp(Steuern)
dochhkon = nlp(HHkon)

liste = []
ahnlichkeitenBildung = []
ahnlichkeitenUmwelt = []
ahnlichkeitenDigi = []
ahnlichkeitenSoMe = []
ahnlichkeitenSoSi = []
ahnlichkeitenSteuern = []
ahnlichkeitenHHkon = []

clean = pd.read_csv(".\\data\\cleanComment.csv")
clean['Date'] = pd.to_datetime(clean['Date'])
clean = clean.set_index(['Date'])

# matcher = Matcher(nlp.vocab)

print(clean)
m = 0

while m < len(clean) - 1:
    # hier anpassen zu gekürzten sätzen via spacy
    text = str(clean['cleanComment'].iloc[m])
    text = re.sub(r'[^A-Za-z0-9ÄäÖöÜüß]+', ' ', text)
    doc = nlp(str(text))

    # Berechne die Ähnlichkeit von doc1 und doc2
    similaritybildung = docbildung.similarity(doc)
    similarityumwelt = documwelt.similarity(doc)
    similaritydigi = docdigi.similarity(doc)
    similaritysome = docsome.similarity(doc)
    similaritysosi = docsosi.similarity(doc)
    similaritysteuern = docsteuern.similarity(doc)
    similarityhhkon = dochhkon.similarity(doc)


    liste.append(clean['cleanComment'].iloc[m])

    ahnlichkeitenBildung.append(similaritybildung)
    ahnlichkeitenUmwelt.append(similarityumwelt)
    ahnlichkeitenDigi.append(similaritydigi)
    ahnlichkeitenSoMe.append(similaritysome)
    ahnlichkeitenSoSi.append(similaritysosi)
    ahnlichkeitenSteuern.append(similaritysteuern)
    ahnlichkeitenHHkon.append(similarityhhkon)

    m = m + 1

sim = pd.DataFrame(ahnlichkeitenBildung, liste, columns=["Bildung"])
sim["Umwelt"] = ahnlichkeitenUmwelt
sim["Digi"] = ahnlichkeitenDigi
sim["SozialeMedian"] = ahnlichkeitenSoMe
sim["SozialeSicherung"] = ahnlichkeitenSoSi
sim["Steuern"] = ahnlichkeitenSteuern
sim["Haushaltskonsolidierung"] = ahnlichkeitenHHkon

sim.to_csv("data/similarities.csv", index=False)
