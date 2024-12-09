# -*- coding: utf-8 -*-

#%%
import json 
import csv 
import os 
from datetime import datetime 
import folium
from folium import PolyLine
import matplotlib.pyplot as plt
from folium.plugins import HeatMap 
import osmnx as ox
from collections import defaultdict 
import networkx as nx
import pandas as pd
import numpy as np

#%% tous les fichiers.json

fichiers=['./data/json/MMM_EcoCompt_ED223110495.json','./data/json/MMM_EcoCompt_ED223110496.json',
          './data/json/MMM_EcoCompt_ED223110497.json','./data/json/MMM_EcoCompt_ED223110500.json',
          './data/json/MMM_EcoCompt_ED223110501.json','./data/json/MMM_EcoCompt_X2H19070220.json',
          './data/json/MMM_EcoCompt_X2H20042632.json','./data/json/MMM_EcoCompt_X2H20042633.json',
          './data/json/MMM_EcoCompt_X2H20042634.json','./data/json/MMM_EcoCompt_X2H20042635.json',
          './data/json/MMM_EcoCompt_X2H20063161.json','./data/json/MMM_EcoCompt_X2H20063162.json',
          './data/json/MMM_EcoCompt_X2H20063163.json','./data/json/MMM_EcoCompt_X2H20063164.json',
          './data/json/MMM_EcoCompt_X2H20104132.json','./data/json/MMM_EcoCompt_X2H21070341.json',
          './data/json/MMM_EcoCompt_X2H21070342.json','./data/json/MMM_EcoCompt_X2H21070343.json',
          './data/json/MMM_EcoCompt_X2H21070344.json','./data/json/MMM_EcoCompt_X2H21070345.json',
          './data/json/MMM_EcoCompt_X2H21070346.json','./data/json/MMM_EcoCompt_X2H21070347.json',
          './data/json/MMM_EcoCompt_X2H21070348.json','./data/json/MMM_EcoCompt_X2H21070349.json',
          './data/json/MMM_EcoCompt_X2H21070350.json','./data/json/MMM_EcoCompt_X2H21070351.json',
          './data/json/MMM_EcoCompt_X2H21111120.json','./data/json/MMM_EcoCompt_X2H21111121.json',
          './data/json/MMM_EcoCompt_X2H22043029.json','./data/json/MMM_EcoCompt_X2H22043030.json',
          './data/json/MMM_EcoCompt_X2H22043031.json','./data/json/MMM_EcoCompt_X2H22043032.json',
          './data/json/MMM_EcoCompt_X2H22043033.json','./data/json/MMM_EcoCompt_X2H22043034.json',
          './data/json/MMM_EcoCompt_X2H22043035.json','./data/json/MMM_EcoCompt_X2H22104765.json',
          './data/json/MMM_EcoCompt_X2H22104766.json','./data/json/MMM_EcoCompt_X2H22104767.json',
          './data/json/MMM_EcoCompt_X2H22104768.json','./data/json/MMM_EcoCompt_X2H22104769.json',
          './data/json/MMM_EcoCompt_X2H22104770.json','./data/json/MMM_EcoCompt_X2H22104771.json',
          './data/json/MMM_EcoCompt_X2H22104772.json','./data/json/MMM_EcoCompt_X2H22104773.json',
          './data/json/MMM_EcoCompt_X2H22104774.json','./data/json/MMM_EcoCompt_X2H22104775.json',
          './data/json/MMM_EcoCompt_X2H22104776.json','./data/json/MMM_EcoCompt_X2H22104777.json',
          './data/json/MMM_EcoCompt_XTH19101158.json','./data/json/MMM_EcoCompt_XTH21015106.json',
          './data/json/MMM_EcoCompt_XTH24072390.json','./data/json/MMM_EcoCompt_XAH23111501.json',
          './data/json/MMM_EcoCompt_XTH19101158_2020.json', './data/json/MMM_EcoCompt_X2H20063164_2020.json', 
          './data/json/MMM_EcoCompt_X2H20063163_2020.json', './data/json/MMM_EcoCompt_X2H20063162_2020.json', 
          './data/json/MMM_EcoCompt_X2H20063161_2020.json', './data/json/MMM_EcoCompt_X2H20042635_2020.json', 
          './data/json/MMM_EcoCompt_X2H20042634_2020.json', './data/json/MMM_EcoCompt_X2H20042633_2020.json', 
          './data/json/MMM_EcoCompt_X2H20042632_2020.json', './data/json/MMM_EcoCompt_X2H19070220_2020.json']

#%% tous les fichiers .csv

# Charger le fichier CSV
donnee2024 = pd.read_csv("./data/CoursesVelomagg.csv")
donnee2023= pd.read_csv("./data/extracted/TAM_MMM_CoursesVelomagg_2023.csv")
donnee2022= pd.read_csv("./data/extracted/TAM_MMM_CoursesVelomagg_2022.csv")
donnee2021= pd.read_csv("./data/extracted/TAM_MMM_CoursesVelomagg_2021.csv", delimiter=';')


