import os
import time
import sys
from src.scraper import SteamPromoScraper

# On essaie d'importer l'analyseur. 
# Si ça échoue, on évite de faire planter tout le script tout de suite.
try:
    from src.analyzer import lancer_interface
except ImportError as e:
    print(f"⚠️ Attention : Impossible d'importer l'analyseur ({e}).")
    lancer_interface = None

def main():
    print("========================================")
    print("🎮 STEAM HUNTER - OUTIL COMPLET")
    print("========================================")

    # Partie 1 : Scrapping
    choix = input("Voulez-vous lancer le scraping (récupération des promos) ? (o/n) : ").lower()
    
    if choix == 'o' or choix == 'y':
        print("\n🚀 Lancement du Scraper...")
        try:
            bot = SteamPromoScraper()
            bot.executer() # Lance tout le processus de scraping
            print("✅ Scraping terminé ! Le fichier 'jeux_steam.csv' est à jour.")
        except Exception as e:
            print(f"❌ Erreur critique pendant le scraping : {e}")
            input("Appuyez sur Entrée pour quitter...")
            return
    else:
        print(">> Scraping ignoré. On utilise les données existantes.")

    # Pause pour être sûr que le fichier est bien libéré
    time.sleep(1)

    # Partie 2 : Analyser 
    print("\n📊 Lancement de l'Interface d'Analyse...")
    
    if not os.path.exists("jeux_steam.csv"):
        print("❌ Erreur : Le fichier 'jeux_steam.csv' est introuvable !")
        print("💡 Conseil : Lancez le scraping au moins une fois pour générer les données.")
        input("Appuyez sur Entrée pour quitter...")
        return

    if lancer_interface:
        print("Ouverture de la fenêtre... (Regardez votre barre des tâches si elle n'apparaît pas)")
        lancer_interface()
    else:
        print("❌ Erreur : Le module d'analyse n'a pas pu être chargé.")

    print("\n========================================")
    print("👋 Fin du programme.")
    print("========================================")

if __name__ == "__main__":
    main()
