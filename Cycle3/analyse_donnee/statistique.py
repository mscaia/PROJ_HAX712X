import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import calendar
import kaleido
import numpy as np

#%%
# Script pour tracer les diagrammes en barre et pour faire les diagrammes circulaires du cours HAX712X.
for i in range(4):  # Parcourir les 4 jeux de données.
    if i==0 :
        chemin ="./data/CoursesVelomagg.csv"
        annee = 2024
    if i==1 :
        chemin ="./data/extracted/TAM_MMM_CoursesVelomagg_2021.csv"
        annee = 2021
    if i==2 :
        chemin ="./data/extracted/TAM_MMM_CoursesVelomagg_2022.csv"
        annee = 2022
    if i==3 :
        chemin ="./data/extracted/TAM_MMM_CoursesVelomagg_2023.csv"
        annee = 2023
    # Traitement du dataframe
    df_coursesvelomagg = pd.read_csv(chemin)
    if i==1:
        df_coursesvelomagg = pd.read_csv(chemin, delimiter=';') # Mauvais format
    df_coursesvelomagg_traité = df_coursesvelomagg
    # Convertir la colonne 'Departure' en datetime
    df_coursesvelomagg_traité['Departure'] = pd.to_datetime(df_coursesvelomagg_traité['Departure'])
    # Extraire les dates de départ
    df_coursesvelomagg_traité['Date'] = df_coursesvelomagg_traité['Departure'].dt.date
    df_bikes = df_coursesvelomagg_traité

    # Statistique sur le nombre de trajet effectué par jour
    # Compter le nombre de trajets par jour pour les départs
    trajets_depart = df_coursesvelomagg_traité.groupby('Date').size().reset_index(name='Nombre de trajets')
    # Remplir les NaN par 0 pour les dates sans trajets
    trajets_depart.fillna(0, inplace=True)
    # Afficher le résultat
    print("Nombre de trajets par jour:")
    print(trajets_depart)
    # Visualisation sous forme de diagramme à barres
    plt.figure(figsize=(12, 6))
    plt.bar(trajets_depart['Date'], trajets_depart['Nombre de trajets'], color='b', alpha=0.7)
    plt.title(f"Nombre total de trajets par jour pour {annee}")
    plt.xlabel('Date')
    plt.ylabel('Nombre total de trajets')
    plt.xticks(rotation=45)  
    plt.grid(axis='y')  
    plt.tight_layout() 
    plt.savefig(f"./docs/projet1_files/figure-html/Nb_trajet_par_{annee}")
    plt.close()

    # Traitement des données pour avoir un graphique avec les jours, heures et le nombre de vélos comme sur la leçon disponible sur moodle.
    df_bikes = df_coursesvelomagg_traité.set_index('Departure')
    df_bikes["Jour"] = df_bikes.index.dayofweek  #[0-6] -> Lundi - Dimanche

    # Regroupement par jour de la semaine et heure avec moyenne
    df_polar = (
        df_bikes.groupby(["Jour", df_bikes.index.hour])
        .agg(
            Total_trajets=("Covered distance (m)", "count"),
            Jours_distincts=("Date", "nunique")
        )
        .reset_index()
    )
    df_polar["Moyenne trajets"] = df_polar["Total_trajets"] / df_polar["Jours_distincts"]


    # Modification de la colonne "weekday" pour obtenir les noms complets des jours
    df_polar["Jour"] = df_polar["Jour"].apply(lambda x: calendar.day_name[x])

    # Traduire les noms complets en français
    traduction_jours_complets = {
        "Monday": "Lundi",
        "Tuesday": "Mardi",
        "Wednesday": "Mercredi",
        "Thursday": "Jeudi",
        "Friday": "Vendredi",
        "Saturday": "Samedi",
        "Sunday": "Dimanche"
    }
    df_polar["Jour"] = df_polar["Jour"].replace(traduction_jours_complets) # Traduction des jours

    # Définition des couleurs
    n_colors = 8  # Nombre de couleurs
    colors = px.colors.sample_colorscale(
        "mrybm", [n / (n_colors - 1) for n in range(n_colors)]
    )

    # Conversion des heures en degrés (0 à 360 degrés)
    df_polar['heure'] = df_polar['Departure'] * 15  # Chaque heure = 15 degrés (360/24)

    # Création de la figure
    fig = px.line_polar(
        df_polar,
        r="Moyenne trajets",  # Utiliser le nombre de trajets comme rayon
        theta="heure",  # Utiliser l'heure comme angle
        color="Jour",
        line_close=True,
        range_r=[0, df_polar["Moyenne trajets"].max() + 5],
        start_angle=0,
        color_discrete_sequence=colors,
        template="seaborn",
        title=f"Trajet journalier {annee}",
    )
    fig.update_layout(polar=dict(angularaxis=dict(tickvals=list(range(0, 360, 15)), ticktext=[f"{i}:00" for i in range(24)])))
    # Sauvegarde de la figure
    fig.write_html(f"./docs/projet1_files/figure-html/graphique_distance_jour_{annee}.html")

