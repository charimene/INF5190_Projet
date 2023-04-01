# Interface de l'application Web
- Un sidebar qui comporte les petits formulaires qui servent a chercher des contrevenants (fonctionnalitées A2 et A5)
- Le résultat des recherches sera affichés dans le corps de la page en question. 

# Fonctionnalités developpées:
## A1
les fonctionnalitées de A1 sont executées lors de l'appel de la route principale de l'application "/".
- L'application fait telecharger les données a partir de l'url dans un doc CSV.
- Ensuite, le document CSV va etre converti en document XML et qui va etre valider par le validator valider.xsd.
- Lecture apartir du fichier XML et extraction de donnees de chaque poursuite et les inserer dans les 2 tables qui constituent la base de données.
- Apres je vais modifier l'attribut "nbr_infraction_etablsmnt" de chaque entree pour sauvegarder le nbr de poursuite lié a l'établissement en question.

## A2
Cette fonctionnalité sert a chercher des contravenants selon:
- le nom de leurs établissements. 
- le nom de leurs propriétaires.
- la rue de leurs établissements(adresse).
L'interface permet de choisir la préférence de l'utilisateur (recherche par Nom est placée par defaut).
## A4
Cette fonctionnalité offre un service REST qui permet de faire un GET pour avoir les poursuites qui ont été faites entre deux dates spécidiées dans les parametres de l'URL.
Exemple :
        GET /contrevenants?du=2020-05-08&au=2022-05-15

- Pour cette fonctionnalité, je cherche les poursuites qui ont "date_poursuite" entre les dates données dans l'url.

## A5
Cette fonctionnalité offre un formulaire qui permet l'introduction de 2 dates (date debut et date fin) entre lesquelles l'application cherches tous les contrevenants qui ont eu des poursuites dans cette période la. (le résultat s'affiche au bout de 2 à 3 sec si je cherche une période entre 2020 et 2023)

- Si on soumet le formulaire sans introduire de dates, un message d'erreur sera affichée.
- Si on soumet des données qui ne sont pas de dates (avec le format YYYY-MM-AA), une erreur sera affichée.

-Le submit de ce formulaire de recherche permet de renvoyer les resultats de recherche "Nom de l'établissement avec le nombre de son appartition dans les resultats" sur la meme page courante dans un tableau.

** Si on fait la recherhce apartir de la page d'accueil, les resultats s'afficheront dans la corps vide de la page. par contre si on lance une recherche apartir de la page resultat qui contient déja des resultats d'une autre recherche, les nouveaux resultats de recherche pas date viendront s'ajouter en bas de la page. (j'ai pas voulu nettoyer la page avant d'afficher mes nouveaux resultat juste pour montrer le travail qui se fait de la requete asynchrone et que la page courante s'actualise pas.)

## A6
Cette fonctionnalité permeet la recherche des poursuites apartir d'une liste prédeterminée de noms d'établissement (le 3e formulaire "Recherche par nom" dans la sidebar), elle permeet a l'utilisateur de choisir un nom d'établissement et d'afficher toutes les poursuites qui ont touché cet etablissement.
cette fonctionnalité appelle une requete Ajax asynchrne pour retourner le resultat.
Précision: 
        - la majorité des nom d'établissement contiennent des espaces vides entre les mots et des caracteres spéciaux comme &, #, / qui ont une interpretation bien spéciale dans une URL.
        Donc, dans mon traitement et lorsque je recupere le nom de mon établissement et a l'aide de la fonction : encodeURIComponent, les caracteres spéciaux seront remplacés par le code ASCII ce qui permet une imterpretation correcte du nom de l'établissement.

Exemple :
1- Dans l'application YARC, les espaces vides seront automatiquement remplacés par %20 :
C'est à dire l'url : http://127.0.0.1:5000/poursuites?nom=restaurant fiore
est equivalente à l'url : http://127.0.0.1:5000/poursuites?nom=restaurant%20fiore

2- Dans l'application YARC, les caracteres spéciaux sont pas interprétés automatiquement comme des chaines de caracteres faisant partie du nom de l'établissement :
par exemple avec l'url : http://127.0.0.1:5000/poursuites?nom=A & W     
ca ne retourne pas ce qu'on attendrait mais si on remplace le caractere & par son code ascii comme ceci :
        http://127.0.0.1:5000/poursuites?nom=A %26 W
ca va nous retourner les poursuites qu'on voudrait avoir.

* un autre exemple avec le caractere "#" dans le nom ""BUFFALO BILL #6"":
        http://127.0.0.1:5000/poursuites?nom=BUFFALO%20BILL%20%236

* Un autre exemple avec le caractere "/" pour le nom : "CAFE NAPOLITAN / BAR SHENANIGANS"
        http://127.0.0.1:5000/poursuites?nom=CAFE%20NAPOLITAN%20%2F%20BAR%20SHENANIGANS

3- Juste pour précision : tous ces traitements se font automatiqument en javascript quand on lance une recherche par nom, c'est a dire tous les caracteres spéciaux vont etre interpretés correctement avec du javascript.


# C1
ici je fais seulement une requete sql qui me retourne les etablissements avec les attributs : nom_etablsmnt et nbr_infraction_etablsmnt
et j'applique ORDER BY nbr_infraction_etablsmnt a ma requetes pour trier mes resultats selon le nombre des poursuites.
et je fais GROUP BY nom_etablsmnt pour eviter les doublons.
Exemple de route pour tester cette fonctionnalité sur YARC:
        http://127.0.0.1:5000/nbr_infractions_etablissements

# C2
Pour cette fonctionnalité, j'utilise la meme fonction utilisée dans C1 pour retourner la liste des établissements avec le nombre de poursuites qu'ils ont eu.
et la liste que je recois en json je la convertis en XML avec xml.etree.ElementTree .
Exemple de route pour tester cette fonctionnalité sur YARC:
        http://127.0.0.1:5000/nbr_infractions_etablissements_xml

# C3
Pour cette fonctionnalité, j'utilise la meme fonction utilisée dans C1 pour retourner la liste des établissements avec le nombre de poursuites qu'ils ont eu.
et la liste que je recois en json je la convertis en CSV avec la bibliotheque CSV .

Exemple de route pour tester cette fonctionnalité sur YARC:
        http://127.0.0.1:5000/nbr_infractions_etablissements_csv

# D1