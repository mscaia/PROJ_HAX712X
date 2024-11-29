import osmnx as ox
import folium
import pandas as pd
from shiny import App, render, ui
import re
import unicodedata
from functools import lru_cache

## FONCTIONS

@lru_cache(maxsize=None)
def coordonne(station):
    try:
        # Recherche de l'emplacement en utilisant osmnx
        location = ox.geocode(f"{station}, Montpellier, France")
        return location[0], location[1]
    except Exception as e:
        print(f"Erreur pour la station {station}: {e}")
        return None, None

# Fonction qui permet d'enleve les bruits dans les chaines de caractère d'un dataframe
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
def gen_carte_trajet(ligne, G, m, index_colonne_départ, index_colonne_arrive,couleur):
    # Essayer de géocoder les stations de départ et d'arrivée
    try:
        origin = ox.geocode(f"{ligne['Departure station']}, Montpellier, France") # Départs
        destination = ox.geocode(f"{ligne['Return station']}, Montpellier, France") # Arrivées
        
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
        folium.PolyLine(locations=route_coords, color=couleur, weight=5, opacity=0.75).add_to(m)

        # Ajouter des marqueurs pour l'origine et la destination
        départ_lat, départ_lon = route_coords[0]
        arr_lat, arr_lon = route_coords[-1]  # Utiliser le dernier point pour l'arrivée
        folium.Marker(location=[départ_lat, départ_lon], popup=f"{ligne[index_colonne_départ]},Départ").add_to(m)
        folium.Marker(location=[arr_lat, arr_lon], popup=f"{ligne[index_colonne_arrive]},arrivé").add_to(m)

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    
    return m


# Effacer le cache
coordonne.cache_clear()

# Configuration initiale
ville = "Montpellier, France"
G = ox.graph_from_place(ville, network_type="all")

# Charger le DataFrame
df_coursesvelomagg_traité = pd.read_csv("data/CoursesVelomagg.csv").dropna()
liste_des_trajets = df_coursesvelomagg_traité[['Departure', 'Departure station', 'Return station', 'Covered distance (m)', 'Duration (sec.)']]

# Nettoyer et normaliser les colonnes
liste_des_trajet_DBF = liste_des_trajets.copy()
liste_des_trajet_DBF['Departure station'] = liste_des_trajet_DBF['Departure station'].apply(nettoyer_adresse_normalise)
liste_des_trajet_DBF['Return station'] = liste_des_trajet_DBF['Return station'].apply(nettoyer_adresse_normalise)

# Remplacements spécifiques
liste_des_trajet_DBF['Departure station'] = liste_des_trajet_DBF['Departure station'].replace("FacdesSciences", "Faculté des sciences")
liste_des_trajet_DBF['Return station'] = liste_des_trajet_DBF['Return station'].replace("FacdesSciences", "Faculté des sciences")
liste_des_trajet_DBF['Departure station'] = liste_des_trajet_DBF['Departure station'].replace(r".*Gare Saint-Roch$", "Gare Saint-Roch", regex=True)
liste_des_trajet_DBF['Return station'] = liste_des_trajet_DBF['Return station'].replace(r".*Gare Saint-Roch$", "Gare Saint-Roch", regex=True)

# Liste des dates disponibles
Liste_des_dates = liste_des_trajet_DBF['Departure'].str[:10].unique()
Liste_des_dates = Liste_des_dates.tolist()

# Recherche du problème
ligne_test = liste_des_trajet_DBF.iloc[0]
print("Valeur pour l'index 1 :", ligne_test[1])
print("Valeur pour l'index 2 :", ligne_test[2])

app_ui = ui.page_fluid(
    ui.panel_title("Carte interactive des trajets"),
    ui.input_select(
        "date_select",
        "Choisissez une date :",
        choices=liste_des_trajet_DBF['Departure'].str[:10].unique().tolist(),  # Conversion explicite en liste
    ),
    ui.input_checkbox("tracer", "Tracer les trajets ?"),
    ui.input_slider("nb_trajets", "Nombre de trajets :", min=1, max=10, value=5),
    ui.input_action_button("tracer_btn", "Afficher la carte"),
    ui.output_ui("carte_output")
)

def server(input, output, session):
    @output
    @render.ui
    def carte_output():
        if input.tracer_btn() > 0:
            # Récupérer les valeurs des widgets
            selected_date = input.date_select()
            tracer = input.tracer()
            nb_trajets = input.nb_trajets()

            # Filtrer les trajets pour la date sélectionnée
            trajets_du_jour = liste_des_trajet_DBF[liste_des_trajet_DBF['Departure'].str.startswith(selected_date)].reset_index(drop=True)
            print(f"Nombre de trajets trouvés pour {selected_date}: {len(trajets_du_jour)}")
            nb_ref = len(trajets_du_jour)

            # Créer la carte centrée sur Montpellier
            m = folium.Map(location=[43.6114, 3.8767], zoom_start=13)

            if tracer:
                for i in range(min(nb_trajets, nb_ref)):
                    trajet = trajets_du_jour.iloc[i]
                    print(f"Affichage du trajet {i+1}")
                    if trajets_du_jour.loc[i, 'Covered distance (m)']<2000 :
                        gen_carte_trajet(trajets_du_jour.iloc[i], G, m, 'Departure station', 'Return station','green')  # Ajout de la carte de chaque trajet à la carte globale
                    elif 2000<trajets_du_jour.loc[i, 'Covered distance (m)']<4000 :
                        gen_carte_trajet(trajets_du_jour.iloc[i], G, m, 'Departure station', 'Return station', 'blue')  # Ajout de la carte de chaque trajet à la carte globale
                    else:
                        gen_carte_trajet(trajets_du_jour.iloc[i], G, m, 'Departure station', 'Return station', 'red')  # Ajout de la carte de chaque trajet à la carte globale
            # Convertir la carte Folium en HTML
            folium_html = m._repr_html_()

            # Renvoyer le contenu HTML directement dans Shiny
            return ui.HTML(folium_html)
        else:
            return ui.tags.div("Cliquez sur 'Afficher la carte' pour générer une carte.")

# Créer et exécuter l'application Shiny
app = App(app_ui, server)
app
