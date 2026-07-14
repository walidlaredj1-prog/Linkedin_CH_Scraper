from bs4 import BeautifulSoup

def extraire_entreprises_suisses(code_html):
    print("Extraction des données par BeautifulSoup")
    
    # 1. On donne le code HTML brut à BeautifulSoup pour qu'il l'analyse
    soup = BeautifulSoup(code_html, 'html.parser')
    
    # Liste vide pour stocker nos résultats propres
    liste_entreprises = []
    
    # 2. On demande à BeautifulSoup de trouver tous les titres de résultats (balises h3)
    titres_resultats = soup.find_all('h3')
    
    # 3. On fait une boucle pour examiner chaque titre trouvé un par un
    for element in titres_resultats:
        texte_complet = element.get_text()
        
        # Nettoyage cosmétique : On enlève le suffixe " - LinkedIn" ou " | LinkedIn" 
        nom_propre = texte_complet.replace(" | LinkedIn", "").replace(" - LinkedIn", "")
        
        # On ajoute le nom propre dans notre liste finale
        liste_entreprises.append(nom_propre)
        
    return liste_entreprises