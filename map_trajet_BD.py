# Map lié à la base de donnée.

import osmnx as ox
import folium
import networkx as nx
import pandas as pd

# Ville ciblée pour extraire les données du réseau de routes cyclables
ville = "Montpellier, France"
G = ox.graph_from_place(ville, network_type="all")

df_coursesvelomagg_traité = pd.read_csv("../data/CoursesVelomagg.csv").dropna()

