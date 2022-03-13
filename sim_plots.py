import pandas as pd
import matplotlib.pyplot as plt

plt.rcdefaults()
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("data/similarities_list.csv")
#bestimme Maximum des Tweets
df['Label_num'] = df.max(axis=1)
df['Label'] = df[['Bildung', 'Umwelt', 'Digi', 'SozialeMedien', 'SozialeSicherung', 'Steuern',
                  'Haushaltskonsolidierung']].idxmax(axis=1)
#lege Schwellwert fest
df.loc[df['Label_num'] < 0.55, 'Label'] = "Sonstiges"

df.to_csv("data/Labels.csv")

#Idee nach Partei Anteile bestimmen
sum_themen = df.groupby("Label").agg({"Label": ['count']})

print(sum_themen)

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

title = "Tweets nach Themen der Fiwi"

fig = go.Figure(data=[go.Pie(labels=top,
                             values=val,
                             textinfo='label+percent',
                             insidetextorientation='radial'
                             )])

fig.update_layout(title=title, title_x=0.48)
fig.write_html("plots/SimTweets.html")
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
fig.write_html("plots/LabelBarplot.html")
fig.show()

