<h1 align="center">CycleVision3</h1>

## 🌐 Project Website  
Visit our interactive site for visualizations and insights: [CycleVision3 - Interactive Bike Traffic Analysis](https://mscaia.github.io/PROJ_HAX712X/)

## 📖 Project Overview 
This project aims to analyze bike traffic in Montpellier, focusing on the investigation of bike-sharing rides and cyclist/pedestrian counts. We will leverage various datasets to visualize and predict bike traffic patterns, creating an interactive website to showcase our findings.

## 👥 Autors list

- [**ARMAND Charlotte**](https://github.com/CharlotteARMAND)
- [**CONDAMY Fabian**](https://github.com/FabianCondamy)
- [**SCAIA Matteo**](https://github.com/mscaia)
- [**STETSUN Kateryna**](https://github.com/KatyaStetsun)

## 🚀 Getting Started

Before beginning development and data analysis, you need to set up the working environment by installing all necessary dependencies. Follow these steps to prepare the project:

# Guide d'utilisation de notre projet
## 1. Introduction 
Ce guide vous explique comment utiliser notre projet, lancer les commandes nécessaires et accéder aux résultats générés.
## 2. Clone du répertoire Github
Pour accéder au projet et à sa structure, commencez par cloner notre répertoire GitHub.
```bash
git clone https://github.com/mscaia/PROJ_HAX712X.git
cd ./PROJ_HAX712X
```
## 3. Installation des packages nécessaire
On vous conseille de créer un environnement virtuel, il permet d'isoler les dépendances d'un projet, d'éviter les conflits de versions, et de garantir un contrôle simple sur les paquets installés. Il assure la reproductibilité du projet, facilite la gestion des dépendances, et protège votre système.
```bash
conda create --name Cycle3 python=3.9.18
conda activate Cycle3
```
Ensuite, installez les packages nécessaires pour faire fonctionner le projet :
```bash
pip install -r requirements.txt
```
Après cette commande, l'environnement virtuel `Cycle3` occupera environ 1 Go de votre espace. Vous êtes maintenant prêt à utiliser notre projet avec tous les packages nécessaires.
## 4. Comment lancer certain script.
Tous les scripts doivent être exécutés depuis le terminal. Assurez-vous que vous êtes dans la racine du projet, nommée `PROJ_HAX712X`. Dans les chemins relatifs, `./ `fait référence à la racine du projet.
### Utilisation de notre class pour télécharger les données
Téléchargez les données nécessaires pour travailler (nous avons choisi de les laisser sur GitHub) :
```bash
 python ./src/donnée.py
```
### Voir nos éléments d'analyse de donnée.
Pour voir les éléments d'analyse des données, lancez la commande suivante :
```bash
python ./Cycle3/analyse_donnee/statistique.py
```
Certaines sorties sont affichées dans le terminal (avec `print`), mais les graphiques sont disponibles dans le répertoire suivant :
```bash
cd ./docs/projet1_files/figure-html
```
Vous y trouverez des fichiers `.html` et `.png`.
### Visualisation des cartes
Dans le dossier `./Cycle3/map/`, vous trouverez trois fichiers `.py` différents pour travailler avec les cartes :
1. `carte.py` : Affiche la disponibilité en temps réel des vélos dans les stations Vélomagg de Montpellier.
```bash
 python ./Cycle3/map/carte.py 
```
La carte générée est sauvegardée dans `./docs/montpellier_bike_stations_map.html.`

2. `map.py` : Effectue une simulation de trajet. L'interactivité se fait via le terminal
```bash
 python ./Cycle3/map/map.py 
```
La carte générée est sauvegardée dans `./Cycle3/visualisation/carte_montpellier_trajet.html`

### Création d'une vidéo
Nous avons lié les scripts `./Cycle3/map/map_trajet_BD.py` et `./Cycle3/vidéo/vidéo.py` pour analyser les trajets d'un jour spécifique et les transformer en vidéo. 
#### Etape 1 : Choisir le jour dans `map_trajet_BD.py`
Lancez la commande suivante pour sélectionner le jour que vous souhaitez analyser. Vous aurez la possibilité de tracer ou non les trajets, et de définir le nombre de trajets à afficher.
```bash
 python ./Cycle3/map/map_trajet_BD.py
```
La carte générée est sauvegardée dans `./Cycle3/visualisation/carte_montpellier_trajet_via_BD.html`
#### Etape 2 : Création de la vidéo
**Attention : Ce processus peut être long. Veuillez vous référer à la section 8. Performance Analysis de la documentation pour plus d'informations.**
Lancez la commande suivante pour créer la vidéo :
```bash
 python ./Cycle3/vidéo/vidéo.py
```
Vous pourrez choisir le nombre de trajets à afficher. La vidéo générée sera sauvegardée dans `./Cycle3/visualisation/simulation_trajets.mp4`.
## 4. Création et utilisation du site 
Voici quelques étapes pour la création et l'utilisation d'un site Quarto comme celui que nous avons créé.
1. **Installation de Quarto**

Téléchargez et installez Quarto depuis [quarto.org/download](https://quarto.org/download). Prenez bien soin d'ajouter Quarto à vos variables d'environnements.

1. **Création du projet**

Puis, ouvrez un terminal et exécutez les commandes suivantes :
```bash
mkdir docs
cd docs
quarto create-project nom_du_projet --type website
```
1. **Ajout de contenu**
- Ajoutez des fichiers .qmd dans le dossier docs pour enrichir le site.
- Modifiez le fichier _quarto.yml pour personnaliser la structure et les paramètres du site.

1. **Prévisualisation locale**

Le site peut ensuite être lancé via la commande suivante dans le répertoire `./docs/`.
```bash
 quarto preview
```

1. **Déploiement sur GitHub**

Dans les paramètres de votre projet Github, allez dans GitHub Pages puis dans la section *Build and Deployment*. Dans l'onglet "Source" sélectionnez *Deploy from a branch* et en dessous sélectionnez la branche *main* et le dossier *docs*.
Vous pouvez ensuite taper les commandes suivantes (toujours dans le répertoire `./docs/`) dans un terminal :
```bash
 quarto render
 ```
Le site sera alors déployé à votre prochain push !

## 5. Suppression de l'environnement virtuel
1. Désactivez l'environnement
```bash
 conda deactivate
```
2. Supprimez l'environnement Conda
```bash
conda env remove --name Cycle3
```
3. Vérifiez que l'environnement a été supprimé
```bash
conda env list
```
Vous ne devez plus voir l'environnement `Cycle3`.
## 🔒 License

This project is licensed under the terms specified in the file [LICENCE](https://github.com/mscaia/PROJ_HAX712X/blob/main/LICENCE). Please refer to the file for more details.
