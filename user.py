class User:

    def __init__(self, id, nom, prenom, courriel,
                 etablissement_a_surveiller, salt, mdp_hash):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.courriel = courriel
        self.etablissement_a_surveiller = etablissement_a_surveiller
        self.salt = salt
        self.mdp_hash = mdp_hash

    def asDictionary(self):
        return {"nom": self.nom,
                "prenom": self.prenom,
                "courriel": self.courriel,
                "etablissement_a_surveiller": self.etablissement_a_surveiller,
                "salt": self.salt,
                "mdp_hash": self.mdp_hash}
