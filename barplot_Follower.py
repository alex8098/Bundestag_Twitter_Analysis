import pandas as pd
# install module plotly; ipykernel; nbformat
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"

# Die Datei sollte so eingelesen werden das umlaute auch übersetzt werden!
df_mdb = pd.read_csv(".\\data\\MDB_Twitter.csv", encoding="latin1")

# Follower Analyse

anz_follower = df_mdb.groupby('partei')['Follower15_05_2021']
anz_follower=anz_follower.mean()
anz_follower=anz_follower.sort_values(ascending=False)

follower = anz_follower.to_frame().reset_index()

title = 'Beliebtheit der Parteien nach durchschnittlicher Followerzahl'

fig = px.bar(follower, x='partei', y='Follower15_05_2021', color = 'partei',
             labels={'Follower15_05_2021':'Follower',
                     'partei': 'Parteiname'},
             color_discrete_map = {'Union': 'rgb(26, 26, 26)',
                                  'SPD': 'rgb(205, 27, 1)',
                                  'FDP': 'rgb(255, 221, 0)',
                                  'AfD': 'rgb(1, 209, 255)',
                                  'Gruene': 'rgb(43, 216, 0)',
                                  'Linke': 'rgb(181, 34, 105)',
                                  'fraktionslos': 'rgb(150, 150, 150)'}
)

fig.update_layout(
title=title, title_x=0.48)
fig.write_html(".\\plots\\Follower.html")
fig.show()

anz_following = df_mdb.groupby('partei')['Following15_05_2021']
anz_following=anz_following.mean()
anz_following=anz_following.sort_values(ascending=False)

follower = anz_following.to_frame().reset_index()

title = 'Beliebtheit der Parteien nach durchschnittlicher Followerzahl'

fig = px.bar(following, x='partei', y='Following15_05_2021', color = 'partei',
             labels={'Following15_05_2021':'Following',
                     'partei': 'Parteiname'},
             color_discrete_map = {'Union': 'rgb(26, 26, 26)',
                                  'SPD': 'rgb(205, 27, 1)',
                                  'FDP': 'rgb(255, 221, 0)',
                                  'AfD': 'rgb(1, 209, 255)',
                                  'Gruene': 'rgb(43, 216, 0)',
                                  'Linke': 'rgb(181, 34, 105)',
                                  'fraktionslos': 'rgb(150, 150, 150)'}
)

fig.update_layout(
title=title, title_x=0.48)
fig.write_html(".\\plots\\Following.html")
fig.show()

