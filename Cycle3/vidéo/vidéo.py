import pandas as pd
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from concurrent.futures import ThreadPoolExecutor
import sys
import os
# Ajouter la racine du projet au chemin Python
racine_du_projet = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, racine_du_projet)
from src.fonctions_basedonnees import *
import datetime
coordonne.cache_clear()

#Recupère le dataframe créer lors du fichier map_trajet_BD.py
data = pd.read_csv("./data/video.csv").dropna()

#Traitement de cette nouvelle base de donnée pour optimiser la vidéo.
#On enlève les trajets vers AtelierTAM
data= data[data['Departure station'] != 'AtelierTAM']
data= data[data['Return station'] != 'AtelierTAM']
data = data.dropna(subset=['Duration (sec.)'])
data['Departure'] = pd.to_datetime(data['Departure']) 
data = data.sort_values(by='Departure', ascending=True)      # trie par date
data.reset_index(drop=True, inplace=True)                    # Nouvelle numérotation

# Obtenir les noms de stations uniques
unique_stations = data['Departure station'].unique()

# Dictionnaire pour stocker les coordonnées de chaque station
station_coordinates = {}

# Récupérer les coordonnées pour chaque station unique
for station in unique_stations:
    lat, lon = coordonne(station)
    station_coordinates[station] = (lat, lon)

# Ajouter les colonnes de coordonnées pour les stations de départ et d'arrivée
data['latitude_depart'] = data['Departure station'].map(lambda x: station_coordinates.get(x, (None, None))[0])
data['longitude_depart'] = data['Departure station'].map(lambda x: station_coordinates.get(x, (None, None))[1])
data['latitude_retour'] = data['Return station'].map(lambda x: station_coordinates.get(x, (None, None))[0])
data['longitude_retour'] = data['Return station'].map(lambda x: station_coordinates.get(x, (None, None))[1])

# Sauvegarder le fichier avec les nouvelles colonnes de coordonnées
data.to_csv("./data/video_avec_coord.csv", index=False)
# Sélectionner les trajets en fonction du nombre demandé
nombre_lignes = len(data)
print(f"Le DataFrame contient {nombre_lignes} lignes.")
min_trajets = int(input("Combien de trajets voulez-vous afficher sur votre journée ? "))
df = data.iloc[:min_trajets]  # Sélectionne les min_trajets premières lignes, où min_trajets est le nombre spécifié
df.reset_index(drop=True, inplace=True)


# Créer le répertoire s'il n'existe pas
output_dir = "./Cycle3/visualisation"
os.makedirs(output_dir, exist_ok=True)


# Charger le réseau routier de Montpellier depuis OpenStreetMap
G = ox.graph_from_place("Montpellier, France", network_type="all")

# Date du jour
date = data.loc[0, 'Departure'].strftime("%Y-%m-%d")  # Format YYYY-MM-DD
titre = f"Visualisation des trajets du {date}"


# Initialisation de la figure
fig, ax = ox.plot_graph(G, show=False, close=False, node_size=0, edge_color="gray", edge_linewidth=0.5)

# Ajouter un texte dans la vidéo
titre_ds_video = fig.text(0.5, 0.95, titre, fontsize=16, color="blue", ha="center", va="top")

# Fonction chemin plus court

def chemin_court(row):
    """
    Description :
    La fonction `chemin_court` calcule le chemin le plus court entre deux points géographiques spécifiés par les colonnes d'une ligne de données. 
    Elle utilise un graphe défini globalement (`G`) pour déterminer le chemin le plus court en termes de distance pondérée.

    Args :
    - row : dictionnaire
    Returns :
    - tuple : (list, int)
        - Une liste représentant le chemin le plus court en termes de nœuds entre le point de départ et le point d'arrivée.
        - La durée du trajet en secondes, issue de la colonne `Duration (sec.)` de la ligne.
        Si une erreur survient, la fonction retourne `(None, None)`.
    """
    try:
        depart_lat, depart_lon = row['latitude_depart'], row['longitude_depart']
        arrivee_lat, arrivee_lon = row['latitude_retour'], row['longitude_retour']
        duration = row['Duration (sec.)']
        
        noeud_deb = ox.distance.nearest_nodes(G, depart_lon, depart_lat)
        noeud_fin = ox.distance.nearest_nodes(G, arrivee_lon, arrivee_lat)
        
        chemin = nx.shortest_path(G, noeud_deb, noeud_fin, weight="length")
        return chemin, duration
    except Exception as e:
        print(f"Erreur pour le trajet entre {row['Departure station']} et {row['Return station']}: {e}")
        return None, None

# Calcul des trajets en parallèle
with ThreadPoolExecutor() as executor:
    results = list(executor.map(chemin_court, [row for _, row in df.iterrows()]))

# Filtrer les chemins valides
paths, durations = zip(*[(path, duration) for path, duration in results if path is not None])

# Préparer les points pour l'animation
points = [ax.plot([], [], 'o', color="yellow", alpha=0.7, markersize=3)[0] for _ in paths]

# Durée souhaitée de la vidéo en secondes et réglage des FPS
dure_cible = 20  # Durée souhaitée de la vidéo
fps = 30                       # FPS cible pour la vidéo
total_frames = dure_cible * fps  # Calcul du nombre total de frames nécessaires
dure_frame = max(durations) / total_frames  # Durée par frame


# Fonction d'initialisation

def init():
    """
    Description :
    La fonction `init` initialise les données associées à une liste d'objets `points`. 
    Elle efface les données des points en les remplaçant par des listes vides pour les axes x et y.

    Args :
    Returns :
    - list
        Une liste des objets `points` après avoir réinitialisé leurs données.

   """
    for point in points:
        point.set_data([], [])
    return points 


# Fonction de mise à jour pour chaque frame

def update(frame):
    """
    Description :
    La fonction `update` met à jour les positions d'une liste de points au fur et à mesure d'une animation, en fonction de la progression d'un chemin dans un graphe. 
    Elle déplace chaque point le long de son chemin associé, calculé à partir des nœuds du graphe.

    Args :
    - frame : int
        Le numéro de la frame actuelle dans l'animation. Il est utilisé pour calculer la progression sur le chemin.

    Returns :
    - list
        Une liste des objets `points` après avoir mis à jour leurs positions.
    """
    for i, path in enumerate(paths):
        progress = min(frame / total_frames, 1)  # Progression en fonction de total_frames
        num_nodes = int(progress * len(path))

        if num_nodes > 0:
            current_node = path[num_nodes - 1]
            x, y = G.nodes[current_node]['x'], G.nodes[current_node]['y']
            points[i].set_data([x], [y])

    return points 

# Créer et sauvegarder l'animation
ani = FuncAnimation(fig, update, frames=range(total_frames), init_func=init, blit=False, repeat=False)
output_dir = "./Cycle3/visualisation"
os.makedirs(output_dir, exist_ok=True)
writer = FFMpegWriter(fps=fps)
ani.save(os.path.join(output_dir, "simulation_trajets.mp4"), writer=writer)
print("La simulation a été sauvegardée sous forme de vidéo : simulation_trajets.mp4")

