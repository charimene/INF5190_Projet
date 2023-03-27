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
# from etablissement import Etablissement
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

    # ok
    def get_poursuite(self, id_poursuite):
        cursor = self.get_connection().cursor()
        cursor.execute("select id, id_etablsmnt, nom_etablsmnt, proprietaire, adresse, ville, statut, date_poursuite, date_jugement, motif, montant from poursuite where id = ?", (id_poursuite,))
        poursuite = cursor.fetchone()
        if poursuite is None:
            return None
        else:
            return Poursuite(poursuite[0], poursuite[1], poursuite[2], poursuite[3], poursuite[4], poursuite[5], poursuite[6], poursuite[7], poursuite[8], poursuite[9], poursuite[10])
            # return {"id": poursuite[0], "date_poursuite": poursuite[1],
            #         "date_jugement": poursuite[2], "motif": poursuite[3],
            #         "montant": poursuite[4], "id_etablsmnt": poursuite[5]}
        

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
    # [{"id": poursuite[0], "date_poursuite": poursuite[1],
    #              "date_jugement": poursuite[2], "motif": poursuite[3],
    #              "montant": poursuite[4], "id_etablsmnt": poursuite[5]} for poursuite in poursuites]
    

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
    
        # [Etablissement(eta[0], eta[1], eta[2],
        #                eta[3], eta[4], eta[5]) for eta in etablissements]
    
            # [{"id": etablsmnt[0], "nom": etablsmnt[1],
            #      "proprietaire": etablsmnt[2], "adresse": etablsmnt[3],
            #      "ville": etablsmnt[4], "statut": etablsmnt[5]} for etablsmnt in etablissements]
        



    # def get_poursuites_etablismnt(self):
    #     cursor = self.get_connection().cursor()
    #     cursor.execute("select * from etablissement, poursuite where etablissement.id = poursuite.id_etablsmnt")
    #     resultats = cursor.fetchall()
    #     return [{"id_e": res[0], "nom_e": res[1],
    #              "proprietaire": res[2], "adresse": res[3],
    #              "ville": res[4], "statut": res[5], "id_p": res[6], "date_p": res[7],
    #              "date_jug": res[8], "motif": res[9],
    #              "montant": res[10]} for res in resultats]

    # def get_contrevenant(self, id_contrevenant):
    #     cursor = self.get_connection().cursor()
    #     cursor.execute("select * from contrevenant "
    #                    "where id = ?", (id_contrevenant,))
    #     etablissement = cursor.fetchone()
    #     if etablissement is None:
    #         return None
    #     else: #a fixer
    #         return Etablissement(etablissement[0], etablissement[1], etablissement[2],
    #                    etablissement[3], etablissement[4], etablissement[5])
    #         # return {"id": etablissement[0], "nom": etablissement[1],
    #         #         "proprietaire": etablissement[2], "adresse": etablissement[3],
    #         #         "ville": etablissement[4], "statut": etablissement[5]}


    
    # def save_etablissmnt(self, etablissement):
    #     connection = self.get_connection()
    #     connection.execute("insert into contrevenant(id, nom, proprietaire, adresse, ville, statut) "
    #                            "values(?, ?, ?, ?, ?, ?)",
    #                            (etablissement.id, etablissement.nom, etablissement.proprietaire,
    #                             etablissement.adresse, etablissement.ville, etablissement.statut))
    #     connection.commit()
    

    
    # def get_etablissements(self):
    #     cursor = self.get_connection().cursor()
    #     cursor.execute("select id, nom, proprietaire, "
    #                    "adresse, ville, statut from etablissement ")
    #     etablissements = cursor.fetchall()
    #     return [Etablissement(eta[0], eta[1], eta[2],
    #                    eta[3], eta[4], eta[5]) for eta in etablissements]
    
    #         # [{"id": etablsmnt[0], "nom": etablsmnt[1],
    #         #      "proprietaire": etablsmnt[2], "adresse": etablsmnt[3],
    #         #      "ville": etablsmnt[4], "statut": etablsmnt[5]} for etablsmnt in etablissements]
        

  
    

    # def nbr_poursuite(self):
    #     cursor = self.get_connection().cursor()
    #     nbr = cursor.execute("SELECT COUNT(*) FROM poursuite")
    #     print("dfsdgdd "+str(nbr))
    #     return nbr

    
    
    # def get_contrevenants(self, date_du, date_au):
    #     datedu = datetime.strptime(date_du, '%Y%m%d')
    #     dateau = datetime.strptime(date_au, '%Y%m%d')
    #     cursor = self.get_connection().cursor()
    #     cursor.execute("select * from etablissement, poursuite where etablissement.id = poursuite.id_etablsmnt",(motif_recherche,))
    #     resultats = cursor.fetchall()
    #     return [{"id_e": res[0], "nom_e": res[1],
    #              "proprietaire": res[2], "adresse": res[3],
    #              "ville": res[4], "statut": res[5], "id_p": res[6], "date_p": res[7],
    #              "date_jug": res[8], "motif": res[9],
    #              "montant": res[10]} for res in resultats]






























    def get_cinq_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select titre, identifiant, auteur, "
                       "date_publication, paragraphe from article "
                       "order by id desc")
        articles = cursor.fetchall()
        return [{"titre": article[0], "id": article[1],
                 "auteur": article[2], "date": article[3],
                 "article": article[4]} for article in articles]

    def insert_article(self, titre, auteur, identifiant,
                       date_publi, paragraphe):
        connection = self.get_connection()
        connection.execute(("insert into article (titre, identifiant, "
                            "auteur, date_publication, paragraphe) "
                            "values(?, ?, ?, ?, ?)"), (titre, identifiant,
                                                       auteur, date_publi,
                                                       paragraphe))
        connection.commit()

    
    def get_article(self, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute("select titre, identifiant, auteur, "
                       "date_publication, paragraphe from article "
                       "where identifiant = ?", (identifiant,))
        article = cursor.fetchone()
        if article is None:
            return None
        else:
            return {"titre": article[0], "id": article[1],
                    "auteur": article[2], "date": article[3],
                    "article": article[4]}
        

    def maj_article(self, identifiant, titre, paragraphe):
        connection = self.get_connection()
        connection.execute("update article set titre = ?, paragraphe =? "
                           "where identifiant = ?",
                           (titre, paragraphe, identifiant))
        connection.commit()

