# Map lié à la base de donnée.

import osmnx as ox
import folium
import networkx as nx
import pandas as pd
from src.fonctions_basedonnees import*

coordonne.cache_clear()

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
liste_des_trajet_DBF['Departure station'] = liste_des_trajet_DBF['Departure station'].replace("Rue Jules Ferry - Gare Saint-Roch", "Gare Saint-Roch")
liste_des_trajet_DBF['Return station'] = liste_des_trajet_DBF['Return station'].replace("Rue Jules Ferry - Gare Saint-Roch", "Gare Saint-Roch")




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

data = trajets_du_jour[['Departure', 'Departure station', 'Return station', 'Covered distance (m)', 'Duration (sec.)']]
data.to_csv('./data/video.csv', index=False)
