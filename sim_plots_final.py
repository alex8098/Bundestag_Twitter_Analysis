# einlesen der module
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


plt.rcdefaults()

import plotly.express as px
import plotly.graph_objects as go

def get_multi_line_title(title: str, subtitle: str):
    return f"{title}<br><sub>{subtitle}</sub><br>"

# einlesen einer csv datei
df = pd.read_csv("data/similarities_list.csv")
#del df['Unnamed: 0']
# Bestimme Maximum einer Zeile (Spaltenweise)
df['Label_num'] = df[['Bildung', 'Umwelt', 'Digi', 'SozialeMedien', 'SozialeSicherung', 'Steuern',
                  'Haushaltskonsolidierung']].max(axis=1)
# Bestimme Index des Maximum einer Zeile (Spaltenweise)
df['Label'] = df[['Bildung', 'Umwelt', 'Digi', 'SozialeMedien', 'SozialeSicherung', 'Steuern',
                  'Haushaltskonsolidierung']].idxmax(axis=1)

# Lege Schwellwert fest
df.loc[df['Label_num'] < 0.55, 'Label'] = "Sonstiges"
# Lösche Zeilen mit Label_num == 0 (diese enthalten keinen Text)
df = df[df.Label_num > 0.00001]

# einlesen des Datensatzes der Abgeordneten
df_mdb = pd.read_csv("data/MDB_Twitter.csv")
df_mdb= df_mdb[['Twitteraccount', 'partei']]
df_mdb = df_mdb.rename(columns ={'Twitteraccount': 'Account'}, inplace = False)

# Merge der Datensätze df und df_mdb über den eindeutigen identifier Account
df1 = pd.merge(df, df_mdb, on='Account')
df1.dropna()
df1.to_csv("data/Labels.csv", index=False)

# Liste aller unterschiedlichen Parteien
list = df1["partei"].unique()
list = str(np.append(list, "Alle"))

input_parteien = input("Welche Parteien sollen analysiert werden (Getrennt durch / angeben)? \n" 
                        "Zur Auswahl stehen" + list)

#trennt string an identifier und speichert elementweise in einer Liste (parteien)
parteien = input_parteien.split("/")

# idee nach datum

print("Welcher Zeitraum soll betrachtet werden?")
since = input("Eingabe Startdatum (YYYY-MM-DD): ")
until = input("Eingabe Enddatum (YYYY-MM-DD): ")
# since = "2017-10-01"
# until = "2021-04-09"

start_date = datetime.strptime(since, '%Y-%m-%d')
#start_date = start_date.replace(tzinfo=timezone.utc).timestamp()
end_date = datetime.strptime(until, '%Y-%m-%d')
#end_date = end_date.replace(tzinfo=timezone.utc).timestamp()

# Date Transformation (Syntax des Twitter Date Format = Syntax der User Eingabe)
df1['Date_new'] = pd.to_datetime(df1['Date']).astype(
    'datetime64[ns, Europe/Paris]').dt.tz_convert('UTC')
df1['Date_new'].dt.tz_localize(None)

df1['Date_new'] = pd.to_datetime(df1['Date_new'])
df1['Date_new'] = df1['Date_new'].apply(lambda x: pd.to_datetime(str(x)))

df1['Date_short'] = df1['Date_new'].dt.date
df1['Date_short'] = pd.to_datetime(df1['Date_short'])

df1["Timebool"] = (df1['Date_short'] >= start_date) & (df1['Date_short'] <= end_date)

df2 = df1[df1["Timebool"] == True]

for partei in parteien:
    if partei != 'Alle':
        df_partei = df2.loc[df2['partei'] == partei]
        sum_themen = df_partei.groupby(["Label"]).agg({"Label": ['count']})

        z = 0
        label_chart = []
        anzahltweets = 0
        val = []
        top = []
        while z < len(sum_themen):
            text = str(sum_themen['Label'].index[z]) + ":\n" + str(sum_themen.values[z][0]) + " Tweets"
            print(text)
            label_chart.append(text)
            anzahltweets = anzahltweets + sum_themen.values[z][0]
            val.append(sum_themen.values[z][0])
            top.append(sum_themen['Label'].index[z])

            z = z + 1
        print(label_chart)
        gesamt = "Tweets gesamt: " + str(anzahltweets)
        print(gesamt)

        title = get_multi_line_title("Tweets der " +partei+ " nach Themen der Fiwi", "Gesamttweets: " + str(len(df_partei)))

        fig = go.Figure(data=[go.Pie(labels=top,
                                     values=val,
                                     textinfo='label+percent',
                                     insidetextorientation='radial'
                                     )])

        fig.update_layout(title=title, title_x=0.48)
        fig.write_html("plots/Tweets nach Themen/SimPiePlot"+ partei + since + "-" + until + ".html")
        fig.show()

        plotframe = pd.DataFrame()
        plotframe['Label'] = sum_themen['Label'].index
        plotframe['Anzahl der Tweets'] = sum_themen['Label']["count"].values
        plotframe = plotframe.sort_values(by=["Anzahl der Tweets"], ascending=False)
        fig = px.bar(plotframe, x='Anzahl der Tweets', y='Label',
                     color='Label',
                     hover_data=['Anzahl der Tweets', 'Label'],
                     labels={'pop': 'population of Canada'}, orientation='h')

        fig.update_layout(title=title, title_x=0.48)
        fig.write_html("plots/Tweets nach Themen/SimBarplot" + partei + since + "-" + until + ".html")
        fig.show()

    else:
        sum_themen = df2.groupby(["Label"]).agg({"Label": ['count']})
        z = 0
        label_chart = []
        anzahltweets = 0
        val = []
        top = []
        while z < len(sum_themen):
            text = str(sum_themen['Label'].index[z]) + ":\n" + str(sum_themen.values[z][0]) + " Tweets"
            print(text)
            label_chart.append(text)
            anzahltweets = anzahltweets + sum_themen.values[z][0]
            val.append(sum_themen.values[z][0])
            top.append(sum_themen['Label'].index[z])

            z = z + 1
        print(label_chart)
        gesamt = "Tweets gesamt: " + str(anzahltweets)
        print(gesamt)

        title = get_multi_line_title("Tweets der Bundestagsabgeordneten nach Themen der Fiwi", "Gesamttweets: " + str(len(df2)))

        fig = go.Figure(data=[go.Pie(labels=top,
                                     values=val,
                                     textinfo='label+percent',
                                     insidetextorientation='radial'
                                     )])

        fig.update_layout(title=title, title_x=0.48)
        fig.write_html("plots/Tweets nach Themen/SimPiePlot" + partei + since + "-" + until + ".html")
        fig.show()

        plotframe = pd.DataFrame()
        plotframe['Label'] = sum_themen['Label'].index
        plotframe['Anzahl der Tweets'] = sum_themen['Label']["count"].values
        plotframe = plotframe.sort_values(by=["Anzahl der Tweets"], ascending=False)
        fig = px.bar(plotframe, x='Anzahl der Tweets', y='Label',
                     color='Label',
                     hover_data=['Anzahl der Tweets', 'Label'],
                     labels={'pop': 'population of Canada'}, orientation='h')

        fig.update_layout(title=title, title_x=0.48)
        fig.write_html("plots/Tweets nach Themen/SimBarplot" + partei + since + "-" + until + ".html")
        fig.show()

