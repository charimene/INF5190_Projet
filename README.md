# INF5190_Projet

Par Imene Charifi - CHAI18608701


J'ai téléchargé une template HTML gratuite que j'ai modifiée pour les fins du TP1.

Lien du téléchargement du template HTML : 
https://themewagon.com/themes/free-bootstrap-4-html5-news-website-template-newsbox/

Licence du template téléchargé : https://themewagon.com/license/


# Installation 

- Pour l’installer RAML :
    npm i -g raml2html

- installation de la db apartir du dossier db/:
    sqlite3 poursuites.db < db.sql 
    
- Pour générer le document doc.html pour la documentation du service REST, depuis la racine du proojet executer la commande suivante:
    raml2html doc.raml > templates/doc.html

- Compilation et execution : 
    FLASK_APP=index.py flask run

# Remarque

- Apres compilation : FLASK_APP=index.py flask run
le chargement du fichier et la conversion et la creation de la db prennent environ 32 sec.
Apres ca, la navigation se fait normalement.


# Fonctionnalités developpées :

- A1 (10XP)
- A2 (10Xp)
- A4 (10Xp)
- A5 (10Xp)
- A6 (10Xp)
- C1 (10Xp)
- C2 (5 Xp)
- C3 (5 Xp)
- D1 (15Xp)
- D2 (5Xp)
- D3 (15Xp)
- E1 (15Xp)

Pour un Total de : 120 XP

Le détail des fonctionnalités developpées se trouve dans le fichier 'correction.md'