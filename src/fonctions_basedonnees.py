import csv 
import matplotlib.pyplot as plt 
import numpy as np 

import os
import pooch
import pandas as pd
import json
import re
import unicodedata
import folium
import osmnx as ox

#importer les données 
filename1= 'MMM_MMM_GeolocCompteurs.csv'
filename2='TAM_MMM_CoursesVelomagg.csv'

#Fonction qui donne le colonne i du tableau voulu: 
def colonne(i, w_file):
    L=[]
    with open(w_file) as f:
        for line in f:
            x=line.split(";")
            L.append(x[i])
    return L         

#Fonction qui retourne toutes les valeurs dans la colonne j quand l'argument de la colonne i est k 
def arg(k,i,j, w_file):
    L=[]
    with open(w_file) as f:
        for line in f:
            x=line.split(";")
            if x[i]==k:
                L.append(x[j])
    return L 

# Fonction qui permet de transforme les donnée date du dataframe en donnée exploitable.
def pd_to_datetime(df, colonne_date):
    df = df.dropna()
    df[colonne_date] = pd.to_datetime(df[colonne_date])
    df['Date'] = df[colonne_date].dt.date
    df = df.drop(columns=[colonne_date])
    return df

#Fonction qui permet d'enleve les bruits dans les chaines de caractère d'un dataframe
def nettoyer_adresse_normalise(adresse):
    """
    Nettoie et normalise une adresse en supprimant les numéros au début, 
    en normalisant les caractères Unicode.
    
    Paramètre :
    adresse (str) : La chaîne d'adresse à normaliser.
    
    Retourne :
    str : L'adresse nettoyée et normalisée.
    """
    # Tenter de corriger l'encodage si nécessaire
    try:
        # Encode la chaîne en latin1 puis décode en utf-8
        adresse = adresse.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass  # Ignore les erreurs d'encodage si elles se produisent

    # Supprimer les numéros ou autres formats non pertinents (ex: 057 au début)
    adresse = re.sub(r'^\d+\s*', '', adresse)  # Enlève les numéros au début
    
    # Normalisation des caractères Unicode
    adresse = unicodedata.normalize('NFKD', adresse)
    
    # Retourner l'adresse nettoyée et normalisée
    return adresse  # Enlever les espaces supplémentaires aux extrémités




# Créer une fonction pour générer la carte pour chaque trajet
def gen_carte_trajet(ligne,G,m,index_colonne_depart,index_colonne_arrive):
    origin = ox.geocode(f"{ligne[index_colonne_depart]}, Montpellier, France")  # Première colonne
    destination = ox.geocode(f"{ligne[index_colonne_arrive]}, Montpellier, France")  # Deuxième colonne

    # Trouver les nœuds les plus proches de l'origine et de la destination
    origin_node = ox.nearest_nodes(G, origin[1], origin[0])
    destination_node = ox.nearest_nodes(G, destination[1], destination[0])

    # Calculer l'itinéraire aller et retour
    route = ox.shortest_path(G, origin_node, destination_node)
    route_back = ox.shortest_path(G, destination_node, origin_node)

    # Fonction pour convertir un itinéraire (liste de nœuds) en liste de coordonnées géographiques
    def route_to_coords(G, route):
        route_coords = []
        for node in route:
            point = (G.nodes[node]['y'], G.nodes[node]['x'])  # latitude, longitude
            route_coords.append(point)
        return route_coords

    # Obtenir les coordonnées pour l'itinéraire
    route_coords = route_to_coords(G, route)

    # Ajouter l'itinéraire aller (en rouge) à la carte
    folium.PolyLine(locations=route_coords, color='red', weight=5, opacity=0.75).add_to(m)

    # Ajouter des marqueurs pour l'origine et la destination
    départ1,départ2 = route_coords[0]
    arr1,arr2 = route_coords[0]
    folium.Marker(location=[départ1, départ2], popup="Départ").add_to(m)
    folium.Marker(location=[arr1, arr2], popup="Arrivée").add_to(m)
    return m


def json_process(url: str, target_path: str) -> pd.DataFrame:
    """
    Télécharge un fichier JSON depuis une URL, le nettoie et le transforme en un DataFrame.
    
    Parameters:
    - url (str): L'URL du fichier JSON à télécharger.
    - target_path (str): Le chemin où le fichier JSON sera sauvegardé.
    
    Returns:
    - pd.DataFrame: Un DataFrame contenant les données JSON nettoyées.
    """
    # Télécharger le fichier JSON
    path, fname = os.path.split(target_path)
    pooch.retrieve(url, path=path, fname=fname, known_hash=None)

    # Lire le fichier JSON depuis le chemin local
    with open(target_path, 'r', encoding='utf-8') as file:
        raw_text = file.read()

    # Utiliser une expression régulière pour trouver chaque objet JSON (entre accolades)
    json_objects = re.findall(r'\{.*?\}', raw_text)

    # Initialiser une liste pour stocker les objets JSON valides
    data = []

    # Fonction pour tenter de réparer les JSON mal formés
    def clean_json(obj_str):
        # Tentative de fermeture des objets JSON en ajoutant une accolade fermante si nécessaire
        if obj_str.count('{') != obj_str.count('}'):
            obj_str += '}'  # Ajouter une accolade fermante si nécessaire
        return obj_str

    # Charger chaque objet JSON séparément
    for obj in json_objects:
        try:
            clean_obj = clean_json(obj)  # Réparer les JSON mal formés
            data.append(json.loads(clean_obj))
        except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON sur l'objet : {obj}")
            print(e)

    # Convertir la liste d'objets JSON en DataFrame
    df = pd.DataFrame(data)
    
    return df
