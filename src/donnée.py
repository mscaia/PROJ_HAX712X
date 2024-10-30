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
import json
sns.set_palette("colorblind")
palette = sns.color_palette("twilight", n_colors=12)
pd.options.display.max_rows = 8


#Import des données

# 1er jeu de données
#Téléchargement du fichier Courses des vélos VéloMagg de Montpellier Méditerranée Métropole
#Sur le site https://data.montpellier3m.fr/dataset/courses-des-velos-velomagg-de-montpellier-mediterranee-metropole
url = "https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_CoursesVelomagg.csv"
path_target = "../data/CoursesVelomagg.csv"
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)
#Permet de lire la dataframe
df_coursesvelomagg = pd.read_csv("../data/CoursesVelomagg.csv")
#Permet d'enlever les valeurs NaN ou les manques de données
df_coursesvelomagg_traité = df_coursesvelomagg.dropna()

#2ème jeu de données
url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_GeolocCompteurs.csv"
path_target = "../data/GeolocCompteurs.csv"
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)
#Permet de lire la dataframe
df_GeolocCompteurs = pd.read_csv("../data/GeolocCompteurs.csv")
#Permet d'enlever les valeurs NaN ou les manques de données
df_GeolocCompteurs_traité = df_GeolocCompteurs.dropna()

#3è jeu de données

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H19070220_archive.json"
path_target = "../data/EcoCompt1.json"
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)