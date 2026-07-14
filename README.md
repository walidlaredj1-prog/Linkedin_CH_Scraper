# 🇨🇭 LinkedIn Switzerland Company Scraper

Un outil d'automatisation et de web scraping robuste développé en Python. Il combine la puissance de **Playwright** pour simuler une navigation humaine sur Google Suisse et **BeautifulSoup** pour extraire et nettoyer proprement les noms des entreprises de services informatiques actives en Suisse.

Les résultats récoltés sont automatiquement nettoyés et exportés dans un fichier Excel exploitable.

---

## ✨ Fonctionnalités

- 🌐 **Navigation automatisée** : Recherche ciblée sur Google Suisse avec des opérateurs spécifiques (`site:ch.linkedin.com/company "solution IT"`).
- 🛡️ **Anti-Fingerprinting basique** : Utilisation d'un User-Agent réaliste et de paramètres de masquage pour éviter d'être détecté comme un robot.
- 🧩 **Résolution semi-manuelle de CAPTCHA** : En cas de détection par Google, le script se met en pause intelligente et te laisse le temps de résoudre le reCAPTCHA à la souris directement dans le navigateur.
- 🧹 **Parsing & Nettoyage** : Extraction ciblée des titres de pages LinkedIn et filtrage du bruit avec BeautifulSoup.
- 📊 **Export Excel** : Génération automatique d'un tableau propre au format `.xlsx` grâce à Pandas.

---

## 📂 Structure du projet

```text
Linkedin_CH_Scraper/
├── src/
│   ├── scraper.py       # Script principal (automatisation, détection captcha, extraction & export)
├── .gitignore           # Fichiers à exclure de la sauvegarde Git (venv, caches, fichiers Excel)
├── README.md            # Ce fichier explicatif
└── entreprises_suisses.xlsx  # Fichier Excel généré (créé après exécution)
