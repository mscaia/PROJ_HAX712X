import os,sys
# Ajouter la racine du projet au chemin Python
racine_du_projet = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, racine_du_projet)

# Import de la classe GestionnaireDonnees
from src.gestion_donnee import *

# Créer une instance de GestionnaireDonnees
gestionnaire = GestionnaireDonnees(repertoire_telechargement="./data")

# Exemple : Téléchargement et traitement des données
# 1er jeu de données
url1 = "https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_CoursesVelomagg.csv"
chemin1 = gestionnaire.telecharger_fichier(url1, "CoursesVelomagg.csv")
df1 = gestionnaire.charger_csv(chemin1)

# 2ème jeu de données (ZIP)
url3 = "https://data.montpellier3m.fr/node/12668/download"
chemin_zip = gestionnaire.telecharger_fichier(url3, "fichier.zip")
dossier_extrait = gestionnaire.extraire_zip(chemin_zip)

print("Téléchargement et traitement terminé.")
