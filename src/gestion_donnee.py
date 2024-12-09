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
        """
        telecharger_fichier(self, url, nom_fichier)
        Télécharge un fichier depuis une URL spécifiée et le sauvegarde dans le répertoire de téléchargement. Le fichier est récupéré à l'aide de la bibliothèque `pooch`.
        Args :
        - url : str
            L'URL du fichier à télécharger.
        - nom_fichier : str
            Le nom sous lequel le fichier sera sauvegardé dans le répertoire de téléchargement.
        Returns:
        - str : Le chemin local où le fichier a été téléchargé.
        """
        chemin = pooch.retrieve(
            url=url,
            known_hash=None,
            fname=nom_fichier,
            path=self.repertoire_telechargement
        )
        return chemin

    def charger_csv(self, chemin_fichier, supprimer_na=True):
        """
        charger_csv(self, chemin_fichier, supprimer_na=True)
        Charge un fichier CSV dans un DataFrame pandas. Par défaut, les lignes contenant des valeurs manquantes sont supprimées.
        
        Args :
        - chemin_fichier : str
            Le chemin vers le fichier CSV à charger.
        - supprimer_na : bool, optionnel
            Si `True`, les lignes contenant des valeurs manquantes sont supprimées. Par défaut, `True`.

        Returns:
        - pandas.DataFrame : Le DataFrame contenant les données du fichier CSV.
        """
        dataframe = pd.read_csv(chemin_fichier)
        if supprimer_na:
            dataframe = dataframe.dropna()
        return dataframe

    def extraire_zip(self, chemin_zip, dossier_extraction=None):
        """
        extraire_zip(self, chemin_zip, dossier_extraction=None)
        Extrait le contenu d'une archive ZIP dans un dossier spécifié ou dans un dossier par défaut. Après extraction, le fichier ZIP est supprimé.
        Args :
        - chemin_zip : str
            Le chemin du fichier ZIP à extraire.
        - dossier_extraction : str, optionnel
            Le dossier où extraire les fichiers. Si non fourni, un dossier `extracted` sera créé dans le répertoire de téléchargement.

        Returns: 
        - str : Le chemin du dossier où les fichiers ont été extraits.
        """
        if dossier_extraction is None:
            dossier_extraction = os.path.join(self.repertoire_telechargement, "extracted")
        os.makedirs(dossier_extraction, exist_ok=True)
        with zipfile.ZipFile(chemin_zip, 'r') as zip_ref:
            zip_ref.extractall(dossier_extraction)
        os.remove(chemin_zip)
        return dossier_extraction
