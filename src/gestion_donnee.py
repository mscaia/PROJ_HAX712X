import os
import pandas as pd
import pooch
import zipfile

class GestionnaireDonnees:
    """
    Une classe pour gérer le téléchargement, la lecture et le traitement des jeux de données.
    """
    def __init__(self, repertoire_telechargement="./data"):
        self.repertoire_telechargement = repertoire_telechargement
        os.makedirs(self.repertoire_telechargement, exist_ok=True)

    def telecharger_fichier(self, url, nom_fichier):
        chemin = pooch.retrieve(
            url=url,
            known_hash=None,
            fname=nom_fichier,
            path=self.repertoire_telechargement
        )
        return chemin

    def charger_csv(self, chemin_fichier, supprimer_na=True):
        dataframe = pd.read_csv(chemin_fichier)
        if supprimer_na:
            dataframe = dataframe.dropna()
        return dataframe

    def extraire_zip(self, chemin_zip, dossier_extraction=None):
        if dossier_extraction is None:
            dossier_extraction = os.path.join(self.repertoire_telechargement, "extrait")
        os.makedirs(dossier_extraction, exist_ok=True)
        with zipfile.ZipFile(chemin_zip, 'r') as zip_ref:
            zip_ref.extractall(dossier_extraction)
        os.remove(chemin_zip)
        return dossier_extraction
