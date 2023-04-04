from flask import Flask
from flask import render_template
from flask import g
from flask import redirect
from flask import request
from flask import jsonify
import hashlib
import uuid
from database import Database
from datetime import datetime, date, timedelta
import re
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError
from schemas import demande_inspection_schema
# from .schemas import person_update_schema
import json
import io
import urllib.request
from urllib.request import Request, urlopen
import csv
import xml.etree.ElementTree as et
from poursuite import Poursuite
from inspection import Inspection


app = Flask(__name__, static_url_path="", static_folder="static")
schema = JsonSchema(app)


# Le bout de code de la fonction construire_db() qui s'execute une seule fois au debut de
# démarrage de l'application    
@app.before_first_request
def construire_db():
    telecharger_donnees()
    convertir_csv2xml()
    inserer_donnees_db()
    nbr_poursuite_etablissement()


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


def noms_etablissements():
    etablissements = get_db().get_etablissements()
    return etablissements


@app.route('/doc')
def documentation():
    return render_template('doc.html')


# La fonction verifier_chaine_caractere verifie si la chaine de
# caractere passée en parametre est une chaine alphanumérique avec des
# apostrophes, des lettres à accents, et le signe ":"
# j'interdis tous les caracteres spéciaux et la ponctuation
def verifier_chaine_caractere(chaine):
    expression_valide = r"^[\w\s\-\':().#$&+/]+$"
    regex = re.compile(expression_valide)
    if regex.match(chaine) is not None:
        resultat = True
    else:
        resultat = False

    return resultat



def telecharger_donnees():
    url = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

    #J'ai ajoute l'agent Mozilla pour eviter l'erreur urllib.error.httperror : erreur http 403
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    donnees_csv = urlopen(request_site).read()

    # requete = urllib.request.urlopen(url)  
    # donnees_csv = requete.read()

    encodage_csv = donnees_csv.decode('utf-8')

    fichier_csv = open("donnees/donnees.csv", "w", encoding="utf-8")
    fichier_csv.write(encodage_csv)
    fichier_csv.close()


def convertir_csv2xml():
    fichier_csv = open("donnees/donnees.csv", newline='')
    lignes = csv.DictReader(fichier_csv)
    # racine du fichier par la balise library qui sert a valider le fichier xml créé par le fichier
    # xsd : valider.xsd
    racine_fichier = et.Element("library")
    racine_fichier.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")   
    racine_fichier.set("xsi:noNamespaceSchemaLocation", "valider.xsd")

    poursuites = et.SubElement(racine_fichier, "poursuites")
    for ligne in lignes:
        poursuite = et.SubElement(poursuites, "poursuite")
        for cle_balise, val in ligne.items():
            champ = et.SubElement(poursuite, cle_balise)
            champ.text = val

    fichier_xml = et.ElementTree(racine_fichier)
    fichier_xml.write("donnees/donnees.xml", encoding="UTF-8", xml_declaration=True)


# cette fonction teste si l'id de la poursuite passé en parametre existe deja dans notre DB
# Si l'id de la poursuite existe dans notre DB, la fonction retourne True, sinon ca retourne false
def poursuite_existe(id_poursuite):
    resultat = False
    poursuite = get_db().get_poursuite(id_poursuite)
    if poursuite is not None:
        resultat = True
    return resultat


def inserer_donnees_db():
    fichier_xml = et.parse("donnees/donnees.xml")
    racine = fichier_xml.getroot()
    poursuites = racine[0]
    for i in poursuites.findall("poursuite"):
        id_etablismnt=i.find("business_id").text
        nom = i.find("etablissement").text
        proprietaire = i.find("proprietaire").text
        adresse = i.find("adresse").text
        ville = i.find("ville").text
        statut = i.find("statut").text
        
        id_poursuite=i.find("id_poursuite").text
        date_poursuite = i.find("date").text
        date_jugement = i.find("date_jugement").text
        motif=i.find("description").text
        montant = i.find("montant").text
        nbr_infraction = 1
        
        # on vient ajouter le meme établissement qu'une seule fois dans la table etblissement de base de donnees
        # il existe surement plusieurs poursuites associées au meme établissement.
        # if not etablsmnt_existe(id_etablismnt):
        #     etablissement = Etablissement(id_etablismnt, nom, proprietaire, adresse, ville, statut)
        #     etablssmnt_db = get_db().save_etablissmnt(etablissement)

        if not poursuite_existe(id_poursuite):
            poursuite = Poursuite(id_poursuite, id_etablismnt, nom, proprietaire, adresse, ville, 
                                  statut, date_poursuite, date_jugement, motif, montant, nbr_infraction)
            poursuite_db = get_db().save_poursuite(poursuite)


# fonction qui va compter le nombre de poursuite a chaque établissement et le met a jour dans la base de donnees.
def nbr_poursuite_etablissement():
    liste_poursuites = get_db().get_poursuites()
    for p in liste_poursuites:
        id_etablissement = p.id_etablsmnt
        nbr_infraction = get_db().get_nbr_poursuite(id_etablissement)
        get_db().update_nbr_poursuite(id_etablissement, nbr_infraction)


@app.route('/', methods=['GET'])
def page_accueil():
    # variable qui contient les noms des établissemnts qui ont fait l'objet de poursuites.
    etablissements_liste = noms_etablissements()
    return render_template('accueil.html', etablissements_liste=etablissements_liste), 200
    #nbr = get_db().nbr_poursuite()
    # return render_template('accueil.html'), 200


