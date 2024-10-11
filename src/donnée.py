#Import des packages, basé sur le cour de développement logiciel
import os
import numpy as np
import calendar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler
import pooch  # download data / avoid re-downloading
from IPython import get_ipython
sns.set_palette("colorblind")
palette = sns.color_palette("twilight", n_colors=12)
pd.options.display.max_rows = 8

#Téléchargement du fichier Courses des vélos VéloMagg de Montpellier Méditerranée Métropole
#Sur le site https://data.montpellier3m.fr/dataset/courses-des-velos-velomagg-de-montpellier-mediterranee-metropole
url = "https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_CoursesVelomagg.csv"
path_target = "./data/CoursesVelomagg.csv"
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)


#Permet de lire la dataframe
df_coursesvelomagg = pd.read_csv("CoursesVelomagg.csv")
#Permet d'enlever les valeurs NaN ou les manques de données
df_coursesvelomagg_traité = df_coursesvelomagg.dropna()


#Pour traiter les données sur la date
# Convertir la colonne 'Departure' en datetime
df_coursesvelomagg_traité['Departure'] = pd.to_datetime(df_coursesvelomagg_traité['Departure'])
# Extraire les dates de départ
df_coursesvelomagg_traité['Date'] = df_coursesvelomagg_traité['Departure'].dt.date

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
plt.title('Nombre total de trajets par jour (départs)')
plt.xlabel('Date')
plt.ylabel('Nombre total de trajets')
plt.xticks(rotation=45)  # Rotation des étiquettes sur l'axe des x pour une meilleure lisibilité
plt.grid(axis='y')  # Ajouter une grille horizontale pour une meilleure lisibilité
plt.tight_layout()  # Pour ajuster les marges
plt.show()
