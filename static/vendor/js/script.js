function validerDate(date){
    if(date.match(/^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$/g)){
        return true;
    }else{
        return false;
    }
}


function nbr_occurence(json_donnees, id_etablissement){
    const donnees = JSON.parse(json_donnees);
    var nbr =0;
    for (var i = 0; i < donnees.length; i++) {
        if (donnees[i].id_etablsmnt === id_etablissement) {
            nbr++;
        }
      }
    return nbr; 
}


function calculer_nbr_occurences(json_donnees){
    var resultat_dictionnaire = {}; // un dictionnaire qui contient pour chaque id etablissemtnn son nom et le nbr de fois qu'il apparait dans les resultats
    var donnees = JSON.parse(json_donnees);
    var nouveau ={};
    // print(json_donnees.length)
    for (var i = 0; i < donnees.length; i++) {
        id_etablissement = donnees[i].id_etablsmnt;
        nbr = nbr_occurence(json_donnees, id_etablissement);
        donnees[i].nbr = nbr // on ajoute l'attribut nbr dans nos données json qui contient le nbr d'occurence pour chaque etablissemnt de la liste des resultats.
    }
    return JSON.stringify(donnees);
}

// fonction qui affiche les donnees dans un tableau html 
function afficherEnTableau(donneesAvecNbr){
    var contrevenants = JSON.parse(donneesAvecNbr);

    espace_resultat = document.getElementById('section_resultat');
    
    var tableau = document.createElement('table'); // creation d'une balise table
    var entete = document.createElement('thead'); // creation de la baslise thead (balise enfant de table)
    tableau.appendChild(entete);

    var enteteTab = entete.insertRow();
    var colonneNom = enteteTab.insertCell();
    var colonneNbr = enteteTab.insertCell();
    colonneNom.textContent = "Nom de l'établissement";
    colonneNbr.textContent = 'Nombre de poursuites';

    var corps = document.createElement('tbody'); // creation de la baslise tbody (balise enfant de table)
    tableau.appendChild(corps);

    for (var i = 0; i < contrevenants.length; i++) {
        nom = contrevenants[i].nom_etablsmnt;
        nbr = contrevenants[i].nbr;

        ligne = corps.insertRow();
        ligne_nom = ligne.insertCell();
        ligne_nbr = ligne.insertCell();

        ligne_nom.textContent = nom;
        ligne_nbr.textContent = nbr;
    }
    espace_resultat.appendChild(tableau);
}

document.getElementById("recherche_dates").addEventListener("submit", function(event) {
    event.preventDefault();

    var section_res = document.getElementById("section_resultat");

    var du = document.getElementById("date_du").value;
    var au = document.getElementById("date_au").value;
    var date_du_valide = validerDate(du)
    var date_au_valide = validerDate(au)

    var erreur = document.getElementById("erreur");

    if ((au === "")  ||  (du === "")) {
        section_res.innerHTML = "";
        erreur.innerHTML = "date début et date de fin sont requises !";
    }else if(!date_du_valide ||  !date_au_valide){
        section_res.innerHTML = "";
        erreur.innerHTML = "Il faut saisir des dates correctes sous format YYYY-MM-JJ !";
    }else{
        const xhr = new XMLHttpRequest();
        var donnee_json;
        const url = "/contrevenants?du=" + du + "&au=" + au; // l'URL a retourner
        xhr.open('GET', url, true); 
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); 

        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) { // verifie si la requete est terminee
                if (xhr.status === 200) { // verifie si la requête a reussi
                    donnee_json = xhr.responseText; // resultaat de la requete
                    donneesAvecNbr= calculer_nbr_occurences(donnee_json);
                    afficherEnTableau(donneesAvecNbr);
                    // section_res.innerHTML = donneesAvecNbr;
                    
                } else {
                    erreur.innerHTML = "Un problème est survenu au niveau du serveur";
                }
            }
        };
        xhr.send();
    }
  });
