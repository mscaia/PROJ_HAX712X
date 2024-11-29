# -*- coding: utf-8 -*-

#%%
# dans la console: !pip install folium; !pip install osmnx
import json 
import csv 
import os 
from datetime import datetime 
import folium
from folium import PolyLine #a rajouter dans 6.1
import matplotlib.pyplot as plt
from folium.plugins import HeatMap #a rajouter dans 6.1
import osmnx as ox
from collections import defaultdict #a rajouter dans 6.1
import networkx as nx
import pandas as pd


#%%
fichiers = [
    './data/json/MMM_EcoCompt_ED223110495.json', './data/json/MMM_EcoCompt_ED223110496.json',
    './data/json/MMM_EcoCompt_ED223110497.json', './data/json/MMM_EcoCompt_ED223110500.json',
    './data/json/MMM_EcoCompt_ED223110501.json', './data/json/MMM_EcoCompt_X2H19070220.json',
    './data/json/MMM_EcoCompt_X2H20042632.json', './data/json/MMM_EcoCompt_X2H20042633.json',
    './data/json/MMM_EcoCompt_X2H20042634.json', './data/json/MMM_EcoCompt_X2H20042635.json',
    './data/json/MMM_EcoCompt_X2H20063161.json', './data/json/MMM_EcoCompt_X2H20063162.json',
    './data/json/MMM_EcoCompt_X2H20063163.json', './data/json/MMM_EcoCompt_X2H20063164.json',
    './data/json/MMM_EcoCompt_X2H20104132.json', './data/json/MMM_EcoCompt_X2H21070341.json',
    './data/json/MMM_EcoCompt_X2H21070342.json', './data/json/MMM_EcoCompt_X2H21070343.json',
    './data/json/MMM_EcoCompt_X2H21070344.json', './data/json/MMM_EcoCompt_X2H21070345.json',
    './data/json/MMM_EcoCompt_X2H21070346.json', './data/json/MMM_EcoCompt_X2H21070347.json',
    './data/json/MMM_EcoCompt_X2H21070348.json', './data/json/MMM_EcoCompt_X2H21070349.json',
    './data/json/MMM_EcoCompt_X2H21070350.json', './data/json/MMM_EcoCompt_X2H21070351.json',
    './data/json/MMM_EcoCompt_X2H21111120.json', './data/json/MMM_EcoCompt_X2H21111121.json',
    './data/json/MMM_EcoCompt_X2H22043029.json', './data/json/MMM_EcoCompt_X2H22043030.json',
    './data/json/MMM_EcoCompt_X2H22043031.json', './data/json/MMM_EcoCompt_X2H22043032.json',
    './data/json/MMM_EcoCompt_X2H22043033.json', './data/json/MMM_EcoCompt_X2H22043034.json',
    './data/json/MMM_EcoCompt_X2H22043035.json', './data/json/MMM_EcoCompt_X2H22104765.json',
    './data/json/MMM_EcoCompt_X2H22104766.json', './data/json/MMM_EcoCompt_X2H22104767.json',
    './data/json/MMM_EcoCompt_X2H22104768.json', './data/json/MMM_EcoCompt_X2H22104769.json',
    './data/json/MMM_EcoCompt_X2H22104770.json', './data/json/MMM_EcoCompt_X2H22104771.json',
    './data/json/MMM_EcoCompt_X2H22104772.json', './data/json/MMM_EcoCompt_X2H22104773.json',
    './data/json/MMM_EcoCompt_X2H22104774.json', './data/json/MMM_EcoCompt_X2H22104775.json',
    './data/json/MMM_EcoCompt_X2H22104776.json', './data/json/MMM_EcoCompt_X2H22104777.json',
    './data/json/MMM_EcoCompt_XTH19101158.json', './data/json/MMM_EcoCompt_XTH21015106.json',
    './data/json/MMM_EcoCompt_XTH24072390.json', './data/json/MMM_EcoCompt_XAH23111501.json',
    './data/json/MMM_EcoCompt_XTH19101158_2020.json', './data/json/MMM_EcoCompt_X2H20063164_2020.json',
    './data/json/MMM_EcoCompt_X2H20063163_2020.json', './data/json/MMM_EcoCompt_X2H20063162_2020.json',
    './data/json/MMM_EcoCompt_X2H20063161_2020.json', './data/json/MMM_EcoCompt_X2H20042635_2020.json',
    './data/json/MMM_EcoCompt_X2H20042634_2020.json', './data/json/MMM_EcoCompt_X2H20042633_2020.json',
    './data/json/MMM_EcoCompt_X2H20042632_2020.json', './data/json/MMM_EcoCompt_X2H19070220_2020.json'
]



