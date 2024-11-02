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


#Fonction qui donne le colonne i du tableau voulu: 
def colonne(i, w_file):
    L=[]
    with open(w_file) as f:
        for line in f:
            x=line.split(",")
            L.append(x[i])
    return L         

#Fonction qui retourne toutes les valeurs dans la colonne j quand l'argument de la colonne i est k 
def arg(k,i,j, w_file):
    L=[]
    with open(w_file) as f:
        for line in f:
            x=line.split(",")
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
def gen_carte_trajet(ligne, G, m, index_colonne_départ, index_colonne_arrive):
    # Essayer de géocoder les stations de départ et d'arrivée
    try:
        origin = ox.geocode(f"{ligne[index_colonne_départ]}, Montpellier, France")  # Première colonne
        destination = ox.geocode(f"{ligne[index_colonne_arrive]}, Montpellier, France")  # Deuxième colonne
        
        # Vérifier si le géocodage a réussi
        if origin is None or destination is None:
            print(f"Erreur de géocodage pour les stations : {ligne[index_colonne_départ]} ou {ligne[index_colonne_arrive]}")
            return m
        
        # Trouver les nœuds les plus proches de l'origine et de la destination
        origin_node = ox.nearest_nodes(G, origin[1], origin[0])  # longitude, latitude
        destination_node = ox.nearest_nodes(G, destination[1], destination[0])  # longitude, latitude

        # Calculer l'itinéraire aller et retour
        route = ox.shortest_path(G, origin_node, destination_node)

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
        départ_lat, départ_lon = route_coords[0]
        arr_lat, arr_lon = route_coords[-1]  # Utiliser le dernier point pour l'arrivée
        folium.Marker(location=[départ_lat, départ_lon], popup=f"{ligne[index_colonne_départ]},Départ").add_to(m)
        folium.Marker(location=[arr_lat, arr_lon], popup=f"{ligne[index_colonne_arrive]},arrivé").add_to(m)

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    
    return m


def coordonne(station):
    try:
        # Recherche de l'emplacement en utilisant osmnx
        location = ox.geocode(f"{station}, Montpellier, France")
        return location[0], location[1]
    except Exception as e:
        print(f"Erreur pour la station {station}: {e}")
        return None, None
