import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import calendar
import kaleido
import numpy as np


for i in range(5):
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
    #Extraire notre dataframe
    df_coursesvelomagg = pd.read_csv(chemin)
    if i==1:
        df_coursesvelomagg = pd.read_csv(chemin, delimiter=';')
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
    plt.xticks(rotation=45)  # Rotation des étiquettes sur l'axe des x pour une meilleure lisibilité
    plt.grid(axis='y')  # Ajouter une grille horizontale pour une meilleure lisibilité
    plt.tight_layout()  # Pour ajuster les marges
    plt.savefig(f"./images/Nbr_trajet_par_jour_{annee}")
    plt.show()



    # Traitement donnée pour avoir un graphique avec les jours,heures et le nombre de vélo

    df_bikes = df_coursesvelomagg_traité.set_index('Departure')
    df_bikes["weekday"] = df_bikes.index.dayofweek  # Monday=0, Sunday=6
    print(df_bikes.index.hour)

    # Regroupement par jour de la semaine et heure
    df_polar = (
        df_bikes.groupby(["weekday", df_bikes.index.hour])["Covered distance (m)"]
        .count()
        .reset_index(name='Count')  # Renommer la colonne résultante
    )

    # Modification de la colonne "weekday" pour obtenir les abréviations
    df_polar["weekday"] = df_polar["weekday"].apply(lambda x: calendar.day_abbr[x])

    # Définition des couleurs
    n_colors = 8  # Nombre de couleurs
    colors = px.colors.sample_colorscale(
        "mrybm", [n / (n_colors - 1) for n in range(n_colors)]
    )

    # Conversion des heures en degrés (0 à 360 degrés)
    df_polar['heure'] = df_polar['Departure'] * 15  # Chaque heure = 15 degrés

    # Création de la figure
    fig = px.line_polar(
        df_polar,
        r="Count",  # Utilisez le nombre de trajets comme rayon
        theta="heure",  # Utilisez l'heure comme angle
        color="weekday",
        line_close=True,
        range_r=[0, df_polar["Count"].max() + 50],
        start_angle=0,
        color_discrete_sequence=colors,
        template="seaborn",
        title=f"Trajet journalier {annee}",
    )
    fig.update_layout(polar=dict(angularaxis=dict(tickvals=list(range(0, 360, 15)), ticktext=[f"{i}:00" for i in range(24)])))
    # Sauvegarde de la figure
    fig.write_html(f"./images/graphique_distance_jour_{annee}.html")
    fig.show()