# Sélectionner les colonnes 2, 5, et 6 (en indexation zéro, cela correspond aux indices 1, 4, et 5)
donnee_utile_2024 = donnee2024.iloc[:, [2, 5, 6]]
donnee_utile_2023 = donnee2023.iloc[:, [2, 5, 6]]
donnee_utile_2022 = donnee2022.iloc[:, [2, 5, 6]]
donnee_utile_2021 = donnee2021.iloc[:, [1, 4, 5]]

# Sauvegarder dans un nouveau fichier CSV

donnee_formate_2024= donnee_utile_2024.to_csv("./data/prediction/2024.csv",sep=",", header= False, index=False)
donnee_formate_2023= donnee_utile_2023.to_csv("./data/prediction/2023.csv",sep=",", header= False, index=False)
donnee_formate_2022= donnee_utile_2022.to_csv("./data/prediction/2022.csv",sep=",", header= False, index=False)
donnee_formate_2021= donnee_utile_2021.to_csv("./data/prediction/2021.csv",sep=",", header= False, index=False)

# Afficher un aperçu pour vérifier




files=["./data/prediction/2021.csv","./data/prediction/2022.csv", "./data/prediction/2023.csv","./data/prediction/2024.csv"]








#%% récupération uniquement des données voulues 
donnee=[]
for filename in fichiers:
    if os.path.exists(filename):  # Vérifie si le fichier existe
        with open(filename, 'r') as f:
            json_data = f.read()
            data = json.loads(json_data)
            for item in data:
                loc = item.get("location")
                date = item.get("dateObserved")
                intensity = item.get("intensity")
                if date != 'Null/Null' and intensity != 'Null':
                    donnee.append([intensity, date, loc])
    else:
        print(f"Le fichier {filename} n'existe pas.")


donnees_utiles = []

for ligne in donnee:
    if ligne[0]!=None:
        if ligne[1].split('/')!=None:
            if ligne[2]['coordinates']!=[None, None]:
                intensite = ligne[0]  # Récupération de l'intensité 
    
    # Extraction de la date, en prenant la première partie avant le 'T'
                date = ligne[1].split('T')[0]
    
    # Extraction des coordonnées sous la bonne forme 

                coordinates = ligne[2]['coordinates']
    
    # Ajout de la ligne de données utiles 
                donnees_utiles.append([intensite, date, coordinates])

# Affichage du résultat




#%%récupération et gestion des stations, de leurs noms et de leurs coordonnées 
stations = [['054' ,[ 3.853317342, 43.5882630621 ]],
    ['055', [ 3.9640091778, 43.5578827375 ]],
    ['058', [ 3.9640091778, 43.5578827375 ]],
    ['041', [ 3.8280306309, 43.6391121171 ]],
    ['035', [ 3.8328917424, 43.6336865747 ]],
    ['048', [ 3.8347266149, 43.6214732421 ]],
    ['044', [ 3.8326421559, 43.6146896895 ]],
    ['049', [ 3.8394718931, 43.6151942523 ]],
    ['036', [ 3.849034904, 43.634312448 ]],
	['037', [ 3.8610694685, 43.6314441319 ]],
	['012', [ 3.8683479381, 43.6226843462 ]],
	['030', [ 3.8658015824, 43.6190001238 ]],
	['047', [ 3.8550871216, 43.6167993822 ]],
	['046', [ 3.8557044551, 43.6219370547 ]],
    ['039', [ 3.882495466, 43.6262678104 ]],
    ['042', [ 3.8738416122, 43.619840485 ]],
    ['040', [ 3.8838703934, 43.6198879537 ]],
	['015', [ 3.8939508257, 43.6187055731 ]], 
    ['019', [ 3.8776877223, 43.6145755318 ]],
    ['013', [ 3.8799808871, 43.6166711412 ]],
    ['005', [ 3.8818275629, 43.6140134811 ]], 
    ['014', [ 3.8849352522, 43.6166451977 ]], 
    ['023', [ 3.8671520365, 43.6120174261 ]],
    ['007', [ 3.8732996639, 43.6109777873 ]],
    ['011', [ 3.8684137971, 43.6085694888 ]], 
    ['020', [ 3.8706517253, 43.6070635891 ]], 
    ['026', [ 3.8679398754, 43.603556964 ]], 
    ['022', [ 3.8722140804, 43.603475123 ]], 
    ['008', [ 3.8772369657, 43.6099342368 ]],
	['003', [ 3.8812760844, 43.6094492048 ]],
    ['002', [ 3.8788315031, 43.6081476627 ]],
    ['009', [ 3.8769170201, 43.6061513637 ]],
    ['001', [ 3.881370075, 43.6053296752 ]],
    ['028', [ 3.8749744308, 43.6048813993 ]], 
    ['050', [ 3.879962846, 43.6043649583 ]], 
    ['025', [ 3.8758151178, 43.5998583226 ]],
    ['024', [ 3.884336371, 43.6011582475 ]],
    ['031', [ 3.8886145464, 43.6037779173 ]], 
    ['018',  [ 3.8867372303, 43.6078882126 ]], 
	['016', [ 3.8907214944, 43.6078937189 ]], 
    ['017', [ 3.8931771644, 43.608206873 ]], 
    ['004', [ 3.894825744, 43.5989539459 ]], 
    ['021', [ 3.8984419614, 43.6003487634 ]], 
    ['029', [ 3.8993434656, 43.6035220367 ]],
    ['045', [ 3.911515161, 43.6058242619 ]], 
    ['027', [ 3.9190935216, 43.6036653221 ]],
    ['033', [ 3.8906896787, 43.590760933 ]], 
    ['032', [ 3.8845068873, 43.5905067128 ]], 
    ['043', [ 3.8601483089, 43.5842380999 ]], 
    ['010', [ 3.8760262589, 43.6029235392 ]], 
    ['006', [ 3.8742329612, 43.6162318463 ]], 
    ['059', [ 3.9234612134, 43.5956676216 ]], 
    ['053', [ 3.8810044754, 43.6043436367 ]], 
    ['056', [ 3.8731804651, 43.6139404657 ]], 
    ['051', [ 3.8824143622, 43.6059890847 ]], 
	['057', [ 3.8728748163, 43.6087803873 ]]]

