import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

# --- LA PARTIE DONNÉES (LE CERVEAU) ---
class SteamDataManager:
    """Cette classe sert à charger, nettoyer et filtrer la liste des jeux."""
    
    def __init__(self, file_path):
        # Au démarrage, on charge les données depuis le fichier CSV
        self.df = self._load_and_clean(file_path)

    def _load_and_clean(self, path):
        """Charge le fichier et prépare les colonnes pour qu'elles soient utilisables."""
        try:
            df = pd.read_csv(path)
            
            # On transforme le texte des prix en vrais nombres pour pouvoir faire des calculs
            df['Prix_Net'] = df['Infos Prix'].str.extract(r'à\s*([\d,]+)').replace(',', '.', regex=True).astype(float)
            
            # On extrait le pourcentage de promo (ex: "50%" devient 50)
            df['Reduc_Val'] = df['Infos Prix'].str.extract(r'(\d+)\s*%').astype(float).fillna(0)
            
            # On remplace les cases vides par du texte vide pour éviter les erreurs de recherche
            df['Avis_Lower'] = df['Avis'].str.lower().fillna("")
            df['Tags'] = df['Tags'].fillna("")
            df['Lien'] = df['Lien'].fillna("")
            return df
        except Exception as e:
            # Si le fichier CSV est introuvable ou mal fait, on affiche une erreur
            print(f"Erreur lors de la lecture des données : {e}")
            return None

    def get_unique_tags(self):
        """Crée une liste propre de tous les styles de jeux (tags) sans doublons."""
        if self.df is None: return []
        all_tags = set()
        for row in self.df['Tags'].str.split(','):
            all_tags.update([t.strip() for t in row if t.strip()])
        return sorted(list(all_tags))

    def filter_games(self, min_reduc, max_price, sentiment, selected_tags):
        """Applique les filtres choisis par l'utilisateur (prix, promo, avis, tags)."""
        # Filtre sur la promo, le prix et les avis
        mask = (self.df['Reduc_Val'] >= min_reduc) & \
               (self.df['Prix_Net'] <= max_price) & \
               (self.df['Avis_Lower'].str.contains(sentiment))

        # On ajoute les filtres pour chaque tag sélectionné (s'il n'est pas sur "Aucun")
        for tag in selected_tags:
            if tag != "Aucun":
                mask = mask & (self.df['Tags'].str.contains(tag, case=False))
        
        return self.df[mask]


