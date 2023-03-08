create table etablissement (
  id integer primary key,
  nom varchar(200),
  proprietaire varchar(200),
  adresse varchar(300),
  ville varchar(100),
  statut varchar(100)
);

create table poursuite (
  id integer primary key,
  date_poursuite text,
  date_jugement text,
  motif varchar(500),
  montant float,
  id_etablsmnt integer,
  foreign key (id_etablsmnt) references etablissement(id)
);

