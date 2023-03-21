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
## A4
Cette fonctionnalité offre un service REST qui permet de faire un GET pour avoir les poursuites qui ont été faites entre deux dates spécidiées dans les parametres de l'URL.
Exemple :
        GET /contrevenants?du=2020-05-08&au=2022-05-15

- Pour cette fonctionnalité, je cherche les poursuites qui ont "date_poursuite" entre les dates données dans l'url.