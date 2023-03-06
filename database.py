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


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/articles.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select titre, identifiant, auteur, "
                       "date_publication, paragraphe from article "
                       "order by id desc")
        articles = cursor.fetchall()
        return [{"titre": article[0], "id": article[1],
                 "auteur": article[2], "date": article[3],
                 "article": article[4]} for article in articles]

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

    def search_articles(self, mot_cle):
        motif_recherche = "%"+str(mot_cle)+"%"
        cursor = self.get_connection().cursor()
        cursor.execute("select titre, identifiant, date_publication from "
                       "article where titre like ? or paragraphe like ?",
                       (motif_recherche, motif_recherche))
        articles = cursor.fetchall()
        return [{"titre": article[0], "id": article[1], "date": article[2]}
                for article in articles]
