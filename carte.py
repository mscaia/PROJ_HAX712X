import osmnx as ox
import folium

# Définir l'endroit
ville = "Montpellier, France"

# Télécharger les stations de vélo
stations = ox.geometries_from_place(ville, tags={'amenity': 'bicycle_rental'})

# Vérifier que des stations de vélo ont été récupérées
print("On a trouvé", len(stations),"stations de vélos")

# Récupérer le polygone des limites de Montpellier
frontiere = ox.geocode_to_gdf(ville)

# Obtenir les coordonnées du centre de Montpellier
location = ox.geocode(ville)
print(location)

# Créer une carte Folium
m = folium.Map(location=location, zoom_start=14)

# Ajouter des marqueurs pour les stations de vélo
for _, station in stations.iterrows():
    # Extraire les coordonnées
    coords = station.geometry.coords[0]
    
    # Récupérer le nom de la station
    station_name = station.get('name', 'Station de vélo sans nom')
    
    folium.CircleMarker(
        location=(coords[1], coords[0]),  # (lat, lon)
        radius=6,  # Taille du cercle
        color='green',  # Couleur du cercle
        fill=True,
        fill_color='red',
        fill_opacity=0.7,
        popup=station_name  # Nom de la station à afficher dans la fenêtre contextuelle
    ).add_to(m)


# Extraire les coordonnées des limites de la ville
coords = frontiere.geometry.values[0].exterior.coords[:]
# Tracer le polygone
folium.Polygon(
    locations=[(lat, lon) for lon, lat in coords],  # (lat, lon)
    color='black',
    fill=False,
    weight=2.5,  # Épaisseur de la bordure
).add_to(m)



# Sauvegarder la carte dans un fichier HTML
m.save('./visualisation/montpellier_bike_stations_map.html')

# Afficher un message de confirmation
print("Carte avec les bornes de vélo enregistrée sous le nom 'montpellier_bike_stations_map.html'.")