# --- LA FENÊTRE DES RÉSULTATS (LA LISTE) ---
class ResultsWindow(tk.Toplevel):
    """Crée une deuxième fenêtre pour afficher les jeux trouvés."""
    
    def __init__(self, parent, results):
        super().__init__(parent)
        self.title(f"Jeuxs trouvées ({len(results)})")
        self.geometry("450x500")
        self._build_ui(results)

    def _build_ui(self, results):
        """Prépare l'affichage de la liste avec une barre de défilement."""
        self.canvas = tk.Canvas(self) 
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollable_frame = ttk.Frame(self.canvas)

        # Permet à la zone de défilement de s'ajuster à la taille du contenu
        scrollable_frame.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # On active la molette de la souris pour naviguer dans la liste
        self.bind_all("<MouseWheel>", self._on_mousewheel) # Windows/Mac

        # Pour chaque jeu trouvé, on crée un petit bloc d'affichage
        for _, game in results.iterrows():
            card = ttk.Frame(scrollable_frame, padding=10)
            card.pack(fill=tk.X)

            # Titre du jeu (cliquable pour ouvrir la page Steam)
            link_label = tk.Label(card, text=game['Titre'], fg="#1a73e8", cursor="hand2", 
                                  font=("Helvetica", 11, "bold", "underline"), wraplength=400, justify="left")
            link_label.pack(anchor=tk.W)
            link_label.bind("<Button-1>", lambda e, url=game['Lien']: webbrowser.open_new(url))

            # Ligne avec le prix et la réduction
            info_text = f"💰 {game['Prix_Net']}€ | Réduction : -{int(game['Reduc_Val'])}%"
            tk.Label(card, text=info_text, font=("Helvetica", 9)).pack(anchor=tk.W)
            
            # Petite ligne de séparation entre les jeux
            ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', padx=20, pady=5)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(self, event):
        """Gère le mouvement de la molette de la souris selon le système d'exploitation."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


# --- LA FENÊTRE PRINCIPALE (L'APPLI) ---
class SteamHunterApp:
    """Fenêtre principale où l'on choisit ses critères de recherche."""
    def __init__(self, root, file_path):
        self.root = root
        self.root.title("Steam Hunter v3.0")
        self.root.geometry("500x750")
        
        # On initialise la gestion des données
        self.data_manager = SteamDataManager(file_path)
        
        # Si les données sont chargées, on affiche l'interface, sinon on montre une erreur
        if self.data_manager.df is not None:
            self._setup_main_ui()
        else:
            messagebox.showerror("Erreur Fatale", "Fichier de données introuvable ou corrompu.")

    def _setup_main_ui(self):
        """Crée tous les boutons et menus de la fenêtre principale."""
        main_container = ttk.Frame(self.root, padding="25")
        main_container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_container, text="🎯 Steam Hunter", font=('Helvetica', 18, 'bold')).pack(pady=15)

        # Menus déroulants pour la réduction, les avis et le prix max
        self.reduc_var = self._create_label_and_cb(main_container, "Réduction minimum :", 
                                                   [f"{i}%" for i in range(0, 100, 5)], "10%")
        
        self.avis_var = self._create_label_and_cb(main_container, "Avis des joueurs :", 
                                                  ["positives", "moyennes", "négatives"], "positives")
        
        self.prix_var = self._create_label_and_cb(main_container, "Budget max (€) :", 
                                                  [f"{i}" for i in range(0, 105, 5)], "35")

        # Section pour choisir jusqu'à 3 tags (styles de jeux)
        ttk.Separator(main_container, orient='horizontal').pack(fill='x', pady=20)
        ttk.Label(main_container, text="Filtres par Tags (max 3) :", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)

        tag_list = ["Aucun"] + self.data_manager.get_unique_tags()
        self.tag_vars = []
        for _ in range(3):
            var = tk.StringVar(value="Aucun")
            cb = ttk.Combobox(main_container, textvariable=var, values=tag_list, state="readonly")
            cb.pack(fill=tk.X, pady=3)
            self.tag_vars.append(var)

        # Gros bouton pour lancer la recherche
        btn = ttk.Button(main_container, text="CHASSER LES OFFRES", command=self._on_search_clicked)
        btn.pack(fill=tk.X, pady=30)

    def _create_label_and_cb(self, parent, label_text, values, default):
        """Petit outil pour créer un texte suivi d'un menu déroulant."""
        ttk.Label(parent, text=label_text, font=('Helvetica', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        var = tk.StringVar(value=default)
        cb = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
        cb.pack(fill=tk.X, pady=5)
        return var

    def _on_search_clicked(self):
        """Action déclenchée quand on clique sur le bouton de recherche."""
        try:
            # On récupère les choix faits dans l'interface
            reduc = float(self.reduc_var.get().replace('%', ''))
            budget = float(self.prix_var.get())
            sentiment = self.avis_var.get()
            tags = [v.get() for v in self.tag_vars]

            # On demande au "cerveau" de filtrer les jeux
            results = self.data_manager.filter_games(reduc, budget, sentiment, tags)

            # Si on trouve des jeux, on ouvre la fenêtre des résultats, sinon on prévient l'utilisateur
            if not results.empty:
                ResultsWindow(self.root, results)
            else:
                messagebox.showinfo("Bredouille", "Aucun jeu ne correspond à vos critères.")
        except ValueError:
            messagebox.showwarning("Attention", "Veuillez vérifier vos filtres.")

# Lancement du programme
if __name__ == "__main__":
    root = tk.Tk()
    app = SteamHunterApp(root, "jeux_steam.csv")
    
    root.mainloop()

