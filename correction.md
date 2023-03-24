# Interface de l'application Web
- Un sidebar qui comporte les petits formulaires qui servent a chercher des contrevenants (fonctionnalitées A2 et A5)
- Le résultat des recherches sera affichés dans le corps de la page en question. 

# Fonctionnalités developpées:
## A1
les fonctionnalitées de A1 sont executées lors de l'appel de la route principale de l'application "/".
- L'application fait telecharger les données a partir de l'url dans un doc CSV.
- Ensuite, le document CSV va etre converti en document XML et qui va etre valider par le validator valider.xsd.
- Lecture apartir du fichier XML et extraction de donnees de chaque poursuite et les inserer dans les 2 tables qui constituent la base de données.
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
Cette fonctionnalité offre un formulaire qui permet l'introduction de 2 dates (date debut et date fin) entre lesquelles l'application cherches tous les contrevenants qui ont eu des poursuites dans cette période la.

- Si on soumet le formulaire sans introduire de dates, un message d'erreur sera affichée.
- Si on soumet des données qui ne sont pas de dates (avec le format YYYY-MM-AA), une erreur sera affichée.

-Le submit de ce formulaire de recherche permet de renvoyer les resultats de recherche en json qui seront recupérés soit par le YARC soit sur le corps de la page web.