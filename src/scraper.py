import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd


def extraire_entreprises_suisses(code_html):
    print("🕵️ Analyse du HTML par BeautifulSoup...")
    
    # On sauvegarde temporairement la page pour pouvoir l'analyser si besoin
    with open("debug_google.html", "w", encoding="utf-8") as f:
        f.write(code_html)
    print("💾 Fichier temporaire 'debug_google.html' créé pour l'inspection.")
    
    soup = BeautifulSoup(code_html, 'html.parser')
    liste_entreprises = []
    
    # Google range souvent ses titres de résultats dans des balises <h3> ou des balises <a>
    # On va extraire à la fois les titres et les liens pour être sûrs de ne rien rater
    liens_et_titres = soup.find_all(['h3', 'a'])
    
    for element in liens_et_titres:
        texte = element.get_text().strip()
        
        # On cible uniquement les éléments qui contiennent des indices de LinkedIn
        if "linkedin.com" in texte or "LinkedIn" in texte:
            # Nettoyage des suffixes
            nom_propre = texte.replace(" | LinkedIn", "").replace(" - LinkedIn", "").replace("... - LinkedIn", "")
            # On élimine le bruit (les phrases trop longues ou trop courtes)
            if nom_propre not in liste_entreprises and 3 < len(nom_propre) < 80:
                liste_entreprises.append(nom_propre)
                
    return liste_entreprises

def capturer_page_google():
    with sync_playwright() as p:
        print("🤖 Initialisation du robot...")
        
        # On utilise des arguments pour rendre le navigateur un peu plus "humain"
        navigateur = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"] # Cache en partie le robot
        )
        
        # On configure un "User-Agent" classique pour ressembler à un vrai Windows
        contexte = navigateur.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = contexte.new_page()
        
        print("🌍 Navigation vers Google Suisse...")
        page.goto("https://www.google.ch")
        time.sleep(2)
        
        print("🛡️ Tentative de validation des cookies...")
        try:
            page.click("button:has-text('Tout accepter')", timeout=3000)
            print("✅ Cookies acceptés.")
        except Exception:
            print("ℹ️ Pas de pop-up de cookies détecté, on continue.")
            
        print("🔍 Saisie de la recherche ciblée...")
        requete = 'site:ch.linkedin.com/company "solution IT"'
        
        barre_recherche = "textarea[name='q'], input[name='q']"
        page.wait_for_selector(barre_recherche, timeout=5000)
        page.click(barre_recherche)
        page.fill(barre_recherche, requete)
        page.press(barre_recherche, "Enter")
        
        print("🚀 Recherche soumise. Analyse anti-robot en cours...")
        time.sleep(3)
        
        # --- DÉTECTION DU CAPTCHA ---
        if "google.com/recaptcha" in page.content() or "captcha" in page.url.lower():
            print("\n⚠️  ATTENTION : Google demande de résoudre un CAPTCHA !")
            print("👉 S'il te plaît, résous le captcha directement dans la fenêtre du navigateur ouverte sur ton écran.")
            
            # Le robot attend patiemment jusqu'à ce que l'URL change ou que les résultats apparaissent
            # On lui dit d'attendre que la balise des résultats de recherche (#search) soit visible
            try:
                page.wait_for_selector("#search", timeout=120000) # Tu as 2 minutes pour le résoudre !
                print("✅ Captcha résolu ! Reprise du script...")
            except Exception:
                print("❌ Temps d'attente dépassé pour résoudre le captcha.")
        else:
            print("🟢 Pas de blocage détecté, poursuite normale.")
            time.sleep(3)
            
        print("📦 Récupération du code HTML brut...")
        code_html_brut = page.content()
        
        navigateur.close()
        print("🎉 Capture réussie !")
        return code_html_brut
    
if __name__ == "__main__":
    print("🏁 Démarrage du script principal...")
    # 1. Le robot récupère le HTML
    html_recupere = capturer_page_google()
    
    # 2. Le parser trie les résultats
    entreprises_trouvees = extraire_entreprises_suisses(html_recupere)
    
    # 3. On affiche la récolte et on l'enregistre
    print("\n🚀 --- LISTE DES ENTREPRISES IT SUISSES CAPTURÉES ---")
    if entreprises_trouvees:
        for index, nom in enumerate(entreprises_trouvees, 1):
            print(f"{index}. {nom}")
            
        # --- EXPORT EXCEL ---
        print("\n💾 Enregistrement des données dans Excel...")
        
        # On crée un dictionnaire propre pour notre tableau
        donnees = {
            "Nom de l'entreprise / Résultat": entreprises_trouvees
        }
        
        # On transforme ça en DataFrame Pandas
        df = pd.DataFrame(donnees)
        
        # On exporte en fichier Excel
        nom_fichier = "entreprises_suisses.xlsx"
        df.to_excel(nom_fichier, index=False)
        
        print(f"✅ Succès ! Le fichier '{nom_fichier}' a bien été créé à la racine de ton projet.")
        
    else:
        print("❌ Aucune entreprise trouvée dans les balises sélectionnées.")
    print("-----------------------------------------------------")