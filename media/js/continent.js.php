/** only continent
 * 010808-153932
 */ 
$(document).ready(function(){
    // * Continent 
    //moteur de recherche assist�e 'Continent' : affiche par default le 'A'
    $(this).artistes_par_lettre('<?=$_GET["id"];?>', 'A');
});
