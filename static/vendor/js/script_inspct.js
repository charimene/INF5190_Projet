function validerDate(date){
    if(date.match(/^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$/g)){
        return true;
    }else{
        return false;
    }
};

function verifier_chaine_caractere(chaine){
    if(chaine.match(/^[\w\s,.'éèàç]*$/g)){
        return true;
    }else{
        return false;
    }
};
    
function entree_valides(nom_etablsmn, adresse, ville, date_visite_client, nom_client, prenom_client, plainte){
    valide = false;
    if(verifier_chaine_caractere(nom_etablsmn) && verifier_chaine_caractere(adresse) && 
        verifier_chaine_caractere(ville) && verifier_chaine_caractere(nom_client) &&
        verifier_chaine_caractere(prenom_client) && verifier_chaine_caractere(plainte) 
        && validerDate(date_visite_client)){

        valide = true;
        
    }
    return valide;
};

// fonction pour soumettre formulaire d'ajout d'inspection 
document.getElementById("form_add_inspection").addEventListener("submit", function(event) {
    event.preventDefault();

    // l'endroit ou on affiche le resultat
    var resultat = document.getElementById("resultat");
    var erreur = document.getElementById("erreur");
    var confirme = document.getElementById("succes");

    var nom_etablsmn = document.getElementById("nom_etablsmn").value;
    var adresse = document.getElementById("adresse").value;
    var ville = document.getElementById("ville").value;
    var date_visite_client = document.getElementById("date_visite_client").value;
    var nom_client = document.getElementById("nom_client").value;
    var prenom_client = document.getElementById("prenom_client").value;
    var plainte = document.getElementById("plainte").value;

    // on valide les données entrées par l'utilisateur.
    if(entree_valides(nom_etablsmn, adresse, ville, date_visite_client, nom_client, prenom_client, plainte)){
        const xhr = new XMLHttpRequest();
        var donnee_json;
        const url = "/inspection"; // l'URL a retourner
        xhr.open('POST', url, true); 
        xhr.setRequestHeader('Content-Type', 'application/json'); 
        var parametres = {nom_etablissement:nom_etablsmn,
            adresse: adresse,
            ville: ville,
            date_visite_client:date_visite_client,
            nom_client:nom_client,
            prenom_client:prenom_client,
            plainte :plainte};
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) { // verifie si la requete est terminee
                if (xhr.status === 201) { // verifie si la requête a reussi
                    donnee_json = xhr.responseText; // resultaat de la requete
                    //resultat.innerHTML="";
                    confirme.innerText = "Votre demande a bien été ajoutée!";
                    resultat.innerText = donnee_json;   
                } else {
                    erreur.innerText = "Un problème est survenu au niveau du serveur";
                }
            }
        };
        xhr.send(JSON.stringify(parametres));
    }else{
        erreur.innerText = "Données sont pas valides !";
    }
});

