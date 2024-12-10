import osmnx as ox
import folium
import requests
import json

# Définir l'endroit
ville = "Montpellier, France"

# Récupérer le polygone des limites de Montpellier
frontiere = ox.geocode_to_gdf(ville)

# Obtenir les coordonnées du centre de Montpellier
location = ox.geocode(ville)

# Créer une carte Folium
m = folium.Map(location=location, zoom_start=14)

# Extraire les coordonnées des limites de la ville
coords = frontiere.geometry.values[0].exterior.coords[:]
# Tracer le polygone
folium.Polygon(
    locations=[(lat, lon) for lon, lat in coords],  # (lat, lon)
    color='black',
    fill=False,
    weight=2.5,  # Épaisseur de la bordure
).add_to(m)

# URL de l'API
url = "https://portail-api-data.montpellier3m.fr/bikestation?limit=1000"
# Envoi de la requête GET
fichier = requests.get(url, headers={"accept": "application/json"})
# Vérifier si la requête a réussi
if fichier.status_code == 200:
    data = fichier.json()  # Extraire les données JSON
    chemin = "./data/json/stationvelo.json"
    # Sauvegarder les données dans un fichier JSON
    with open(chemin, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    # Ouvrir et lire le fichier JSON pour vérifier
    with open(chemin, "r", encoding="utf-8") as file:
        data = json.load(file)  # Charger les données depuis le fichier
    # Afficher les données pour vérifier
    print(json.dumps(data, ensure_ascii=False, indent=4))  # Affichage formaté

# Ajouter des marqueurs avec les informations sur les vélos disponibles dans le popup
for station in data:
    # Extraire l'adresse, le nombre de vélos disponibles et le nombre de places libres
    address = station['address']['value']['streetAddress']
    velo_present = station['availableBikeNumber']['value']
    total_place = station['freeSlotNumber']['value']
    if total_place > 0:  # Eviter la division par zéro
        rapport = (velo_present / total_place) * 100
    else:
        rapport = 0  # Si aucune place disponible, le pourcentage est 0
    # Créer le texte à afficher dans le popup avec du HTML pour l'agrandir
    if rapport > 100:
        popup_text = f"""
        <div style="font-size: 14px; font-weight: bold; color: black;">
            <p><b>Station:</b> {address}</p>
            <p><b>Vélos disponibles:</b> {rapport}</p>
            <p><b>Vélos total:</b> {total_place}</p>
        </div>
        """
    else:
        popup_text = f"""
        <div style="font-size: 14px; font-weight: bold; color: black;">
            <p><b>Station:</b> {address}</p>
            <p><b>Vélos disponibles:</b> {velo_present}</p>
            <p><b>Vélos total:</b> {total_place}</p>
            <p><b>Pourcentage de vélos disponibles:</b> {rapport:.2f}%</p>
        </div>
        """
    
    # Extraire les coordonnées de chaque station
    coords = station['location']['value']['coordinates']
    
    # Ajouter un marqueur avec ces informations dans le popup
    folium.Marker(
        location=(coords[1], coords[0]),  # (lat, lon)
        popup=folium.Popup(popup_text, max_width=300),  # Utiliser un popup plus grand avec max_width
        icon=folium.Icon(color='blue', icon='info-sign')  # Icône personnalisée
    ).add_to(m)


# Sauvegarder la carte dans un fichier HTML
m.save('./docs/index_files/montpellier_bike_stations_map.html')

# Afficher un message de confirmation
print("Carte avec les bornes de vélo enregistrée sous le nom 'montpellier_bike_stations_map.html'.")
