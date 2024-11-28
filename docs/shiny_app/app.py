import osmnx as ox
import folium
import pandas as pd
from shiny import App, render, ui
from src.fonctions_basedonnees import *  # Assurez-vous que ces fonctions sont accessibles

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
                        gen_carte_trajet(trajets_du_jour.iloc[i], G, m, 1, 2,'green')  # Ajout de la carte de chaque trajet à la carte globale
                    elif 2000<trajets_du_jour.loc[i, 'Covered distance (m)']<4000 :
                        gen_carte_trajet(trajets_du_jour.iloc[i], G, m, 1, 2, 'blue')  # Ajout de la carte de chaque trajet à la carte globale
                    else:
                        gen_carte_trajet(trajets_du_jour.iloc[i], G, m, 1, 2, 'red')  # Ajout de la carte de chaque trajet à la carte globale
            # Convertir la carte Folium en HTML
            folium_html = m._repr_html_()

            # Renvoyer le contenu HTML directement dans Shiny
            return ui.HTML(folium_html)
        else:
            return ui.tags.div("Cliquez sur 'Afficher la carte' pour générer une carte.")

# Créer et exécuter l'application Shiny
app = App(app_ui, server)
app