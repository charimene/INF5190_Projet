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
from inspection import Inspection
import json

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
        cursor.execute("select id, id_etablsmnt, nom_etablsmnt, proprietaire, adresse, ville, statut, date_poursuite, date_jugement, motif, montant, nbr_infraction_etablsmnt from poursuite where id = ?", (id_poursuite,))
        poursuite = cursor.fetchone()
        if poursuite is None:
            return None
        else:
            return Poursuite(poursuite[0], poursuite[1], poursuite[2], poursuite[3], poursuite[4], poursuite[5], poursuite[6], poursuite[7], poursuite[8], poursuite[9], poursuite[10], poursuite[11])
        

    def save_poursuite(self, poursuite):
        connection = self.get_connection()
        connection.execute("insert into poursuite(id, id_etablsmnt, nom_etablsmnt, proprietaire, adresse, ville, statut, date_poursuite, date_jugement, motif, montant, nbr_infraction_etablsmnt) "
                               "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (poursuite.id, poursuite.id_etablsmnt, poursuite.nom_etablsmnt, poursuite.proprietaire,
                                poursuite.adresse, poursuite.ville, poursuite.statut, 
                                poursuite.date_poursuite, poursuite.date_jugement, poursuite.motif, poursuite.montant, poursuite.nbr_infraction_etablsmnt))
        connection.commit()


    def get_poursuites(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, id_etablsmnt, nom_etablsmnt, proprietaire,"
                       "adresse, ville, statut, date_poursuite, date_jugement,"
                       "motif, montant, nbr_infraction_etablsmnt from poursuite ")
        poursuites = cursor.fetchall()
        return [Poursuite(poursuite[0], poursuite[1], poursuite[2],
                       poursuite[3], poursuite[4], poursuite[5], 
                       poursuite[6], poursuite[7], poursuite[8],
                       poursuite[9], poursuite[10], poursuite[11]) for poursuite in poursuites]
   

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
        cursor.execute("select distinct nom_etablsmnt from poursuite order by nom_etablsmnt")
        etablissements = cursor.fetchall()
        return [{"nom": etablsmnt[0]} for etablsmnt in etablissements]
    

    #fonction qui retourne les poursuite d'un etablissement donné
    def get_poursuites_etablissement(self, nom_etablissement):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, id_etablsmnt, nom_etablsmnt, proprietaire,"
                       "adresse, ville, statut, date_poursuite, date_jugement,"
                       "motif, montant, nbr_infraction_etablsmnt from poursuite where lower(nom_etablsmnt) = lower(?) ",(nom_etablissement,))
        poursuites = cursor.fetchall()
        return [Poursuite(poursuite[0], poursuite[1], poursuite[2],
                       poursuite[3], poursuite[4], poursuite[5], 
                       poursuite[6], poursuite[7], poursuite[8],
                       poursuite[9], poursuite[10], poursuite[11]) for poursuite in poursuites]


    def get_nbr_poursuite(self, id_etablissement):
        cursor = self.get_connection().cursor()
        cursor.execute("select count(*) from poursuite where id_etablsmnt = ?",(id_etablissement,))
        nbr = cursor.fetchone()
        return nbr[0]
    

    def update_nbr_poursuite(self, id_etablissement, nbr_poursuite):
        connection = self.get_connection()
        connection.execute("update poursuite set nbr_infraction_etablsmnt = ? where nbr_infraction_etablsmnt = 1 and id_etablsmnt = ? ",(nbr_poursuite, id_etablissement))
        connection.commit()
    
    
    def get_etablissements_par_nbr(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select distinct * from poursuite group by nom_etablsmnt order by nbr_infraction_etablsmnt desc")
        etablissements = cursor.fetchall()
        return [Poursuite(eta[0], eta[1], eta[2],
                       eta[3], eta[4], eta[5], 
                       eta[6], eta[7], eta[8],
                       eta[9], eta[10], eta[11]) for eta in etablissements]
        # return [{"nom": etablsmnt[0], "nbr": etablsmnt[1]} for etablsmnt in etablissements]


    def save_inspection(self, inspection):
        connection = self.get_connection()
        connection.execute("insert into inspection(nom_etablissement, adresse, ville, date_visite_client, nom_client, prenom_client, plainte) "
                            "values(?, ?, ?, ?, ?, ?, ?)",
                            (inspection.nom_etablissement, inspection.adresse, inspection.ville, inspection.date_visite_client,inspection.nom_client, inspection.prenom_client, inspection.plainte))
        connection.commit()
        return inspection


    def get_inspections(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from inspection")
        inspections = cursor.fetchall()
        return [Inspection(inspection[0], inspection[1], inspection[2],
                       inspection[3], inspection[4], inspection[5],
                       inspection[6], inspection[7]) for inspection in inspections]


    def get_inspection(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from inspection where id = ?", (id,))
        inspection = cursor.fetchone()
        if inspection is None:
            return None
        else:
            return Inspection(inspection[0], inspection[1], inspection[2], inspection[3], inspection[4], inspection[5], inspection[6], inspection[7])
        
    def delete_inspection(self, id):
        connection = self.get_connection()
        connection.execute("delete from inspection where id = ?", (id,))
        connection.commit()


    def get_inspections_dun_etablissement(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from poursuite where id_etablsmnt = ?", (id,))
        poursuites = cursor.fetchall()
        return [Poursuite(p[0], p[1], p[2],
                       p[3], p[4], p[5], 
                       p[6], p[7], p[8],
                       p[9], p[10], p[11]) for p in poursuites]
    

    def delete_etablissement(self, id):
        #la suppression d'un etablissement quelcoque revient a supprimer toutes les poursuites qui 
        #comme reference l'etablissement en question.
        connection = self.get_connection()
        connection.execute("delete from poursuite where id_etablsmnt = ?", (id,))
        connection.commit()