from flask import Flask
from flask import render_template
from flask import g
from flask import redirect
from flask import request
import hashlib
import uuid
from database import Database
from datetime import datetime, date
import re
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError
import json
import urllib.request


app = Flask(__name__, static_url_path="", static_folder="static")
schema = JsonSchema(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({'error': e.message, 'errors': errors}), 400


@app.route('/doc')
def documentation():
    return render_template('doc.html')


# La fonction verifier_chaine_caractere verifie si la chaine de
# caractere passée en parametre est une chaine alphanumérique avec des
# apostrophes, des lettres à accents, et le signe ":"
# j'interdis tous les caracteres spéciaux et la ponctuation
def verifier_chaine_caractere(chaine):
    expression_valide = r"^[\w\s\-\':]+$"
    regex = re.compile(expression_valide)
    if regex.match(chaine) is not None:
        resultat = True
    else:
        resultat = False

    return resultat


# La fonction verifier_date verifie si la chaine passee en parametre est
# une date correcte selon le format aaaa-mm-jj
def verifier_format_date(chaine):
    expression_valide = r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
    regex = re.compile(expression_valide)
    if regex.match(chaine) is not None:
        resultat = True
    else:
        resultat = False

    return resultat


# La fonction verifier_date verifie si la chaine passee en parametre
# est une date actuelle ou future
def verifier_date(chaine):
    date_obj = datetime.strptime(chaine, "%Y-%m-%d")
    date = date_obj.date()
    date_systeme = date.today()
    if (date < date_systeme):
        resultat = False
    else:
        resultat = True
    return resultat


# La fonction verifier_texte_article verifie si l'article ne
# depasse pas les 500 caracteres
def verifier_texte_article(article):
    if (len(article) > 500):
        resultat = False
    else:
        resultat = True
    return resultat


# La fonction verifier_date verifie si la chaine passee en parametre
# est une date du jour ou d'avant
def verifier_date_si_actuelle_ou_passee(chaine):
    date_obj = datetime.strptime(chaine, "%Y-%m-%d")
    date = date_obj.date()
    date_systeme = date.today()
    if (date > date_systeme):
        resultat = False
    else:
        resultat = True
    return resultat


# La fonction prend en paramètres une liste d'articles et parcourt
# cette dernière pour ne retourner que les articles qui ont été
# publiés à la date du jour ou avant.
def get_article_jour(articles):
    liste_article = []
    for article in articles:
        if verifier_date_si_actuelle_ou_passee(article["date"]):
            liste_article.append(article)
        if len(liste_article) == 5:
            break
    return liste_article


def telecharger_donnees():
    url = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

    requete = urllib.request.urlopen(url)
    donnees_csv = requete.read()

    encodage_csv = donnees_csv.decode('utf-8')

    fichier_csv = open("donnees/donnees.csv", "w", encoding="utf-8")
    fichier_csv.write(encodage_csv)
    fichier_csv.close()


@app.route('/', methods=['GET'])
def page_accueil():
    doc_xml = telecharger_donnees()
    return render_template('accueil.html')

