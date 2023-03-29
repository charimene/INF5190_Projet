# INF5190_Projet

Par Imene Charifi - CHAI18608701


J'ai téléchargé une template HTML gratuite que j'ai modifiée pour les fins du TP1.

Lien du téléchargement du template HTML : 
https://themewagon.com/themes/free-bootstrap-4-html5-news-website-template-newsbox/

Licence du template téléchargé : https://themewagon.com/license/


# Installation 

Pour l’installer RAML :
    npm i -g raml2html

- installation de la db:
    sqlite3 poursuites.db < db.sql 
    
Pour générer le document doc.html pour la documentation du service REST, depuis la racine du proojet executer la commande suivante:
    raml2html doc.raml > templates/doc.html


    Apres compilation : FLASK_APP=index.py flask run
    le chargement du fichier et la conversion et la creation de la db prennent environ 32 sec 
    Apres la navigation se fait normalement.