files=['./data/extracted/TAM_MMM_CoursesVelomagg_2023.csv','./data/CoursesVelomagg.csv', 
            './data/extracted/TAM_MMM_CoursesVelomagg_2021.csv', './data/extracted/TAM_MMM_CoursesVelomagg_2022.csv']

print(files)
#a changer par rapport au github  
#%%
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
print(donnee)

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
print(donnees_utiles)

#%%
#jour_semaine prend en entrée un chiffre entre 0 et 6 0 pour lundi et 6 pour dimanche et retourne la liste de toutes les coordonnées et des intensités calculées dans tous les jours des archives correspondant à ce jour de la semaine 
def jour_semaine(j):
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

#%%
def coor_unique(j):
    L=jour_semaine(j)
    co=[]
    for i in L:
        if i[1] not in co:
            co.append(i[1])
    return co
    

#%%


def mean_intens(j):
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

#%% Carte avec chaleur ou non 
def intensity_to_color(intens, min_in, max_in): #code couleur pour les intensités 
    norm_in = (intens - min_in) / (max_in - min_in)
    color = plt.cm.RdYlGn_r(norm_in)  # Colormap GnYlRd(vert à rouge)
    return 'rgba({}, {}, {}, {})'.format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255), 1)

def map_jour(j, style):#entrée 0-6 pour les jours de la semaine, 0-1 sans-avec chaleur
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
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6
                ).add_to(m)
        
    #choix de chaleur ou non
    if style==0:
        nom=f'intensity_{j}.html'
        m.save(nom)
        return "La carte a été générée et sauvegardée sous le nom", nom
    
    else:
        heat_data = [[coord[1], coord[0], intensity] for intensity, coord in data]
        HeatMap(heat_data).add_to(m)
        nom=f'intensity_{j}_heat.html'
        m.save(nom)
        return"La carte a été générée et sauvegardée sous le nom", nom 


#%% maps pour lundi 
map_jour(0,0)
map_jour(0,1)
#%% maps pour mardi 
map_jour(1,0)
map_jour(1,1)

#%% maps pour mercredi 
map_jour(2,0)
map_jour(2,1)

#%% maps pour jeudi 
map_jour(3,0)
map_jour(3,1)

#%% maps pour vendredi 
map_jour(4,0)
map_jour(4,1)

#%% maps pour samedi 
map_jour(5,0)
map_jour(5,1)

#%% maps pour dimanche 
map_jour(6,0)
map_jour(6,1)

#problème avec la donnée de chaleur hors de montpellier 

#%% liste des stations et coordonnées géo 
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



#%% récupération des numéros des stations uniquement 
Sta=[]
for i in stations:
    Sta.append(i[0])
    
print (Sta)

#%% nombre de jour j

def nb_tot_jour(j):
    D=[]
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            lecteur = csv.reader(f, delimiter=';')  # Définir le séparateur si nécessaire
            next(lecteur) #ignorer l'entête 
            for ligne in lecteur: 
                dat, heur = ligne[2].split(' ')
                date=datetime.strptime(dat, '%Y-%m-%d')
                jour=date.weekday()
                if jour==j:
                    dep=ligne[5].split(' ')[0]
                    arr=ligne[6].split(' ')[0]
                    if dep!='' and arr!='':
                        if dep in Sta and arr in Sta:
                            if dat not in D:
                                D.append(dat)
    return len(D)


#%%

def poids_par_h(j):
    heures = {heure: 0 for heure in range(24)}
    D=[]
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            lecteur = csv.reader(f, delimiter=';')  
            next(lecteur) #ignorer l'entête 
            for ligne in lecteur: 
                dat, heur = ligne[2].split(' ')
                date=datetime.strptime(dat, '%Y-%m-%d')
                jour=date.weekday()
                if jour==j:
                    dep=ligne[5].split(' ')[0]
                    arr=ligne[6].split(' ')[0]
                    if dep!='' and arr!='':
                        if dep in Sta and arr in Sta:
                            if dat not in D:
                                D.append(dat)
                            heure = int(heur.split(':')[0])  # Extraire l'heure
                            heures[heure] += 1 # Incrémenter le compteur pour cette heure
    N=len(D)
    H=[heures[h]/N for h in heures]
    t=sum(H[h] for h in heures)
    return 'pourcentage de trajets par heure', [[h, H[h]*100/t] for h in heures]