@app.route('/recherche', methods=['POST'])
def donnees_recherche():
    mot_cle = request.form['nl-search']
    filtre = request.form['options']

    if mot_cle == "":
        return render_template("resultats.html",
                               error="Le champ de recherche est "
                               "obligatoire"), 400
    # elif (not verifier_chaine_caractere(mot_cle)):
    #     return render_template("resultats.html",
    #                            error="Les motifs de recherche "
    #                            "doivent être des chaines de "
    #                            "caracteres alphanumériques"), 400
    elif (filtre == "nom"):
        contravenants = get_db().search_contravenant_par_nom(mot_cle)
        return render_template('resultats.html', resultats=contravenants), 200
    elif (filtre == "proprietaire"):
        contravenants = get_db().search_contravenant_par_proprietaire(mot_cle)
        return render_template('resultats.html', resultats=contravenants), 200
    elif (filtre == "rue"):
        contravenants = get_db().search_contravenant_par_rue(mot_cle)
        return render_template('resultats.html', resultats=contravenants), 200
    

@app.route('/contrevenants', methods=["GET"])
def get_contrevenants():
    contrevenants_liste=[]
    # récuperer les dates passées en parametres
    date_du = request.args.get('du')
    date_au = request.args.get('au')

    # normaliser les dates recues en parametres selon leur format en DB
    # on eneleve les - 
    date_du = date_du.replace('-', "")
    date_au = date_au.replace('-', "")
    # convertir les dates en chaine de caracteres en type date pour pouvoir les comparer
    datedu = datetime.strptime(date_du, '%Y%m%d')
    dateau = datetime.strptime(date_au, "%Y%m%d")
    date_du_parametre = datedu.date()
    date_au_parametre = dateau.date()

    # contrevenants = get_db().get_poursuites()
    contrevenants = get_db().get_poursuites()
    for c in contrevenants:
        # recuperer la date de la poursuite  
        date_poursuite = c.date_poursuite

        # converitr la date de la poursuite en type date
        datec = datetime.strptime(date_poursuite, "%Y%m%d")
        date_c = datec.date()
        
        # comparer les dates et ajouter celle qui est entre les 2 dates passées en parmetres
        if date_c >= date_du_parametre and date_c <= date_au_parametre:
            contrevenants_liste.append(c)

    if len(contrevenants_liste) == 0:
        return "", 404
    else:
        return jsonify([contrevenant.asDictionary() for contrevenant in contrevenants_liste])


@app.route('/poursuites', methods=["GET"])
def get_poursuites():
    contrevenants_liste=[]
    # récuperer le nom passé en parametres
    nom_etablissement = request.args.get('nom')

    # valider l'argument passé en parametre
    if(verifier_chaine_caractere(nom_etablissement)):
        poursuites = get_db().get_poursuites_etablissement(nom_etablissement)
        if poursuites is None:
            return "", 404
        else:
            return jsonify([poursuite.asDictionary() for poursuite in poursuites]), 200


@app.route('/nbr_infractions_etablissements', methods=['GET'])
def get_liste_etablissements():
    etablissements = get_db().get_etablissements_par_nbr()
    if etablissements is None:
        return "", 404
    else:
        return jsonify([eta.asDictionaryNbr() for eta in etablissements])
        

@app.route('/nbr_infractions_etablissements_xml', methods=['GET'])
def get_liste_etablissements_xml():
    etablissements = get_liste_etablissements() 
    if(etablissements is None):
        return "", 404
    else:
        json_data = etablissements.json

        racine = et.Element('etablissements')

        for item in json_data:
            etablissement = et.SubElement(racine, "etablissement")
            nbr_balise = et.SubElement(etablissement, "nombre")
            nbr_balise.text = str(item['nombre'])
            nom_balise = et.SubElement(etablissement, "nom")
            nom_balise.text = str(item["nom"])

        etablissements_xml = et.tostring(racine, encoding='UTF-8', xml_declaration=True)
        
        return etablissements_xml, 200
    
@app.route('/nbr_infractions_etablissements_csv', methods=['GET'])
def get_liste_etablissements_csv():
    etablissements = get_liste_etablissements() 
    if(etablissements is None):
        return "", 404
    else:
        json_data = etablissements.json

        etablissements_csv = io.StringIO()
        csv_ecriture = csv.writer(etablissements_csv)

        csv_ecriture.writerow(["Nombre", "Nom"])

        for item in json_data:
            csv_ecriture.writerow([item['nombre'], item['nom']])
        
        etablissements_csv_str = etablissements_csv.getvalue()
        return etablissements_csv_str, 200

@app.route('/inspection', methods=["POST"])
@schema.validate(demande_inspection_schema)
def create_inspection():
    donnees = request.get_json()
    inspection = Inspection(None, donnees["nom_etablissement"], donnees["adresse"], donnees["ville"], donnees["date_visite_client"], donnees["nom_client"], donnees["prenom_client"], donnees["plainte"])
    inspection = get_db().save_inspection(inspection)
    return jsonify(inspection.asDictionary()), 201


@app.route('/demande_inspection', methods=["GET","POST"])
def demande_inspection():
    return render_template("ajout_inspection.html")
    

@app.route('/inspections', methods=["GET"])
def get_inspections():
    inspections = get_db().get_inspections()
    return jsonify([inspection.asDictionary() for inspection in inspections])


@app.route('/inspection/<id>', methods=["DELETE"])
def supprimer_inspection(id):
    inspection = get_db().get_inspection(id)
    if inspection is None:
        return "", 404
    else:
        get_db().delete_inspection(id)
        return "", 200