Bibliothèques utilisées
==========================

Dans le cadre de ce projet, plusieurs bibliothèques ont été utilisées pour répondre aux différents besoins techniques et analytiques. Voici une présentation des bibliothèques principales et leur rôle.

* **concurrent.futures.ThreadPoolExecutor**  
  ``ThreadPoolExecutor`` est une fonctionnalité du module standard ``concurrent.futures`` pour exécuter des tâches en parallèle.  
  Elle est utilisée pour optimiser le traitement des données et accélérer le rendu des animations dans le cadre de ce projet.

* **csv**  
  La bibliothèque ``csv`` permet de lire et d’écrire des fichiers CSV, un format commun pour manipuler des données tabulaires.  
  Nous avons utilisé ``csv`` pour extraire et traiter les données brutes contenues dans des fichiers au format CSV. Cela est particulièrement utile pour manipuler des ensembles de données simples où une lecture ligne par ligne est nécessaire.

* **datetime**  
  ``datetime`` est un module intégré pour manipuler les dates et les heures.  
  Dans le projet, il est employé pour traiter les données temporelles des trajets cyclistes et synchroniser les animations avec les horodatages.

* **folium**  
  ``folium`` est une bibliothèque dédiée à la création de cartes interactives.  
  Nous avons utilisé ``folium`` pour visualiser les trajets et itinéraires des vélos sur des cartes interactives, permettant une meilleure compréhension géographique des données.

* **functools.lru_cache**  
  ``functools.lru_cache`` est une fonctionnalité de Python pour optimiser les performances.  
  En mettant en cache les résultats des fonctions fréquemment appelées, ``functools.lru_cache`` améliore les performances et réduit le temps de calcul pour des opérations répétées.

* **json**  
  ``json`` est utilisée pour manipuler des données au format JSON, un standard de stockage et d’échange d’informations structurées.  
  Nous utilisons ``json`` pour lire et écrire des données structurées, notamment pour gérer les configurations et les résultats intermédiaires dans des fichiers légers.

* **matplotlib.animation.FuncAnimation** et **FFMpegWriter**  
  Ces modules de la bibliothèque ``matplotlib.animation`` permettent de créer des animations et d'exporter celles-ci sous forme de fichiers vidéo.  
  Dans le projet, ils sont utilisés pour générer des animations illustrant les variations temporelles du trafic cycliste et les enregistrer sous un format visuel accessible.

* **matplotlib.pyplot**  
  ``matplotlib.pyplot`` est utilisée pour produire des graphiques statiques et des visualisations animées.  
  Dans ce projet, elle permet de créer des graphiques dynamiques illustrant les trajectoires cyclistes et d’exporter ces visualisations sous forme de vidéos à l'aide des modules ``FuncAnimation`` et ``FFMpegWriter``.

* **networkx**  
  ``networkx`` est une bibliothèque dédiée à la création, la manipulation et l'analyse de graphes complexes.  
  Dans ce projet, elle est utilisée pour représenter et étudier les réseaux cyclistes, notamment pour visualiser les trajets et calculer les chemins les plus courts entre les nœuds.

* **numpy**  
  ``numpy`` est une bibliothèque puissante pour effectuer des calculs numériques avancés, notamment des opérations matricielles.  
  Les opérations matricielles et les calculs numériques complexes nécessaires à l’analyse des données sont simplifiés grâce à ``numpy``, qui garantit également des performances élevées.

* **os**  
  ``os`` fournit des fonctions pour interagir avec le système d’exploitation, notamment pour gérer les fichiers et les répertoires.  
  Nous avons utilisé ``os`` pour gérer les chemins des fichiers, vérifier l’existence des répertoires, et manipuler les ressources locales du système.

* **osmnx**  
  ``osmnx`` est utilisée pour le géocodage et l’analyse des réseaux géographiques.  
  Cette bibliothèque permet d’extraire des données géographiques d’OpenStreetMap, de construire des graphes routiers, et d’analyser les itinéraires et les trajets cyclistes dans le cadre de ce projet.

* **pandas**  
  ``pandas`` est essentielle pour manipuler et analyser des données tabulaires de manière efficace.  
  ``pandas`` est utilisée pour nettoyer, transformer et analyser des ensembles de données complexes, offrant des fonctionnalités avancées comme le traitement des séries temporelles et des jointures de tables.

* **pooch**  
  ``pooch`` facilite le téléchargement et la mise en cache des fichiers nécessaires à l’exécution du projet.  
  Cette bibliothèque permet de garantir un accès fiable aux données externes en les téléchargeant automatiquement et en les stockant localement pour une réutilisation future.

* **re**  
  La bibliothèque ``re`` permet de travailler avec des expressions régulières pour manipuler des chaînes de caractères.  
  Grâce à ``re``, nous avons pu extraire des informations spécifiques des chaînes de caractères et nettoyer les données textuelles de manière efficace.

* **unicodedata**  
  ``unicodedata`` est utilisée pour normaliser les chaînes de caractères Unicode.  
  Cette bibliothèque est essentielle pour traiter les caractères spéciaux et garantir la cohérence des chaînes de caractères provenant de différentes sources.

* **zipfile**  
  La bibliothèque ``zipfile`` permet de travailler avec des fichiers au format ZIP, un format couramment utilisé pour la compression et l'archivage de fichiers.  
  Nous avons utilisé ``zipfile`` pour extraire des fichiers compressés afin de récupérer les données nécessaires à notre projet. Cette bibliothèque offre une interface simple pour l'extraction, la création et la gestion des archives ZIP, ce qui facilite le traitement des données compressées.