name_sta=[['054', 'Providence-Ovalie'], 
['055', 'Pérols'],
['058', 'Pérols'], 
['041', 'Euromédecine'], 
['035', 'Malbosc'],
['048', 'Hôtel du Département'], 
['044', 'Celleneuve'], 
['049', 'Tonnelles'], 
['036', 'Occitanie'], 
['037', 'Fac des Sciences'], 
['012', 'Boutonnet'], 
['030', 'Charles Flahault'], 
['047', 'Place Viala'], 
['046', 'Père Soulas'],
['039', 'Aiguelongue'], 
['042', 'Marie Caizergues'],  
['040', 'Jeu de Mail des Abbés'],
['015', 'Les Aubes'], 
['019', 'Louis Blanc'], 
['013', 'Emile Combes'],  
['005', 'Corum'], 
['014', 'Beaux-Arts'],
['023', 'Les Arceaux'], 
['007', 'Foch'], 
['011', 'Plan Cabanes'],  
['020', 'Gambetta'], 
['026', 'Renouvier'], 
['022', 'Clémenceau'], 
['008', 'Halles Castellane'], 
['003', 'Esplanade'], 
['002', 'Comédie'],
['009', 'Observatoire'], 
['001', 'Rue Jules Ferry'], 
['028', 'Saint-Denis'],
['050', 'Parvis Jules Ferry'],  
['025', 'Nouveau Saint-Roch'],
['024', 'Cité Mion'], 
['031', 'Voltaire'], 
['018', 'Nombre d Or'],
['016', 'Antigone Centre'],
['017', 'Médiathèque Emile Zola'],
['004', 'Hôtel de Ville'], 
['021', 'Port Marianne'], 
['029', 'Richter'], 
['045', 'Jardin de la Lironde'],
['027', 'Odysseum'], 
['033', 'Garcia Lorca'], 
['032', 'Près d Arènes'],
['043', 'Sabines'],
['010', 'Rondelet'],
['006', 'Place Albert 1er - St-Charles'],  
['059', 'Montpellier Sud de France'], 
['053', 'Deux Ponts - Gare Saint-Roch'],
['056', 'Albert 1er - Cathedrale'],
['051', 'Pont de Lattes - Gare St-Roch'], 
['057', 'Saint-Guilhem - Courreau']]



# récupération des numéros des stations uniquement 
Sta=[]
for i in stations:
    Sta.append(i[0])
    


#%% jour_semaine(j)
#jour_semaine prend en entrée un chiffre entre 0 et 6 0 pour lundi et 6 pour dimanche et retourne la liste de toutes les coordonnées et des intensités calculées dans tous les jours des archives correspondant à ce jour de la semaine 
def jour_semaine(j):
    """
    Description: 
    La fonction 'jour_semaine' renvoie une liste des intensités et leurs coordonnées qui ont été mesurées à une date correspondant au jour de la semaine j. 
    
    Args: 
    - j : int
        Le numéro du jour de la semaine (entre 0 et 6) voulu. 
        
    Returns:
    - list 
        Une liste contenant toutes les données étant rattachées à une date correspondant au jour de la semaine voulu. Les données sont l'intensité et les coordonnées auxquelles elle est liée. 
    """
    
    Lundi=[]
    Mardi=[]
    Mercredi=[]
    Jeudi=[]
    Vendredi=[]
    Samedi=[]
    Dimanche=[]
    for i in range (len(donnees_utiles)): 
        date=datetime.strptime(donnees_utiles[i][1], '%Y-%m-%d')
        jour=date.weekday()
        if jour==0:
            Lundi.append([donnees_utiles[i][0], donnees_utiles[i][2]])
        elif jour==1:
            Mardi.append([donnees_utiles[i][0], donnees_utiles[i][2]])
        elif jour==2:
            Mercredi.append([donnees_utiles[i][0], donnees_utiles[i][2]])
        elif jour==3:
            Jeudi.append([donnees_utiles[i][0], donnees_utiles[i][2]])
        elif jour==4:
            Vendredi.append([donnees_utiles[i][0], donnees_utiles[i][2]])
        elif jour==5:
            Samedi.append([donnees_utiles[i][0], donnees_utiles[i][2]])
        else:
            Dimanche.append([donnees_utiles[i][0], donnees_utiles[i][2]])
    if j==0:
        return Lundi
    elif j==1:
        return Mardi 
    elif j==2:
        return Mercredi 
    elif j==3:
        return Jeudi
    elif j==4:
        return Vendredi 
    elif j==5:
        return Samedi 
    else:
        return Dimanche 
    
