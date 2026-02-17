from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

class SteamPromoScraper:
    def __init__(self):
        """Initialisation du driver et des variables"""
        self.driver = self._configurer_driver()
        self.wait = WebDriverWait(self.driver, 10)

    def _configurer_driver(self):
        """Configure les options du navigateur (Headless, User-Agent, etc.)"""
        options = webdriver.ChromeOptions()

        # Mode Headless
        options.add_argument("--headless=new") 

        # Taille de fenêtre (En headless c'est mieux de renseigner la taille de la fenêtre pour être sur que selenium puisse lire les infos)
        options.add_argument("--window-size=1920,1080")

        # User-Agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        options.add_argument(f'user-agent={user_agent}')

        # Anti-détection bot
        options.add_argument("--disable-blink-features=AutomationControlled")

        print("Lancement du scraper en arrière-plan (Headless)...")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def naviguer_vers_promos(self):
        """Navigue de l'accueil jusqu'à la page des promos"""
        self.driver.get("https://store.steampowered.com")

        # Accepter les cookies
        accept_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "acceptAllButton"))
        )
        accept_button.click()

        # Cliquer sur "Parcourir"
        bouton_parcourir = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Parcourir')]"))
            )
        bouton_parcourir.click()

        # Cliquer sur "Promos"
        bouton_promo = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'specials')]"))
        )
        bouton_promo.click()

    def scroller_page(self, scrolls=3, pause_time=1):
        """Fonction utilitaire pour scroller la page"""
        for i in range(scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"Scroll {i+1}/{scrolls}")
            time.sleep(pause_time)

    def charger_tous_les_jeux(self, nombre_de_tours=3):
        """Boucle principale de chargement (Scroll -> Clic Afficher Plus -> Scroll)"""
        print(f"Début du chargement étendu : {nombre_de_tours} tours prévus.")

        for i in range(nombre_de_tours):
            print(f"--- Tour {i+1} / {nombre_de_tours} ---")
            
            # Scroll pour atteindre le bouton
            self.scroller_page(scrolls=3, pause_time=1)
            
            try:
                # Clic sur le bouton
                bouton_afficherplus = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Afficher plus')]"))
                )
                bouton_afficherplus.click()
                print("✅ Bouton 'Afficher plus' cliqué !")
                
                # Pause (Pour être sûr de ne pas avoir de problèmes)
                time.sleep(3)
                
            except:
                print("⚠️ Bouton non trouvé ou fin de page atteinte. Arrêt de la boucle.")
                break

        # Scroll final
        print("Scroll final...")
        self.scroller_page(scrolls=3, pause_time=1)

    def extraire_et_sauvegarder(self, nom_fichier='jeux_steam.csv'):
        """Récupère les données et sauvegarde dans le CSV"""
        
        # Récupération de la liste des jeux (Dans le cas de Steam, il y'a des jeux à plusieurs endroits dans la page web, ici je contraint la recherche au coeur de la page)
        liste_jeux = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'sale_item_browser')]//div[contains(@class, 'ImpressionTrackedElement')]")
        print(f"Nombre de jeux trouvés (filtrés) : {len(liste_jeux)}")

        with open(nom_fichier, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # En-tête du CSV
            writer.writerow(["Titre", "Infos Prix", "Avis", "Résumé", "Tags", "Lien"])   
            
            for jeu in liste_jeux:
                print("------------------------------------------------")
                try:
                    # Titre
                    titre = jeu.find_element(By.XPATH, ".//img").get_attribute("alt")
                except:
                    titre = "Titre inconnu"

                try:
                    # Prix
                    infos_prix = jeu.find_element(By.XPATH, ".//div[contains(@class, 'StoreSalePriceWidgetContainer')]").get_attribute("aria-label")
                except:
                    infos_prix = "Pas de prix / Gratuit"

                try:
                    # Evaluation
                    infos_eval = jeu.find_element(By.XPATH, ".//a[contains(@class, 'ReviewScore')]//div[@aria-label]").get_attribute("aria-label")
                except:
                    infos_eval = "Pas d'évaluation"

                try:
                    # Résumé
                    resume = jeu.find_element(By.XPATH, ".//div[contains(@class, 'StoreSaleWidgetShortDesc')]").text
                except:
                    resume = "Pas de résumé disponible"
                
                try:
                    # Tags
                    elements_tags = jeu.find_elements(By.XPATH, ".//a[contains(@href, '/tags/')]")
                    
                    # Logique de nettoyage et de filtrage (On recupère le Tag brut sans caractères autour et on vérifie bien que la liste ne contient pas de Tags vides)
                    liste_tags_propre = [t.get_attribute("textContent").strip() for t in elements_tags]
                    liste_tags_propre = [tag for tag in liste_tags_propre if tag] 
                    
                    tags = ", ".join(liste_tags_propre)
                    if not tags:
                        tags = "Aucun tag"
                except:
                    tags = "Erreur récupération tags"
                
                try:
                    # Lien
                    lien = jeu.find_element(By.XPATH, ".//a[contains(@href, '/app/')]").get_attribute("href")
                    if "?" in lien:
                        lien = lien.split("?")[0]
                except:
                    lien = "Pas de lien trouvé"

                # Affichage dans le terminal
                print(f"Jeu : {titre}")
                print(f"Prix : {infos_prix}")
                print(f"Avis : {infos_eval}")
                print(f"Résumé : {resume}")
                print(f"Tags : {tags}")
                
                # Écriture dans le CSV
                writer.writerow([titre, infos_prix, infos_eval, resume, tags, lien])
                print(f"Sauvegardé : {titre}")

    def executer(self):
        """Lance toutes les étapes du scraping"""
        try:
            self.naviguer_vers_promos()
            self.charger_tous_les_jeux(nombre_de_tours=3) # Vous pouvez changer le nombre de tours ici (il y'a 12 jeux par tour)
            self.extraire_et_sauvegarder()
        finally:
            print("--- FIN DU SCRAPING ---")
            self.driver.quit() # Cette ligne permet d'être sur que le navigateur est fermé car on est en headless mode

# Point d'entrée du script 
if __name__ == "__main__":
    scraper = SteamPromoScraper()
    scraper.executer()
