// --------------------
function validerDate(date){
    if(date.match(/^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$/g)){
        return true;
    }else{
        return false;
    }
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
    } else if(!date_du_valide ||  !date_au_valide){
        section_res.innerHTML = "";
        erreur.innerHTML = "Il faut saisir des dates correctes sous format YYYY-MM-JJ !";

    }else{
        const xhr = new XMLHttpRequest();
        // l'URL a retourner
        const url = "/contrevenants?du=" + du + "&au=" + au;
        xhr.open('GET', url, true); 
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); 

        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) { // Vérifie si la requête est terminée
                if (xhr.status === 200) { // Vérifie si la requête a réussi
                    section_res.innerHTML = xhr.responseText;
                } else {
                    erreur.innerHTML = "Un problème est survenu au niveau du serveur";
                }
            }
            };
            xhr.send();
    }
  });
