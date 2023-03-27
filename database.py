# Copyright 2017 Jacques Berger
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


import sqlite3
from datetime import datetime, date
from poursuite import Poursuite

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/poursuites.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None


    def get_poursuite(self, id_poursuite):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, id_etablsmnt, nom_etablsmnt, proprietaire, adresse, ville, statut, date_poursuite, date_jugement, motif, montant from poursuite where id = ?", (id_poursuite,))
        poursuite = cursor.fetchone()
        if poursuite is None:
            return None
        else:
            return Poursuite(poursuite[0], poursuite[1], poursuite[2], poursuite[3], poursuite[4], poursuite[5], poursuite[6], poursuite[7], poursuite[8], poursuite[9], poursuite[10])
        

    def save_poursuite(self, poursuite):
        connection = self.get_connection()
        connection.execute("insert into poursuite(id, id_etablsmnt, nom_etablsmnt, proprietaire, adresse, ville, statut, date_poursuite, date_jugement, motif, montant) "
                               "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (poursuite.id, poursuite.id_etablsmnt, poursuite.nom_etablsmnt, poursuite.proprietaire,
                                poursuite.adresse, poursuite.ville, poursuite.statut, 
                                poursuite.date_poursuite, poursuite.date_jugement, poursuite.motif, poursuite.montant))
        connection.commit()


    def get_poursuites(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, id_etablsmnt, nom_etablsmnt, proprietaire,"
                       "adresse, ville, statut, date_poursuite, date_jugement,"
                       "motif, montant from poursuite ")
        poursuites = cursor.fetchall()
        return [Poursuite(poursuite[0], poursuite[1], poursuite[2],
                       poursuite[3], poursuite[4], poursuite[5], 
                       poursuite[6], poursuite[7], poursuite[8],
                       poursuite[9], poursuite[10]) for poursuite in poursuites]
   

    def search_contravenant_par_proprietaire(self, mot_cle):
        motif_recherche = "%"+str(mot_cle)+"%"
        cursor = self.get_connection().cursor()
        cursor.execute("select * from poursuite where proprietaire like ?",(motif_recherche,))
        resultats = cursor.fetchall()
        return [{"id_p": res[0], "id_e": res[1], "nom_e": res[2],
                 "proprietaire": res[3], "adresse": res[4],
                 "ville": res[5], "statut": res[6], "date_p": res[7],
                 "date_jug": res[8], "motif": res[9],
                 "montant": res[10]} for res in resultats]
    

    def search_contravenant_par_nom(self, mot_cle):
        motif_recherche = "%"+str(mot_cle)+"%"
        cursor = self.get_connection().cursor()
        cursor.execute("select * from poursuite where nom_etablsmnt like ?",(motif_recherche,))
        resultats = cursor.fetchall()
        return [{"id_p": res[0], "id_e": res[1], "nom_e": res[2],
                 "proprietaire": res[3], "adresse": res[4],
                 "ville": res[5], "statut": res[6], "date_p": res[7],
                 "date_jug": res[8], "motif": res[9],
                 "montant": res[10]} for res in resultats]
    

    def search_contravenant_par_rue(self, mot_cle):
        motif_recherche = "%"+str(mot_cle)+"%"
        cursor = self.get_connection().cursor()
        cursor.execute("select * from poursuite where adresse like ?",(motif_recherche,))
        resultats = cursor.fetchall()
        return [{"id_p": res[0], "id_e": res[1], "nom_e": res[2],
                 "proprietaire": res[3], "adresse": res[4],
                 "ville": res[5], "statut": res[6], "date_p": res[7],
                 "date_jug": res[8], "motif": res[9],
                 "montant": res[10]} for res in resultats]
    

    def get_etablissements(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select distinct nom_etablsmnt from poursuite")
        etablissements = cursor.fetchall()
        return [{"nom": etablsmnt[0]} for etablsmnt in etablissements]
    

    #fonction qui retourne les poursuite d'un etablissement donné
    def get_poursuites_etablissement(self, nom_etablissement):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, id_etablsmnt, nom_etablsmnt, proprietaire,"
                       "adresse, ville, statut, date_poursuite, date_jugement,"
                       "motif, montant from poursuite where lower(nom_etablsmnt) = lower(?) ",(nom_etablissement,))
        poursuites = cursor.fetchall()
        return [Poursuite(poursuite[0], poursuite[1], poursuite[2],
                       poursuite[3], poursuite[4], poursuite[5], 
                       poursuite[6], poursuite[7], poursuite[8],
                       poursuite[9], poursuite[10]) for poursuite in poursuites]