#%% coor_unique(j)
def coor_unique(j):
    """
    Description: 
    La fonction 'coor_unique' extrait toutes les coordonnées prises sur un jour j de façon unique 
    
    Args: 
    - j : int
        Le numéro du jour de la semaine (entre 0 et 6) voulu. 
        
    Returns: 
    - list 
        Une liste contenant toutes les coordonnées apparaissant dans les données prises un jour de la semaine j de façon unique. 
    """
    L=jour_semaine(j)
    co=[]
    for i in L:
        if i[1] not in co:
            co.append(i[1])
    return co

#%% mean_intens(j)
def mean_intens(j):
    """
    Description: 
    La fonction 'mean_intens' renvoie une liste des moyennes des intensités par coordonnées mesurées à une date correspondant au jour de la semaine j. 
    
    Args: 
    - j : int
        Le numéro du jour de la semaine (entre 0 et 6) voulu. 
        
    Returns: 
    - list 
        Une liste contenant toutes les moyennes d'intensité et les coordonnées auxquelles elle sont liées. 
    """
    N=0 
    L=jour_semaine(j)
    M=[]
    for i in L: 
        N=0 
        sum=i[0]
        n=0 
        k=0 
        for h in L:
            if h[1]==i[1]:
                sum+=h[0]
                N+=1 
        if len(M)>0:
            while n==0 and k<len(M):
                if i[1]==M[k][1]:
                    n=1
                k+=1
        if n==0:
            i[0]=sum/N
            M.append(i)
    return M 

#%% Carte avec chaleur ou non  intensity_to_color et map_jour
def intensity_to_color(intens, min_in, max_in): 
    """
    Description: 
    La fonction 'intensity_to_color' renvoie un code couleur pour une intensité donnée.  
    
    Args: 
    - intens : int
        L'intensité qu'on cherche à représenter. 
    - min_in : int
        L'intensité minimale à représenter. Elle correspond au minimum de l'échelle de couleur. 
    - max_in : int
        L'intensité maximale à représenter. Elle correspond au maximum de l'échelle de couleur. 
        
    Returns: 
    - 'rgba({}, {}, {}, {})' : str
        Le code couleur RGB associé à l'intensité à représenter. 
    """
    norm_in = (intens - min_in) / (max_in - min_in)
    color = plt.cm.RdYlGn_r(norm_in)  # Colormap GnYlRd(vert à rouge)
    return 'rgba({}, {}, {}, {})'.format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), 1)

