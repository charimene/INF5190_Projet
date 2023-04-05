
// fonction pour soumettre formulaire de modification d'un etablissement.
document.getElementById("form_edit_etablsmn").addEventListener("submit", function(event) {
    event.preventDefault();

    // l'endroit ou on affiche le resultat
    // var resultat = document.getElementById("resultat");
    var erreur = document.getElementById("erreur");
    var confirme = document.getElementById("resultat");

    var id = document.getElementById("id").value;
    var nom_etablsmn = document.getElementById("nom_etablsmn").value;
    var adresse = document.getElementById("adresse").value;
    var ville = document.getElementById("ville").value;
    var proprietaire = document.getElementById("propietaire").value;
    var statut = document.getElementById("statut").value;
    // var nbr = document.getElementById("nbr_infraction").value;

    // on valide les données entrées par l'utilisateur.
    // if(entree_valides(nom_etablsmn, adresse, ville, proprietaire, statut) && !isNaN(nbr)){
        const xhr = new XMLHttpRequest();
        // var donnee_json;
        //console.log("+++++++++++"+id+"_"+"nom="+nom_etablsmn);
        url = "/contrevenant/"+ id;// l'URL a retourner
        //url2 = encodeURIComponent(url);
        xhr.open('PUT', url, true); 
        xhr.setRequestHeader('Content-Type', 'application/json'); 
        var parametres = {nom_etablsmnt:nom_etablsmn,
            proprietaire:proprietaire,
            adresse: adresse,
            ville: ville,
            statut:statut};
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) { // verifie si la requete est terminee
                if (xhr.status === 200) { // verifie si la requête a reussi
                    //donnee_json = xhr.responseText; // resultaat de la requete
                    //resultat.innerHTML="";
                    confirme.innerText = "Votre modification a bien été effectuée!";
                    //resultat.innerText = donnee_json;   
                } else {
                    erreur.innerText = "Un problème est survenu au niveau du serveur qui empeche la modification voulue";
                }
            }
        };
        xhr.send(JSON.stringify(parametres));
    // }else{
        // erreur.innerText = "Données ne sont pas valides !";
    // }
});

// function modifierEtablissement(id){
//     xhr = new XMLHttpRequest();
//     var erreur = document.getElementById("erreur");
//     var section_res = document.getElementById("section_resultat");
//     const url = "/contrevenant/"+ id; // l'URL a retourner
//     xhr.open('PUT', url, true); 
//     xhr.setRequestHeader('Content-Type', 'application/json'); 

//         xhr.onreadystatechange = function() {
//             if (xhr.readyState === XMLHttpRequest.DONE) { // verifie si la requete est terminee
//                 if (xhr.status === 200) { // verifie si la requête a reussi
//                     // donnee_json = xhr.responseText; // resultaat de la requete
//                     section_res.innerText = "L'opération de suppression s'est déroulée avec succès.";
                    
//                 } else {
//                     erreur.innerHTML = "Un problème est survenu au niveau du serveur qui a empecher la supression! veuillez reessayer!";
//                 }
//             }
//         };
//         xhr.send();
// };


