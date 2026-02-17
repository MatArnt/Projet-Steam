# Projet-Steam

# 🎮 Steam Hunter v3.0

> **L'outil ultime pour traquer les meilleures promotions sur Steam en temps réel.**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Web%20Scraping-green?style=for-the-badge&logo=selenium)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)

## 📋 Description

**Steam Hunter** est une solution complète d'automatisation et d'analyse de données.
Il permet de récupérer automatiquement (Scraping) les offres de la section "Promotions" de Steam, puis d'analyser ces données via une interface graphique interactive pour trouver les pépites cachées (ex: jeux à -50% avec des avis "Très positifs").

### ✨ Fonctionnalités Clés
* **🕵️‍♂️ Scraping Furtif :** Utilise un navigateur "Headless" et User-Agent réaliste.
* **🔄 Scroll Infini Automatisé :** Le script gère le chargement dynamique tout seul.
* **📊 Analyse Intelligente :** Une interface graphique (GUI) pour filtrer par :
    * Budget max (€)
    * Pourcentage de réduction (%)
    * Avis des joueurs (Positifs, Moyens...)
    * Tags (RPG, Aventure, Indé...)
* **📂 Export CSV :** Toutes les données sont sauvegardées proprement dans `jeux_steam.csv`.
* **🔗 Liens Cliquables :** Accès direct à la page magasin du jeu depuis l'interface.

---

## 🛠️ Installation

Suivez ces étapes pour lancer le projet sur votre machine.

### 1. Prérequis
* Avoir **Python** installé sur votre ordinateur.
* Avoir **Google Chrome** installé (le script utilise ses drivers).

### 2. Cloner ou Télécharger
Téléchargez le dossier du projet et ouvrez-le dans votre éditeur de code (VS Code recommandé).

### 3. Installer les dépendances
Ouvrez un terminal dans le dossier du projet et lancez la commande suivante :

```bash
python -m pip install -r requirements.txt
```
## 🚀 Utilisation
Le projet utilise un lanceur unique pour simplifier la tâche.

### Étape 1 : Lancer le programme
Dans votre terminal, tapez :

```Bash
python main.py
```

### Étape 2 : Le Scraping (Récupération)
Le terminal vous demandera :
- Voulez-vous lancer le scraping (récupération des promos) ? (o/n)
- Tapez o (oui) pour lancer le robot.
- Attendez que le terminal affiche ✅ Scraping terminé !
- Note : Chrome ne s'ouvrira pas visiblement, tout se passe en arrière-plan.

Ps : Dans le fichier python scrapper.py vous pouvez modifier la boucle pour charger plus de jeux dans le CSV.

### Étape 3 : L'Analyse (Interface)
- Une fois le scraping fini (ou si vous avez répondu 'n'), la fenêtre Steam Hunter s'ouvre.
- Choisissez vos critères (ex: Prix max 20€, Avis "très positives").
- Cliquez sur "CHASSER LES OFFRES".
- Une liste de résultats apparaît. Cliquez sur le titre d'un jeu pour l'acheter !

## 📂 Structure du Projet
Voici comment les fichiers sont organisés :

```bash
Projet-Steam/
│
├── main.py              # 🏁 Le chef d'orchestre (lance le scraping puis l'interface)
├── requirements.txt     # 📦 Liste des librairies nécessaires
├── README.md            # 📖 Ce fichier que vous lisez
│
└── src/                 # ⚙️ Code source (Le moteur)
    ├── scraper.py       # 🤖 Le robot Selenium (classe SteamPromoScraper)
    └── analyzer.py      # 🖥️ L'interface graphique Tkinter (classe SteamHunterApp)
```

## ⚖️ Disclaimer
Ce projet a été réalisé dans un but pédagogique pour apprendre l'automatisation avec Python, Selenium et Tkinter.
L'utilisation intensive de bots sur les sites web peut être soumise à restrictions. Merci d'utiliser cet outil de manière responsable.

