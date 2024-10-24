import csv 
import matplotlib.pyplot as plt 
import numpy as np 

import os
import pooch
import pandas as pd
import json
import re


#importer les données 
filename1= 'MMM_MMM_GeolocCompteurs.csv'
filename2='TAM_MMM_CoursesVelomagg.csv'

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
