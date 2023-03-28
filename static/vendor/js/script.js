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

    var corps = document.createElement('tbody'); // creation de la balise tbody (balise enfant de table)
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

// fonction qui fait une requete AJAx pour chercher les contrevenants entre 2 dates
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


// fonction qui fait une requete AJAx (A6) pour chercher les contrevenants par noms d'établissements
document.getElementById("recherche_nom").addEventListener("submit", function(event) {
    event.preventDefault();

    var section_res = document.getElementById("section_resultat");
    var erreur = document.getElementById("erreur");

    var option_choisi = document.getElementById('recherche_etablsmnt').value;

    if (option_choisi === ""){
        section_res.innerHTML = "";
        erreur.innerHTML = "Nom d'établissement est requise !";
    }else{ 
        // faire encodeURIComponent pour ne pas interpreter certains caracteres speciaux comme
        // des séparateurs d'url comme le & et /
        option_choisie = encodeURIComponent(option_choisi);
        const xhr = new XMLHttpRequest();
        var donnee_json;
        const url = "/poursuites?nom=" + option_choisie; // l'URL a retourner
        xhr.open('GET', url, true); 
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); 

        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) { // verifie si la requete est terminee
                if (xhr.status === 200) { // verifie si la requête a reussi
                    donnee_json = xhr.responseText; // resultaat de la requete
                    // donneesAvecNbr= calculer_nbr_occurences(donnee_json);
                    section_res.innerHTML = "";
                    afficherPoursuitesEnHTML(donnee_json);
                    //section_res.innerHTML = donnee_json;
                    
                } else {
                    erreur.innerHTML = "Un problème est survenu au niveau du serveur";
                }
            }
        };
        xhr.send();
    }
  });


// fonction qui affiche les resultats des poursuites dans une page HTML.
function afficherPoursuitesEnHTML(donnee_json){
    var poursuites = JSON.parse(donnee_json);

    espace_resultat = document.getElementById('section_resultat');
    

    for (var i = 0; i < poursuites.length; i++) {
        id_poursuite = poursuites[i].id;
        nom_etablissement = poursuites[i].nom_etablsmnt;
        id_etablissement = poursuites[i].id_etablsmnt;
        proprietaire = poursuites[i].proprietaire;
        adresse = poursuites[i].adresse;
        ville = poursuites[i].ville;
        statut = poursuites[i].statut;
        date_poursuite = poursuites[i].date_poursuite;
        date_jugement = poursuites[i].date_jugement;
        description = poursuites[i].motif;
        montant = poursuites[i].montant;


        // ici je renprends le html de la page resultat.
        var div = document.createElement('div'); // <div class="col-12 col-sm-12 cadre">
        div.setAttribute('class', 'col-12 col-sm-12 cadre');

        var sous_div = document.createElement('div'); // <div class="single-blog-post d-flex style-4 mb-30">
        sous_div.setAttribute('class', 'single-blog-post d-flex style-4 mb-30');

        var sous_div2 = document.createElement('div'); // <div class="blog-content">
        sous_div2.setAttribute('class', 'blog-content');

        div.appendChild(sous_div);
        sous_div.appendChild(sous_div2);


        // Pour chaque ligne on crée le span suivant : <span class="post-date">
        var span0 = document.createElement('span'); 
        span0.setAttribute('class', 'post-date');
        span0.innerHTML = "<strong>Nom de l'établissement: </strong>"+nom_etablissement +"<br>";
        sous_div2.appendChild(span0);

        var span1 = document.createElement('span'); 
        span1.setAttribute('class', 'post-date');
        span1.innerHTML = "<strong>Id poursuite: </strong>"+id_poursuite +"<br>";
        sous_div2.appendChild(span1);

        var span2 = document.createElement('span'); 
        span2.setAttribute('class', 'post-date');
        span2.innerHTML = "<strong>Id établissement: </strong>"+id_etablissement+"<br>";
        sous_div2.appendChild(span2);

        var span3 = document.createElement('span'); 
        span3.setAttribute('class', 'post-date');
        span3.innerHTML = "<strong>Propriétaire:</strong> "+proprietaire+"<br>";
        sous_div2.appendChild(span3);

        var span4 = document.createElement('span'); 
        span4.setAttribute('class', 'post-date');
        span4.innerHTML = "<strong>Adresse: </strong>"+adresse+"<br>";
        sous_div2.appendChild(span4);

        var span5 = document.createElement('span'); 
        span5.setAttribute('class', 'post-date');
        span5.innerHTML = "<strong>Ville: </strong>"+ville+"<br>";
        sous_div2.appendChild(span5);

        var span6 = document.createElement('span'); 
        span6.setAttribute('class', 'post-date');
        span6.innerHTML = "<strong>Statut: </strong>"+statut+"<br>";
        sous_div2.appendChild(span6);

        var span7 = document.createElement('span'); 
        span7.setAttribute('class', 'post-date');
        span7.innerHTML = "<strong>Date de poursuite:</strong> "+date_poursuite+"<br>";
        sous_div2.appendChild(span7);

        var span8 = document.createElement('span'); 
        span8.setAttribute('class', 'post-date');
        span8.innerHTML = "<strong>Date de jugement: </strong>"+date_jugement+"<br>";
        sous_div2.appendChild(span8);

        var span9 = document.createElement('span'); 
        span9.setAttribute('class', 'post-date');
        span9.innerHTML ="<strong>Description: </strong>"+description+"<br>";
        sous_div2.appendChild(span9);

        var span10 = document.createElement('span'); 
        span10.setAttribute('class', 'post-date');
        span10.innerHTML ="<strong>Montant: </strong>"+montant+"<br>";
        sous_div2.appendChild(span10);

        espace_resultat.appendChild(div);
    }
    
}