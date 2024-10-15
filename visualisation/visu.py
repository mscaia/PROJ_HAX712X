import pandas as pd
import json
import requests
from fonctions_basedonnees import json_process

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H19070220_archive.json"
data = json_process(url,"../data/EcoCompt1.json")