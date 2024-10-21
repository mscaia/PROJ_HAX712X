# Map lié à la base de donnée.

import osmnx as ox
import folium
import networkx as nx
import pandas as pd
from src.fonctions_basedonnees import*
# Ville ciblée pour extraire les données du réseau de routes cyclables
ville = "Montpellier, France"
G = ox.graph_from_place(ville, network_type="all")

df_coursesvelomagg_traité = pd.read_csv("../data/CoursesVelomagg.csv").dropna()
# Extraire les trajets avec les noms des stations aller et le nom des stations retours
liste_des_trajets = df_coursesvelomagg_traité = df_coursesvelomagg_traité[['Departure','Departure station', 'Return station']]
liste_des_dates = pd_to_datetime(df_coursesvelomagg_traité, 'Departure')
