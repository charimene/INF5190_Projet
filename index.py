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


app = Flask(__name__, static_url_path="", static_folder="static")


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


@app.route('/', methods=['GET'])
def page_accueil():
    date_now = date.today()
    articles = get_db().get_cinq_articles()
    articles_date_jour = get_article_jour(articles)
    return render_template('accueil.html', articles=articles_date_jour), 200


@app.route('/admin', methods=['GET'])
def page_admin():
    articles = get_db().get_articles()
    return render_template('admin.html', articles=articles), 200


@app.route('/admin-nouveau', methods=['GET'])
def page_nouveau_article():
    return render_template('ajout_article.html'), 200


@app.route('/envoyer', methods=['POST'])
def donnees_formulaire():
    titre = request.form['titre']
    auteur = request.form['auteur']
    date = request.form['date_publication']
    texte_article = request.form['article']
    identifiant = request.form['id_article']
    print(identifiant)

    donnees_entrees = {}
    donnees_entrees["titre"] = titre
    donnees_entrees["auteur"] = auteur
    donnees_entrees["date"] = date
    donnees_entrees["paragraphe"] = texte_article
    donnees_entrees["identifiant"] = identifiant

    if (titre == "" or auteur == "" or date == "" or texte_article == ""
       or identifiant == ""):
        return render_template("ajout_article.html",
                               error="Tous les champs sont obligatoires"), 400
    elif (not verifier_chaine_caractere(titre)):
        return render_template("ajout_article.html",
                               donnees_entrees=donnees_entrees,
                               error="Le titre de l'article "
                               "doit etre des chaines de "
                               "caracteres alphanumériques"), 400
    elif (not verifier_chaine_caractere(auteur)):
        return render_template("ajout_article.html",
                               donnees_entrees=donnees_entrees,
                               error="L'auteur de l'article "
                               "doit etre des chaines de "
                               "caracteres alphanumériques"), 400
    elif (not verifier_format_date(date)):
        return render_template("ajout_article.html",
                               donnees_entrees=donnees_entrees,
                               error="La date doit etre sous "
                               "le format suivant : aaaa-mm-jj"), 400
    elif (not verifier_chaine_caractere(identifiant)):
        return render_template("ajout_article.html",
                               donnees_entrees=donnees_entrees,
                               error="L'identifiant de l'article "
                               "doit etre des chaines de "
                               "caracteres alphanumériques"), 400
    elif (not verifier_date(date)):
        return render_template("ajout_article.html",
                               donnees_entrees=donnees_entrees,
                               error="La date doit etre celle "
                               "d'aujourd'hui ou du future"), 400
    elif (not verifier_texte_article(texte_article)):
        return render_template("ajout_article.html",
                               donnees_entrees=donnees_entrees,
                               error="Le contenu de l'article ne doit "
                               "pas dépasser un paragraphe (pas plus "
                               "de 500 caracteres)"), 400
    else:
        get_db().insert_article(titre, auteur, identifiant, date,
                                texte_article)
        return redirect('/confirmation')


@app.route('/article/<identifiant>', methods=['GET'])
def article(identifiant):
    article = get_db().get_article(identifiant)
    if article is None:
        return redirect('/erreur'), 404
    else:
        return render_template('article.html', article=article), 200


@app.route('/modifier-article/<identifiant>', methods=['GET', 'POST'])
def page_modification_article(identifiant):
    article = get_db().get_article(identifiant)

    if request.method == "GET":
        if article is None:
            return redirect('/erreur'), 404
        else:
            return render_template("modif_article.html", article=article), 200
    else:
        titre = request.form["titre"]
        paragraphe = request.form["article"]

        if titre == "" or paragraphe == "":
            return render_template("modif_article.html", article=article,
                                   error="Tous les champs sont "
                                   "obligatoires"), 400
        elif (not verifier_chaine_caractere(titre)):
            return render_template("modif_article.html", article=article,
                                   error="Le titre de l'article doit etre "
                                   "des chaines de caracteres "
                                   "alphanumériques"), 400
        elif (not verifier_texte_article(paragraphe)):
            return render_template("modif_article.html", article=article,
                                   error="Le contenu de l'article ne doit "
                                   "pas dépasser un paragraphe "
                                   "(pas plus de 500 caracteres)"), 400
        else:
            get_db().maj_article(identifiant, titre, paragraphe)
            return redirect('/confirmation')


@app.route('/confirmation')
def confirmer():
    return render_template('confirmation.html')


@app.route('/erreur')
def erreur():
    return render_template('404.html'), 404


@app.route('/recherche', methods=['POST'])
def donnees_recherche():
    mot_cle = request.form['nl-search']
    if mot_cle == "":
        return render_template("articles.html",
                               error="Le champ de recherche est "
                               "obligatoire"), 400
    elif (not verifier_chaine_caractere(mot_cle)):
        return render_template("articles.html",
                               error="Les motifs de recherche "
                               "doivent être des chaines de "
                               "caracteres alphanumériques"), 400
    else:
        articles = get_db().search_articles(mot_cle)
        return render_template('articles.html', articles=articles), 200
