Objectif du projet

Le but était de construire un scraper complet capable de :
Parcourir toutes les catégories du site
Extraire les informations de chaque livre : titre, prix, disponibilité, note, image, etc.
Enregistrer ces données dans des fichiers CSV
Télécharger les images de couverture des livres
Et enfin, faire une petite analyse des prix et des notes avec pandas
 
Outils utilisés

Python 3.10+
requests → pour télécharger les pages web
pandas → pour organiser et analyser les données
scrapy.Selector → pour extraire le contenu HTML
os / time → pour la gestion des fichiers et temporisations

Installation

Cloner le dépôt

git clone git@github.com:jeremyyy05/ProjetsPython.git
cd ProjetsPython
git add.
git commit -m "message"
git push -u main origin

Installer les dépendances

pip install -r requirements.txt

Lancer le projet
Pour exécuter le scraper :
python books_to_scrape.py
Les données seront enregistrées automatiquement dans :
outputs/csv/ → pour les fichiers CSV
outputs/images/ → pour les images des livres

Exemple d’analyse

Une fois les CSV créés, on peut facilement analyser les données avec pandas :
import pandas as pd
df = pd.read_csv("outputs/csv/category_poetry.csv")
df["Prix (£)"] = df["Prix (£)"].astype(float)
print("Prix moyen :", round(df["Prix (£)"].mean(), 2), "£")
print("Nombre de livres :", len(df))
print("\nRépartition des notes :")
print(df["Note"].value_counts())

Ce que j’ai appris

Ce projet m’a permis de :

Comprendre le fonctionnement du web scraping
Manipuler et structurer des données avec pandas
Automatiser des tâches répétitives en Python
Et surtout, mieux organiser mon code pour un vrai projet

Auteur

Jeremy Lin
Étudiant à l’EFREI Paris
En bachelor cybersecurite ethical hacking 