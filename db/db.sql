create table poursuite(
  id integer primary key,
  id_etablsmnt integer,
  nom_etablsmnt varchar(200),
  proprietaire varchar(200),
  adresse varchar(300),
  ville varchar(100),
  statut varchar(100),
  date_poursuite text,
  date_jugement text,
  motif varchar(500),
  montant float,
  nbr_infraction_etablsmnt integer
);

create table inspection(
  id integer primary key,
  nom_etablissement varchar(200),
  adresse varchar(300),
  ville varchar(100),
  date_visite_client text,
  nom_client varchar(50),
  prenom_client varchar(50),
  plainte varchar(500)
);