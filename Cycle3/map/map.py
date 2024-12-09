import osmnx as ox
import folium
import networkx as nx

# Ville ciblée pour extraire les données du réseau de routes cyclables
ville = "Montpellier, France"
G = ox.graph_from_place(ville, network_type="all")

# Import des noms de stations de vélos
stations = ox.geometries_from_place(ville, tags={'amenity': 'bicycle_rental'})
stations = stations['name'].dropna()
Liste_des_stations = stations.tolist()
print(Liste_des_stations)

def choisir_station(prompt):
    """
    Description :
    La fonction `choisir_station` permet à l'utilisateur de choisir une station parmi une liste prédéfinie appelée `Liste_des_stations`. 
    Si l'utilisateur entre une station invalide, la fonction affiche un message d'erreur et redemande la saisie jusqu'à ce qu'une station valide soit sélectionnée.

    Args :
    - prompt : str
        Un message affiché à l'utilisateur pour lui demander de saisir une station.

    Returns:
    - str
        La station sélectionnée par l'utilisateur, qui est un élément valide de `Liste_des_stations`.
    """
    while True:
        choix = input(prompt)
        if choix in Liste_des_stations:
            return choix
        else:
            print(f"'{choix}' n'est pas dans la liste des stations. Veuillez choisir parmi : {Liste_des_stations}")

# Utilisation de ox.geocode() pour obtenir les coordonnées de l'origine et de la destination
départ = choisir_station("Entrez le lieu de départ : ")
arrivé = choisir_station("Entrez le lieu d'arrivée : ")

# Ajout de ", Montpellier, France" pour s'assurer du géocodage correct
origin = ox.geocode(f"{départ}, Montpellier, France")
destination = ox.geocode(f"{arrivé}, Montpellier, France")

# Trouver les noeuds les plus proches de l'origine et de la destination
origin_node = ox.nearest_nodes(G, origin[1], origin[0])
destination_node = ox.nearest_nodes(G, destination[1], destination[0])

# Afficher les coordonnées de l'origine et de la destination
print("Origine:", origin)
print("Destination:", destination)

# Calculer l'itinéraire aller et retour
route = ox.shortest_path(G, origin_node, destination_node)
route_back = ox.shortest_path(G, destination_node, origin_node)

# Fonction pour convertir un itinéraire (liste de noeuds) en liste de coordonnées géographiques
def route_to_coords(G, route):
    """
    Description :
    La fonction `route_to_coords` convertit une liste de noeuds représentant une route dans un graphe en une liste de coordonnées géographiques (latitude, longitude).

    Args :
    - G : networkx.Graph
        Un graphe contenant des informations sur les noeuds. Chaque noeud doit avoir des attributs 'x' (longitude) et 'y' (latitude).
    - route : list
        Une liste de noeuds représentant une route dans le graphe `G`.

    Returns: :
    - list of tuple
        Une liste de tuples contenant les coordonnées géographiques (latitude, longitude) pour chaque noeud de la route.
    """
    route_coords = []
    for node in route:
        point = (G.nodes[node]['y'], G.nodes[node]['x'])  # latitude, longitude
        route_coords.append(point)
    return route_coords

# Obtenir les coordonnées pour l'itinéraire aller et retour
route_coords = route_to_coords(G, route)
route_back_coords = route_to_coords(G, route_back)

# Créer la carte centrée sur l'origine
m = folium.Map(location=[origin[0], origin[1]], zoom_start=13)

# Ajouter l'itinéraire aller (en rouge) à la carte
folium.PolyLine(locations=route_coords, color='red', weight=5, opacity=0.75).add_to(m)

# Ajouter l'itinéraire retour (en bleu) à la carte
folium.PolyLine(locations=route_back_coords, color='blue', weight=5, opacity=0.75).add_to(m)

# Ajouter des marqueurs pour l'origine et la destination
folium.Marker(location=[origin[0], origin[1]], popup="Origine").add_to(m)
folium.Marker(location=[destination[0], destination[1]], popup="Destination").add_to(m)

# Sauvegarder la carte dans un fichier HTML
m.save("./Cycle3/visualisation/carte_montpellier_trajet.html")

# Afficher un message pour indiquer que la carte est prête
print("La carte a été sauvegardée sous 'carte_montpellier.html'.")