#dans le return f'nombre total de trajets sur le jour {j}={t}', 'pourcentage de trajets par heure', [[h, H[h]*100/t] for h in heures], 'nombre de trajets par heure:', [[h, H[h]] for h in heures]

#%% nb et proportions de trajets par heure le lundi 
poids_par_h(0)

#%% nb et proportions de trajets par heure le mardi 
poids_par_h(1)

#%% nb et proportions de trajets par heure le mercredi 
poids_par_h(2)        

#%% nb et proportions de trajets par heure le jeudi 
poids_par_h(3)

#%% nb et proportions de trajets par heure le vendredi 
poids_par_h(4)

#%% nb et proportions de trajets par heure le samedi 
poids_par_h(5)

#%% nb et proportions de trajets par heure le dimanche 
poids_par_h(6)

#%% intensité de chaque trajet particulier 

def trajets_parcourus(j,h):
    D=[]
    T=[]
    U=[]
    F=[]
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            lecteur = csv.reader(f, delimiter=';')  # Définir le séparateur si nécessaire
            next(lecteur) #ignorer l'entête 
            for ligne in lecteur: 
                print(ligne)
                dat, heur = ligne[2].split(' ')
                dep=ligne[5].split(' ')[0]
                arr=ligne[6].split(' ')[0]
                date=datetime.strptime(dat, '%Y-%m-%d')
                jour=date.weekday()
                if jour==j:
                    if dep!='' and arr!='':
                        if dep in Sta and arr in Sta:
                            D.append([heur, dep, arr])
    #return D #récupération de tous les trajets pour les jours j
    for j in D:
        H=int(j[0].split(':')[0])
        if H==h:
            T.append([j[1],j[2]])
    #return T #récupérations de tous les trajets pour les jours j à l'heure h
    for I in T:
        if I not in U:
            U.append(I) 
    #return U #récupération de tous les trajets de façon unique
    for s in U:
        c=0
        for t in T:
            if t==s:
                c+=1
        F.append([s,c])
    return F #, len(T), len(D), len(T)/len(D) #récupération [station départ, station arrivée, nombre], et nombre de trajets total

 

#%%

def map_trajets(j, h):
    trajets=trajets_parcourus(j, h)
    stations_dict = {station[0]: station[1] for station in stations}
    N=nb_tot_jour(j)
    
    
    ville = "Montpellier, France"
    location = ox.geocode(ville)
    graphe = ox.graph_from_point(location, dist=10000, network_type="all", simplify=True)
    carte = folium.Map(location=location, zoom_start=13)

    #nb passages 
    edges_passages = defaultdict(int)

    for trajet in trajets:
        start, end = trajet[0]
        intensity = trajet[1]/N
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
        if passage_count < 1:
           color= "#0000ff" 
        else:     
            max_intensity = 50  # Ajuster selon les données
            passage_clamped = max(0, min(passage_count, max_intensity))  # Limiter à une plage raisonnable
            red = int(255 * (passage_clamped / max_intensity))
            green = int(255 * (1 - passage_clamped / max_intensity))
            color = f"#{red:02x}{green:02x}00"


        # Ajouter le segment
        folium.PolyLine(
            locations=coords,
            color=color,
            weight=4,  # Épaisseur fixe
            opacity=0.8,
            tooltip=f"Passages: {passage_count}"
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
        height: 140px;
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
        ">
        <b>Nombre de passages:</b><br>
        <i style="background: #0000ff; width: 20px; height: 10px; display: inline-block;"></i> Très faible (&lt;1)<br>
        <i style="background: #00ff00; width: 20px; height: 10px; display: inline-block;"></i> Faible (1-2)<br>
        <i style="background: #80ff00; width: 20px; height: 10px; display: inline-block;"></i> Modérée (3-5)<br>
        <i style="background: #ff0000; width: 20px; height: 10px; display: inline-block;"></i> Forte (&gt;5)<br>
    </div>
    """
    carte.get_root().html.add_child(folium.Element(legend_html))

    # Save la carte
    nom = f"trajets_couleurs_cumulées_j{j}_h{h}.html"
    carte.save(nom)
    return f"Carte enregistrée sous '{nom}'."

