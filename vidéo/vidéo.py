
import pandas as pd
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from concurrent.futures import ThreadPoolExecutor
from src.fonctions_basedonnees import *
coordonne.cache_clear()

#Recupère le dataframe créer lors du fichier map_trajet_BD.py
data = pd.read_csv("./data/video.csv").dropna()

# Obtenir les noms de stations uniques (départ et arrivée)
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
df = data.iloc[:min_trajets]  # Sélectionne les n premières lignes, où n est le nombre spécifié
df.reset_index(drop=True, inplace=True)


# Créer le répertoire s'il n'existe pas
output_dir = "./visualisation"
os.makedirs(output_dir, exist_ok=True)


# Charger le réseau routier de Montpellier depuis OpenStreetMap
G = ox.graph_from_place("Montpellier, France", network_type="all")

# Initialisation de la figure
fig, ax = ox.plot_graph(G, show=False, close=False, node_size=0, edge_color="gray", edge_linewidth=0.5)

# Fonction chemin plus court
def chemin_court(row):
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

# Préparer les lignes pour l'animation
lines = [ax.plot([], [], color="yellow", alpha=0.7, linewidth=1)[0] for _ in paths]

# Fonction d'initialisation
def init():
    for line in lines:
        line.set_data([], [])
    return lines

# Fonction de mise à jour pour chaque frame
def update(frame):
    for i, path in enumerate(paths):
        progress = min(frame / (durations[i] // 4), 1)
        num_nodes = int(progress * len(path))
        
        if num_nodes > 1:
            x, y = zip(*[(G.nodes[node]['x'], G.nodes[node]['y']) for node in path[:num_nodes]])
            lines[i].set_data(x, y)
    
    return lines

# Animation
max_duration = max(durations) // 4 if durations else 100
ani = FuncAnimation(fig, update, frames=range(int(max_duration)), init_func=init, blit=False, repeat=False)

# Sauvegarder la vidéo
writer = FFMpegWriter(fps=15)
ani.save(os.path.join(output_dir, "simulation_trajets.mp4"), writer=writer)
print("La simulation a été sauvegardée sous forme de vidéo : simulation_trajets.mp4")