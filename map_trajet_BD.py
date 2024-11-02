# Map lié à la base de donnée.

import osmnx as ox
import folium
import networkx as nx
import pandas as pd
from src.fonctions_basedonnees import*

# Ville ciblée pour extraire les données du réseau de routes cyclables
ville = "Montpellier, France"
G = ox.graph_from_place(ville, network_type="all")
# Créer une carte globale centrée sur Montpellier
m = folium.Map(location=[43.6114, 3.8767], zoom_start=13)  # Coordonnées du centre Montpellier

#Extraire notre dataframe
df_coursesvelomagg_traité = pd.read_csv("../data/CoursesVelomagg.csv").dropna()

# Extraire les trajets avec les noms des stations aller et le nom des stations retours
liste_des_trajets = df_coursesvelomagg_traité[['Departure','Departure station', 'Return station','Covered distance (m)', 'Duration (sec.)']]

#Convertir + nettoyer les colonnes
#Convertie les donnée date en datetime pour que la machine puisse comprendre les dates
liste_des_trajet_DBF =liste_des_trajets #pd_to_datetime(df_coursesvelomagg_traité, 'Departure')
#Nettoie le dataframe des mauvais caractère qui bruitent l'analyse
liste_des_trajet_DBF['Departure station'] = liste_des_trajet_DBF['Departure station'].apply(nettoyer_adresse_normalise)
liste_des_trajet_DBF['Return station'] = liste_des_trajet_DBF['Return station'].apply(nettoyer_adresse_normalise)

# Traite un cas particulier.
# Remplacer les valeurs dans les colonnes 'Departure station' et 'Return station'
liste_des_trajet_DBF['Departure station'] = liste_des_trajet_DBF['Departure station'].replace("FacdesSciences", "Faculté des sciences")
liste_des_trajet_DBF['Return station'] = liste_des_trajet_DBF['Return station'].replace("FacdesSciences", "Faculté des sciences")


Liste_des_dates = liste_des_trajet_DBF['Departure'].str[:10].unique()
print(Liste_des_dates)

# Interaction avec l'utilisateur
date = input("Veuillez choisir une date parmi la liste des dates (AAAA-MM-JJ) : ")

# Sélectionner les trajets du jour
trajets_du_jour = liste_des_trajet_DBF[liste_des_trajet_DBF['Departure'].str.startswith(date)]
nb_ref = len(trajets_du_jour)
print(f"Nous avons {nb_ref} référence(s) à cette date.")

# Demander si l'utilisateur souhaite tracer les trajets
a = input("Voulez-vous les tracer (oui/non) ? ")
if a.lower() == "oui":
    # Demander combien de trajets afficher
    min_trajets = int(input("Combien de trajets voulez-vous afficher sur votre journée ? "))
    
    # Boucle pour afficher les trajets (limité au nombre de trajets disponibles)
    for i in range(min(min_trajets, nb_ref)): 
        print(f"Affichage du trajet {i+1}")
        gen_carte_trajet(trajets_du_jour.iloc[i], G, m, 1, 2)  # Ajout de la carte de chaque trajet à la carte globale

# Sauvegarder la carte dans un fichier HTML
m.save("./visualisation/carte_montpellier_trajet_via_BD.html")

# Afficher un message pour indiquer que la carte est prête
print("La carte a été sauvegardée sous './visualisation/carte_montpellier_trajet_via_BD.html'.")







# Partie vidéo





import pandas as pd
import osmnx as ox
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go

data = trajets_du_jour[['Departure', 'Departure station', 'Return station', 'Covered distance (m)', 'Duration (sec.)']]
data.to_csv('./data/video.csv', index=False)

# Obtenir les noms de stations uniques (départ et arrivée)
unique_stations = data['Departure station'].unique()

# Dictionnaire pour stocker les coordonnées de chaque station
station_coordinates = {}

# Récupérer les coordonnées pour chaque station unique
for station in unique_stations:
    lat, lon = coordonne(station)
    station_coordinates[station] = (lat, lon)
    print(f"Station: {station} - Latitude: {lat}, Longitude: {lon}")

# Ajouter les colonnes de coordonnées pour les stations de départ et d'arrivée
data['latitude_depart'] = data['Departure station'].map(lambda x: station_coordinates.get(x, (None, None))[0])
data['longitude_depart'] = data['Departure station'].map(lambda x: station_coordinates.get(x, (None, None))[1])
data['latitude_retour'] = data['Return station'].map(lambda x: station_coordinates.get(x, (None, None))[0])
data['longitude_retour'] = data['Return station'].map(lambda x: station_coordinates.get(x, (None, None))[1])

# Sauvegarder le fichier avec les nouvelles colonnes de coordonnées
data.to_csv("./data/video_avec_coord.csv", index=False)
df = data.iloc[[2]]
df.reset_index(drop=True, inplace=True)
# Définir les coordonnées de départ et d'arrivée à partir de votre DataFrame
lat_start = df['latitude_depart'][0]
lon_start = df['longitude_depart'][0]
lat_end = df['latitude_retour'][0]
lon_end = df['longitude_retour'][0]

# Créer un graphe des routes pour Montpellier
G = ox.graph_from_place('Montpellier, France', network_type='drive')

# Trouver le nœud le plus proche de départ et d'arrivée
orig_node = ox.distance.nearest_nodes(G, lon_start, lat_start)
dest_node = ox.distance.nearest_nodes(G, lon_end, lat_end)

# Calculer le plus court chemin
route = nx.shortest_path(G, orig_node, dest_node, weight='length')

# Extraire les coordonnées du chemin
route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
latitudes, longitudes = zip(*route_coords)

# Créer un DataFrame pour Plotly
animation_data = pd.DataFrame({
    'latitude': latitudes,
    'longitude': longitudes,
    'frame': range(len(latitudes))
})

# Créer l'animation avec Plotly
fig = go.Figure()

# Ajouter les frames
for k in range(len(animation_data)):
    fig.add_trace(go.Scattergeo(
        lat=animation_data['latitude'][:k+1],
        lon=animation_data['longitude'][:k+1],
        mode='markers+lines',
        marker=dict(size=8, color='red'),
        line=dict(width=2, color='blue'),
        showlegend=False
    ))

# Mettre à jour le layout pour centrer sur Montpellier
fig.update_layout(
    title='Animation du trajet à Montpellier',
    geo=dict(
        scope='europe',  # Garder comme scope pour l'Europe
        projection_type='mercator',
        center=dict(lat=43.6119, lon=3.8772),  # Coordonnées de Montpellier
        projection=dict(scale=10),  # Ajuster le scale pour bien voir la région
        showland=True,
        landcolor='lightgray',
        countrycolor='gray',
        lataxis=dict(showgrid=True, gridcolor='white', range=[43.5, 43.7]),  # Limites de latitude
        lonaxis=dict(showgrid=True, gridcolor='white', range=[3.6, 4.1])  # Limites de longitude
    )
)

# Ajouter un bouton pour l'animation
fig.update_layout(
    updatemenus=[{
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'mode': 'immediate'}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }]
)

# Afficher la figure
fig.show()