# Copyright 2020 Jacques Berger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class Poursuite:
    def __init__(self, id, id_etablsmnt, nom_etablsmnt, proprietaire, adresse, ville, statut, date_poursuite, date_jugement, motif, montant, nbr_infraction):
        self.id = id
        self.id_etablsmnt = id_etablsmnt
        self.nom_etablsmnt = nom_etablsmnt
        self.proprietaire = proprietaire
        self.adresse = adresse
        self.ville = ville
        self.statut = statut
        self.date_poursuite = date_poursuite
        self.date_jugement = date_jugement
        self.motif = motif
        self.montant = montant
        self.nbr_infraction_etablsmnt = nbr_infraction


    def asDictionary(self):
        return {"id": self.id,
                "id_etablsmnt": self.id_etablsmnt,
                "nom_etablsmnt": self.nom_etablsmnt,
                "proprietaire": self.proprietaire,
                "adresse": self.adresse,
                "ville": self.ville,
                "statut": self.statut,
                "date_poursuite": self.date_poursuite,
                "date_jugement": self.date_jugement,
                "motif": self.motif,
                "montant": self.montant}
    
    def asDictionaryNbr(self):
        return{
            "nom": self.nom_etablsmnt,
            "nombre" : self.nbr_infraction_etablsmnt
        }