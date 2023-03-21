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
  montant float
);