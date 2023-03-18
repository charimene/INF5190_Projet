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
Dans la conception de la base de données, j'ai 2 tables, une pour les établissements, une pour les poursuites, c'est pourquoi si je fais entrer un motif de recherche je recois une seule fois le nom du'un contrevenants qui lui associé a une ou plusieurs poursuites.
## A3

## A4