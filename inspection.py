class Inspection:
    def __init__(self, id, nom_etablissement, adresse,
                 ville, date_visite_client, nom_client,
                 prenom_client, plainte):
        self.id = id
        self.nom_etablissement = nom_etablissement
        self.adresse = adresse
        self.ville = ville
        self.date_visite_client = date_visite_client
        self.nom_client = nom_client
        self.prenom_client = prenom_client
        self.plainte = plainte

    def asDictionary(self):
        return {"id": self.id,
                "nom_etablissement": self.nom_etablissement,
                "adresse": self.adresse,
                "ville": self.ville,
                "date_visite_client": self.date_visite_client,
                "nom_client": self.nom_client,
                "prenom_client": self.prenom_client,
                "plainte": self.plainte}