#%%
def map_jour(j, style,jour):#entrée 0-6 pour les jours de la semaine, 0-1 sans-avec chaleur
    """
    Description: 
    La fonction 'map_jour' génère une carte des intensités moyennes observées un jour de la semaine j. 
    
    Args: 
    - j : int
        Le numéro du jour de la semaine (entre 0 et 6) voulu. 
    - style : int
        Le numéro (0 ou 1) correspondant au style voulu. 0 donnera une carte avec uniquement des points de différentes couleur et 1 donnera une carte avec ces points mais également la carte de chaleur (Heatmap) associée. 
    - jour : str
        Le nom du jour correspondant (par exemple, "Lundi", "Mardi", etc.), utilisé pour nommer les fichiers générés.
        
    Returns: 
    - 'La carte a été générée et sauvegardée sous le nom', nom : str, str 
        Un message de validation de création de la carte et le nom sous lequel elle a été enregistrée. 
    """
    data = mean_intens(j)
    intensities = [d[0] for d in data]
    min_in = min(intensities)
    max_in = max(intensities)

    # centrer 
    ville = "Montpellier, France"
    location = ox.geocode(ville)
    m = folium.Map(location=location, zoom_start=12)


    # Ajouter les points sur la carte
    for intensity, coord in data:
        lon, lat = coord[1], coord[0]# Inversion des valeurs
        if abs(lon-location[0])<1 and abs(lat-location[1])<1:
            color = intensity_to_color(intensity, min_in, max_in)
            folium.CircleMarker(
                location=[lon, lat],
                radius=8,
                popup=f"{intensity}",
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6
                ).add_to(m)
            
    legend_html ="""
<div style="
            position: fixed;
            bottom: 50px;
            left: 50px;
            width: 220px;
            height: 120px;
            background-color: white;
            border: 2px solid grey;
            z-index: 9999;
            font-size: 14px;
            padding: 10px;
            ">
            <b>Nombre de passages:</b>
            <div style="
                height: 20px;
                background: linear-gradient(to right, #008000, #f1fd4d, #f20000);
                margin: 10px 0;
                ">
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Faible</span>
                <span>Élevé</span>
            </div>
        </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))
    #choix de chaleur ou non
    if style==0:
        nom=f'intensity_{j}.html'
        m.save(f'./Cycle3/visualisation/{jour}/intensité/{nom}')
        return "La carte a été générée et sauvegardée sous le nom", nom
    
    else:
        heat_data = [[coord[1], coord[0], intensity] for intensity, coord in data]
        HeatMap(heat_data).add_to(m)
        nom=f'intensity_{j}_heat.html'
        m.save(f'./Cycle3/visualisation/{jour}/intensité/{nom}')
        return"La carte a été générée et sauvegardée sous le nom", nom 
        
        
#%% tracer toutes les cartes avec intensité sur un jour avec ou sans chaleur 

reply = input("Voulez-vous tracer les 14 cartes intensité par jour (avec et sans chaleur) ? (oui/non) : ")
if reply.strip().lower() == "oui":
    map_jour(0,0,'Lundi')
    map_jour(0,1,'Lundi')
    print("Cartes pour lundi crées.")
    map_jour(1,0,'Mardi')
    map_jour(1,1,'Mardi')
    print("Cartes pour mardi crées.")
    map_jour(2,0,'Mercredi')
    map_jour(2,1,'Mercredi')
    print("Cartes pour mercredi crées.")
    map_jour(3,0,'Jeudi')
    map_jour(3,1,'Jeudi')
    print("Cartes pour jeudi crées. ")
    map_jour(4,0,'Vendredi')
    map_jour(4,1,'Vendredi')
    print("Cartes pour vendredi crées. ")
    map_jour(5,0,'Samedi')
    map_jour(5,1,'Samedi')
    print("Cartes pour samedi crées.")
    map_jour(6,0,'Dimanche')
    map_jour(6,1,'Dimanche')
    print("Cartes pour dimanche crées.")
else:
    print("Les cartes des intensités n'ont pas été générées.")
    
    
#%%nb_tot_jour(j)
def nb_tot_jour(j):
    """
    Description: 
    La fonction 'nb_tot_jour' renvoie le nombre de dates comptées dans les donnnées correspondants au jour de la semaine j. 
    
    Args: 
    - j : int
        Le numéro du jour de la semaine (entre 0 et 6) voulu. 
        
    Returns: 
    - int 
        Le nombre de jour j comptés dans les données.
    """
    
    D=[]
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            lecteur = csv.reader(f, delimiter=',')  # Définir le séparateur si nécessaire
            next(lecteur) #ignorer l'entête 
            for ligne in lecteur: 
                dat, heur = ligne[0].split(' ')
                date=datetime.strptime(dat, '%Y-%m-%d')
                jour=date.weekday()
                if jour==j:
                    dep=ligne[1].split(' ')[0]
                    arr=ligne[2].split(' ')[0]
                    if dep!='' and arr!='':
                        if dep in Sta and arr in Sta:
                            if dat not in D:
                                D.append(dat)
    return len(D)

#%%nb_tot_jour pour chaque jour
rep = input("Voulez-vous le nombre de jours pour chaque jour de la semaine? Attention, pour pouvoir compiler la suite du code et afficher les cartes dans la suite, il est nécessaire de répondre oui à chaque étape. (oui/non) : ")
if rep.strip().lower() == "oui":
    Nl=nb_tot_jour(0)
    Nma=nb_tot_jour(1)
    Nme=nb_tot_jour(2)
    Nj=nb_tot_jour(3)
    Nv=nb_tot_jour(4)
    Ns=nb_tot_jour(5)
    Nd=nb_tot_jour(6)
    print("Le nombre de dates pour chaque jour a été calculé et enregistré.")
else: 
    print("Le calcul n'a pas été effectué.")
    
#%%poids_par_h(j) 

def poids_par_h(j):
    """
    Description: 
    La fonction 'poids_par_h' compte la participation de chaque heure dans la journée. Elle donne la proportion de l'activité journalière calculée par heure pour le jour de la semaine j. 
    
    Args: 
    - j : int
        Le numéro du jour de la semaine (entre 0 et 6) voulu. 
        
    Returns: 
    - matrix 
        Une matrice avec pour colonne les heures et le pourcentage de l'activité journalière associée à chacune de ces heures. 
    """
    heures = {heure: 0 for heure in range(24)}
    D=[]
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            lecteur = csv.reader(f, delimiter=',')  
            next(lecteur) #ignorer l'entête 
            for ligne in lecteur: 
                dat = ligne[0].split(' ')[0]
                heur =ligne[0].split(' ')[1]
                date=datetime.strptime(dat, '%Y-%m-%d')
                jour=date.weekday()
                if jour==j:
                    dep=ligne[1].split(' ')[0]
                    arr=ligne[2].split(' ')[0]
                    if dep!='' and arr!='':
                        if dep in Sta and arr in Sta:
                            if dat not in D:
                                D.append(dat)
                            heure = int(heur.split(':')[0])  # Extraire l'heure
                            heures[heure] += 1 # Incrémenter le compteur pour cette heure
    N=len(D)
    H=[heures[h]/N for h in heures]
    t=sum(H[h] for h in heures)
    return  [[h, H[h]*100/t] for h in heures]

#%% poids_par_h pour chaque jour. 
reponse = input("Voulez-vous le poids des heures pour chaque jour de la semaine? Attention, pour pouvoir compiler la suite du code et afficher les cartes dans la suite, il est nécessaire de répondre oui à chaque étape. (oui/non) : ")
if reponse.strip().lower() == "oui":
    pLu=poids_par_h(0)
    pMa=poids_par_h(1)
    pMe=poids_par_h(2)   
    pJe=poids_par_h(3)
    pVe=poids_par_h(4)
    pSa=poids_par_h(5)
    pDi=poids_par_h(6)
    print("Le poids des heures de chaque jour a été calculé")
else:
    print("Le poids des heures n'a pas été calculé.")
    
#%%map_jour_h 
def map_jour_h(j, h,style,jour):#entrée 0-6 pour les jours de la semaine, 0-1 sans-avec chaleur
    """
    Description: 
    La fonction 'map_jour_h' génère une carte des intensités moyennes observées un jour de la semaine j à une heure h. 
    
    Args: 
    - j : int
        Le numéro du jour de la semaine (entre 0 et 6) voulu. 
    - h : int
        Le numéro de l'heure voulue (entre 0 et 23, 0 étant la plage horraire 00h00- 00h59). 
    - style : int
        Le numéro (0 ou 1) correspondant au style voulu. 0 donnera une carte avec uniquement des points de différentes couleur et 1 donnera une carte avec ces points mais également la carte de chaleur (Heatmap) associée. 
    - jour : str
        Le nom du jour correspondant (par exemple, "Lundi", "Mardi", etc.), utilisé pour nommer les fichiers générés.
        
    Returns: 
    - 'La carte a été générée et sauvegardée sous le nom', nom : str, str 
        Un message de validation de création de la carte et le nom sous lequel elle a été enregistrée. 
    """    
    data = mean_intens(j)
    p=poids_par_h(j)
    intensities = [d[0]*p[h][1]/100 for d in data]
    min_in = min(intensities)
    max_in = max(intensities)

    # centrer 
    ville = "Montpellier, France"
    location = ox.geocode(ville)
    m = folium.Map(location=location, zoom_start=12)


    # Ajouter les points sur la carte
    for intensity, coord in data:
        newint=intensity*p[h][1]/100
        lon, lat = coord[1], coord[0]# Inversion des valeurs
        if abs(lon-location[0])<1 and abs(lat-location[1])<1:
            color = intensity_to_color(newint, min_in, max_in)
            folium.CircleMarker(
                location=[lon, lat],
                radius=8,
                popup=f"{newint}",
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6
                ).add_to(m)
            
    # Générer la légende avec les couleurs correspondant aux min et max
    min_color = intensity_to_color(min_in, min_in, max_in)  # Couleur pour la valeur minimale
    max_color = intensity_to_color(max_in, min_in, max_in)  # Couleur pour la valeur maximale

    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 200px;
        height: 100px;
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
    ">
        <b>Nombre de passages:</b><br>
        <i style="background: {min_color}; width: 20px; height: 10px; display: inline-block;"></i> {round(min_in, 2)}<br>
        <i style="background: {max_color}; width: 20px; height: 10px; display: inline-block;"></i> {round(max_in, 2)}<br>
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))
    #choix de chaleur ou non
    if style==0:
        nom=f'intensity_{j}_{h}.html'
        m.save(f'./Cycle3/visualisation/{jour}/intensité/{nom}')
        return "La carte a été générée et sauvegardée sous le nom", nom
    
    else:
        heat_data = [[coord[1], coord[0], intensity] for intensity, coord in data]
        HeatMap(heat_data).add_to(m)
        nom=f'intensity_{j}_{h}_heat.html'
        m.save(f'./Cycle3/visualisation/{jour}/intensité/{nom}')
        return"La carte a été générée et sauvegardée sous le nom", nom 



#%% tracer toutes les cartes avec intensité sur un jour avec ou sans chaleur 

reply = input("Voulez-vous tracer les 168 cartes intensité par jour et par heure sans chaleur ? (oui/non) : (Cela n'influe pas la suite du code)")
L=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
if reply.strip().lower() == "oui":
    for i in range (0, 7):
        for j in range(0,24):
                map_jour_h(i, j, 0,L[i])
                print('map', i, j, 'générée')
else: 
    print("Les cartes n'ont pas été générées. ")



#%%trajets_parcourus_jour(j)
def trajets_parcourus_jour(j):
    """
    Description: 
    La fonction 'trajets_parcourus_jour' recense tous les trajets ayant eut lieu un jour j. 
    
    Args: 
    - j : int
        Le numéro du jour de la semaine (entre 0 et 6) voulu. 
     
    Returns: 
    - matrix
        Une matrice avec chaque ligne de la forme [heure de départ, station de départ, station d'arrivée]. 
    """
    D=[]
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            lecteur = csv.reader(f, delimiter=',')  # Définir le séparateur si nécessaire
            next(lecteur) #ignorer l'entête 
            for ligne in lecteur: 
                dat, heur = ligne[0].split(' ')
                dep=ligne[1].split(' ')[0]
                arr=ligne[2].split(' ')[0]
                date=datetime.strptime(dat, '%Y-%m-%d')
                jour=date.weekday()
                if jour==j:
                    if dep in Sta and arr in Sta:
                        if dep!=arr:
                            D.append([heur, dep, arr])
    return D 


#%% trajets_parcourus_jour pour chaque jour.
quest = input("Voulez-vous les trajets parcourus pour chaque jour de la semaine? Attention, pour pouvoir compiler la suite du code et afficher les cartes dans la suite, il est nécessaire de répondre oui à chaque étape. (oui/non) : ")
if quest.strip().lower() == "oui":
    Lu=trajets_parcourus_jour(0)
    Ma=trajets_parcourus_jour(1)
    Me=trajets_parcourus_jour(2)
    Je=trajets_parcourus_jour(3)
    Ve=trajets_parcourus_jour(4)
    Sa=trajets_parcourus_jour(5)
    Di=trajets_parcourus_jour(6)
    print("Les trajets ont été comptés pour chaque jour.")
else: 
    print("Les trajets n'ont pas été comptés.")

#%% trajets_parcourus(j,h)
def trajets_parcourus(j,h):
    """
    Description: 
    La fonction 'trajets_parcourus' recense les trajets ayant eu lieu un jour j à une heure h et leur occurence. 
    
    Args: 
    - j : int
        Le numéro du jour de la semaine (entre 0 et 6) voulu. 
    - h : int
        Le numéro (de 0 à 23) de l'heure voulue. 
        
    Returns: 
    - matrix 
        Une matrice avec chaque ligne de la forme [[station de départ, station d'arrivée], occurrence]
    """
    D=trajets_parcourus_jour(j)
    T=[]
    U=[]
    F=[]
    for j in D:
        H=int(j[0].split(':')[0])
        if H==h:
            T.append([j[1],j[2]])
    for I in T:
        if I not in U:
            U.append(I) 
    for s in U:
        c=0
        for t in T:
            if t==s:
                c+=1
        F.append([s,c])
    return F


#%%  

def TRAJETS(j, h):
    """
    Description: 
    La fonction 'TRAJETS' recense les trajets ayant eu lieu un jour j à une heure h. 
    
    Args: 
    - j : int
        Le numéro du jour de la semaine (entre 0 et 6) voulu. 
    - h : int
        Le numéro (de 0 à 23) de l'heure voulue. 
        
    Returns: 
    - matrix 
        Une matrice avec chaque ligne de la forme [station de départ, station d'arrivée]
    """
    T=[]
    J=[Lu, Ma, Me, Je, Ve, Sa, Di]
    L=J[j]
    for j in L: 
        H=int(j[0].split(':')[0])
        if H==h: 
            T.append([j[1], j[2]])
    return T 

#%%
A=np.zeros((7, 24), dtype=int)
question = input("Voulez-vous recenser les trajets parcourus pour chaque jour de la semaine à chaque heure? (oui/non) : ")
if question.strip().lower() == "oui":
    A = [[TRAJETS(i, k) for k in range(24)] for i in range(7)]
    print("Les trajets ont été recensées dans A")

else: 
    print("Les trajets n'ont pas été recensés. ")

#%%
def traj_mult(j, h):
    """
    Description: 
    La fonction 'trajets_mult' recense les trajets ayant eu lieu un jour j à une heure h et leur occurrence. 
        
    Args: 
        - j : int
            Le numéro du jour de la semaine (entre 0 et 6) voulu. 
        - h : int
            Le numéro (de 0 à 23) de l'heure voulue. 
    
    Returns: 
        - matrix 
        Une matrice avec chaque ligne de la forme [[station de départ, station d'arrivée], occurrence] uniquement si l'occurrence est supérieure à 8 ( 2 fois pas an).
    """
    T=TRAJETS(j, h)
    U=[]
    F=[]
    G=[]
    for I in T:
        if I not in U:
            U.append(I) 
    for s in U:
        c=0
        for t in T:
            if t==s:
                c+=1
        F.append([s,c])
    for i in F:
        if i[1]>=8: #min une fois par semestre 
            G.append(i)
    return G
    
#%%
All_t=np.zeros((7, 24), dtype=int)
question = input("Voulez-vous recenser les trajets parcourus pour chaque jour de la semaine à chaque heure et leurs occurrences, s'il y a eu plus de 8 occurences de ces trajets? Attention, pour pouvoir compiler la suite du code et afficher les cartes dans la suite, il est nécessaire de répondre oui à chaque étape. (oui/non) : ")
if question.strip().lower() == "oui":
    All_t = [[traj_mult(i, k) for k in range(24)] for i in range(7)]
    print("Les trajets et leurs occurrences ont été recensés dans All_t")

else: 
    print("Les trajets et leurs occurrences n'ont pas été recensés. ")
    
#%%
def map_trajets(j, h,jour):
    """
    Description: 
    La fonction 'map_trajets' génère une carte des trajets parcourus un jour de la semaine j et à une heure h, ainsi que la probabilité qu'il soit de nouveau parcouru (en tenant compte des archives). 
    
    Args: 
    - j : int
        Le numéro du jour de la semaine (entre 0 et 6) voulu. 
    - h : int
        Le numéro (0 ou 1) correspondant au style voulu. 0 donnera une carte avec uniquement des points de différentes couleur et 1 donnera une carte avec ces points mais également la carte de chaleur (Heatmap) associée. 
    - jour : str
        Le nom du jour correspondant (par exemple, "Lundi", "Mardi", etc.), utilisé pour nommer les fichiers générés.
        
    Returns: 
    - 'La carte a été générée et sauvegardée sous le nom', nom : str, str 
        Un message de validation de création de la carte et le nom sous lequel elle a été enregistrée. 
    """
    trajets=All_t[j][h]
    stations_dict = {station[0]: station[1] for station in stations}
    if j==0:
        N=Nl
    elif j==1:
        N=Nma
    elif j==2: 
        N=Nme
    elif j==3:
        N=Nj
    elif j==4:
        N=Nv
    elif j==5: 
        N=Ns
    else: 
        N=Nd
    
    
    ville = "Montpellier, France"
    location = ox.geocode(ville)
    graphe = ox.graph_from_point(location, dist=10000, network_type="all", simplify=True)
    carte = folium.Map(location=location, zoom_start=14)

    #nb passages 
    edges_passages = defaultdict(int)

    for trajet in trajets:
        start, end = trajet[0]
        intensity = min(trajet[1]/N, 1)
        if start in stations_dict and end in stations_dict:
            if start!=end:
                lon_start, lat_start = stations_dict[start]
                lon_end, lat_end = stations_dict[end]

                # Trouver les nœuds les plus proches dans le graphe
                start_node = ox.distance.nearest_nodes(graphe, lon_start, lat_start)
                end_node = ox.distance.nearest_nodes(graphe, lon_end, lat_end)
                # Calculer le chemin entre les deux nœuds
                path = nx.shortest_path(graphe, start_node, end_node, weight="length")

            # Ajouter chaque segment du chemin au compteur de passages
            for u, v in zip(path[:-1], path[1:]):
                edges_passages[(u, v)] += intensity
                edges_passages[(v, u)] += intensity  #on compte les passages dans les deux sens 

    #couleurs en fonction du nb de passages
    for (u, v), passage_count in edges_passages.items():
        # récup coordonnées des segments
        coords = [
            (graphe.nodes[u]['y'], graphe.nodes[u]['x']),
            (graphe.nodes[v]['y'], graphe.nodes[v]['x'])
        ]

        # Calcul de la couleur
        if passage_count < 0.05:
           color= "#0000ff" #bleu si faible
        elif passage_count < 0.15:
            color= "#008000" # vert 
        elif passage_count < 0.25:
            color="#ffff00" #jaune
        elif passage_count < 0.35: 
            color="#ff80000" #orange 
        elif passage_count < 1: 
            color="#ff0000" #rouge si fort 
        else:
            passage_count=1
            color="#000000"

        # Ajouter le segment
        folium.PolyLine(
            locations=coords,
            color=color,
            weight=4,
            opacity=0.8,
            tooltip=f"Pourcentage: {passage_count*100}"
        ).add_to(carte)

    # Ajout des stations comme marqueurs
    for station in stations:
        try:
            (lon, lat) = station[1]
            for k in name_sta: 
                if k[0]==station[0]: 
                    name= k[1]
            folium.Marker(
                location=(lat, lon),
                popup=f"{name}: {lon}, {lat}",
                icon=folium.Icon(color="gray")
            ).add_to(carte)
        except Exception as e:
            print(f"Erreur lors de l'ajout de la station {station}: {e}")

    # légende 
    legend_html = """
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 200px;
        height: 200px;
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
        ">
        <b>Pourcentage de chance que le trajet soit parcouru:</b><br>
        <i style="background: #0000ff; width: 20px; height: 10px; display: inline-block;"></i> Très faible (&lt;5%)<br>
        <i style="background: #008000; width: 20px; height: 10px; display: inline-block;"></i> Faible (5%-14%)<br>
        <i style="background: #ffff00; width: 20px; height: 10px; display: inline-block;"></i> Modéré (15%-24%)<br>
        <i style="background: #ff8000; width: 20px; height: 10px; display: inline-block;"></i> Fort (25%-34%)<br>
        <i style="background: #ff0000; width: 20px; height: 10px; display: inline-block;"></i> Très fort (&gt; 34%)<br>
        <i style="background: #000000; width: 20px; height: 10px; display: inline-block;"></i> Sûr (1)<br>
    </div>
    """
    carte.get_root().html.add_child(folium.Element(legend_html))

    # Save la carte
    nom = f"trajets_couleurs_cumulées_j{j}_h{h}.html"
    carte.save(f'./Cycle3/visualisation/{jour}/Trajetscouleurs/{nom}')
    return f"Carte enregistrée sous '{nom}'."

#%% 
ask = input("Voulez-vous tracer les 168 cartes correspondant aux trajets par jour et par heure ? (oui/non) Attention, cela peut prendre jusqu'à 6h: ")
if ask.strip().lower() == "oui":
    for i in range(0, 7):
        for j in range(0, 24):
            map_trajets(i, j,L[i])
            print('map', i, j, 'générée')
else: 
    print("Les cartes n'ont pas été générées.")