#%%
# Initialisation d'un dictionnaire et d'une liste 
compteur_stations_cumulé = {}
distance = []
# Script pour savoir quelles stations sont les plus utilisées et la distance moyenne parcourue en vélo au fil des années, des mois.
for i in range(4):  # Parcourir les 5 jeux de données.
    if i==0 :
        chemin ="./data/extracted/TAM_MMM_CoursesVelomagg_2021.csv"
        annee = 2021
    if i==1 :
        chemin ="./data/extracted/TAM_MMM_CoursesVelomagg_2022.csv"
        annee = 2022
    if i==2 :
        chemin ="./data/extracted/TAM_MMM_CoursesVelomagg_2023.csv"
        annee = 2023
    if i==3 :
        chemin ="./data/CoursesVelomagg.csv"
        annee = 2024
    # Traitement du dataframe
    # Extraire notre dataframe
    df_coursesvelomagg = pd.read_csv(chemin)
    if i==0:
        df_coursesvelomagg = pd.read_csv(chemin, delimiter=';') # Mal représenté
    df_coursesvelomagg_traité = df_coursesvelomagg
    # Prendre le nom de nos stations, et prendre seulement les valeurs uniques (sans doublons de station)
    Stations = df_coursesvelomagg_traité['Departure station']
    Stations = Stations.unique()
    # Compter le nombre de trajet vers une station.
    compteur_stations = {station: 0 for station in Stations}
    for station in Stations:
        trajet_vers_station = df_coursesvelomagg_traité['Return station'].value_counts().get(station, 0)
        # Ajouter ou mettre à jour le compteur dans le dictionnaire 
        if station in compteur_stations_cumulé:
            compteur_stations_cumulé[station] += trajet_vers_station
        else:
            compteur_stations_cumulé[station] = trajet_vers_station
    
    # PARTIE SUR LA DISTANCE -  On compte la distance moyenne par mois/années et on trace
    df_coursesvelomagg_traité['Departure'] = pd.to_datetime(df_coursesvelomagg_traité['Departure']) # Format datetime
    # Extraire le mois et l'année de la colonne 'Departure'
    df_coursesvelomagg_traité['Mois'] = df_coursesvelomagg_traité['Departure'].dt.to_period('M')  # 'M' pour mois
    # Calculer la somme de la distance parcourue par mois et conversion en kilomètre.
    nombre_trajets_par_mois = df_coursesvelomagg_traité.groupby('Mois')['Covered distance (m)'].count()
    somme_distance_par_mois = ((df_coursesvelomagg_traité.groupby('Mois')['Covered distance (m)'].sum())/1000)/nombre_trajets_par_mois
    # Ajouter une colonne pour l'année pour chaque mois
    somme_distance_par_mois = somme_distance_par_mois.reset_index()
    somme_distance_par_mois['Annee'] = annee
    distance.append(somme_distance_par_mois)

# On garde les stations qui ont plus de n trajets car sinon la représentation n'est pas lisible.        
compteur_stations_cumulé = dict(filter(lambda item: item[1] >= 20000, compteur_stations_cumulé.items()))
# Tracer le graphique
stations = list(compteur_stations_cumulé.keys())  # Stations sur l'axe des x
trajets = list(compteur_stations_cumulé.values())  # Nombre de trajets sur l'axe des y
# Tracer pour les stations
# Création du graphique
plt.figure(figsize=(10, 6))
plt.bar(stations, trajets, color='skyblue')
plt.xlabel('Stations')
plt.ylabel('Nombre de trajets')
plt.title('Nombre total de trajets vers chaque station')
plt.xticks(rotation=45, ha="right")
# Afficher le graphique
plt.savefig("./docs/projet1_files/figure-html/StationStat")
plt.close()


# Fusionner toutes les années dans un seul DataFrame
df_distance = pd.concat(distance)
df_distance.reset_index()
df_distance = df_distance.drop_duplicates(['Mois'])
print(df_distance)
# Tracer un seul graphique avec toutes les distances de 2021 à 2024
plt.figure(figsize=(12, 6))

# Tracer chaque année
for annee in [2021, 2022, 2023, 2024]:
    x = df_distance[df_distance['Annee'] == annee]
    plt.plot(x['Mois'].astype(str), x['Covered distance (m)'], marker='o')

# plot
plt.xlabel('Mois')
plt.ylabel('Distance parcourue en moyenne (km)')
plt.title('Distance parcourue en moyenne par mois de 2021 à 2024')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.grid(True)
plt.savefig("./docs/projet1_files/figure-html/Distance_par_mois_2021_2024.png")
plt.close()

# %%
