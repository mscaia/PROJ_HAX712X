
import pandas as pd
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from concurrent.futures import ThreadPoolExecutor
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
data = data.sort_values(by='Departure', ascending=True)
data.reset_index(drop=True, inplace=True)

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

# Préparer les points pour l'animation
points = [ax.plot([], [], 'o', color="yellow", alpha=0.7, markersize=3)[0] for _ in paths]

# Définir le texte pour l'heure en haut de la vidéo
start_time = df['Departure'].min()  # Heure de départ la plus ancienne
time_text = ax.text(0.5, 1.05, '', transform=ax.transAxes, ha='center', fontsize=12, color="black")

# Durée souhaitée de la vidéo en secondes et réglage des FPS
desired_duration_seconds = 20  # Durée souhaitée de la vidéo
fps = 30                       # FPS cible pour la vidéo
total_frames = desired_duration_seconds * fps  # Calcul du nombre total de frames nécessaires
frame_duration = max(durations) / total_frames  # Durée par frame


# Fonction d'initialisation
def init():
    for point in points:
        point.set_data([], [])
    time_text.set_text('')
    return points + [time_text]


# Fonction de mise à jour pour chaque frame
def update(frame):
    # Calculer l'heure actuelle
    current_time = start_time + datetime.timedelta(seconds=frame * frame_duration)
    time_text.set_text(current_time.strftime('%Y-%m-%d %H:%M:%S'))

    for i, path in enumerate(paths):
        progress = min(frame / total_frames, 1)  # Progression en fonction de total_frames
        num_nodes = int(progress * len(path))

        if num_nodes > 0:
            current_node = path[num_nodes - 1]
            x, y = G.nodes[current_node]['x'], G.nodes[current_node]['y']
            points[i].set_data([x], [y])

    return points + [time_text]

# Créer et sauvegarder l'animation
ani = FuncAnimation(fig, update, frames=range(total_frames), init_func=init, blit=False, repeat=False)
output_dir = "./visualisation"
os.makedirs(output_dir, exist_ok=True)
writer = FFMpegWriter(fps=fps)
ani.save(os.path.join(output_dir, "simulation_trajets.mp4"), writer=writer)
print("La simulation a été sauvegardée sous forme de vidéo : simulation_trajets.mp4")