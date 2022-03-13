import pandas as pd
import spacy
from spacy.lang.de import German
import explacy

print(spacy.__version__)

# https://github.com/explosion/spacy-models/releases//tag/de_core_news_lg-3.0.0
nlp = spacy.load("de_core_news_lg-3.0.0/de_core_news_lg/de_core_news_lg-3.0.0")

doc = nlp("Twitter Inc. und die Bundestagswahl 2021 an der Universität Wuppertal. Martin Schulz führt die Rangliste"
          " mit 640000 Follower an!")

print("Index : ", [token.i for token in doc])
print("Text: ", [token.text for token in doc])
print("is_alpha: ", [token.is_alpha for token in doc])
print("is_punct: ", [token.is_punct for token in doc])
print("like_num: ", [token.like_num for token in doc])

for token in doc:
    token_text = token.text
    token_pos = token.pos_
    token_dep = token.dep_
    print("Text: ", token_text, "Tag: ", token.pos_, "Dependecies: ", token.dep_)

    if (token_pos == 'ADJ') or (token_pos == 'PROPN') or (token_pos == 'NOUN') or (token_pos =='VERB'):
        tweet.neu.append(token_text + ' ')
spacy.explain("PROPN")
spacy.explain("CCONJ")
spacy.explain("DET")

# explacy.print_parse_info(nlp, "Twitter Inc. und die Bundestagswahl 2021 an der Universität Wuppertal. Martin Schulz führt die Rangliste"
#          " mit 640000 Follower an!")

# explacy.print_parse_info(nlp, "Sie hat eine Pizza gegessen!")

ent_text = []
ent_label = []

for ent in doc.ents:
    print(ent.text, ent.label_)
    ent_text.append(ent.text + " ")
    ent_label.append(ent.label_ + " ")

ent = pd.DataFrame(list(zip(ent_label, ent_text)), columns=["ent_text", "ent_label"])
print(tweet_neu)