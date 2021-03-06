// Cart

// 
$(document).ready(function(){
  //dbg
  //$("#cart-itemz").show();
  
  
  $(".cart-album-list").hide();// cache par default tracklisting album
  
  $("#cont-panier").attr("title", "Cliquer pour afficher").css({cursor:"pointer"}).click(
  function(){
  
  if( $("#cart-itemz").is(":hidden")){
    $("#fleche-cart").attr("src", "../templates/img/fleche_down_cart.png").css("margin","3px 4px 0px 5px");
    $("#fleche-cart").attr("title", "Cliquer pour afficher"); 
    $("#cart-itemz").fadeIn("slow");  
  }else{
    $("#fleche-cart").attr("src", "../templates/img/fleche_cart_droite.png").css("margin","2px 8px 0px 5px");
    $("#fleche-cart").attr("title", "Cliquer pour cacher");   
    $("#cart-itemz").fadeOut("slow");
  }
    
  });


  
});//eo.$(document).ready()


  /****
   *
   *
   * 100209-185920
   */           
  function recup_olcart(){
    // post
    $.ajax({
    type: "POST",
    url: "./includes/ajax.lib.php",
    data: "p=jax_recup_olcart",
     success: function(xml){
     
     display_cart(xml);
     $("#panier_ol, #titre-olcart").remove();
     
     }//eo.success
    });//eo.post  
  
  
  }//eo.func

  /****
  * display *all* cart itemz for flash cart 
  */
  
  function cart_display_viafla(){
    // post
    $.ajax({
    type: "POST",
    url: "./includes/ajax.lib.php",
    data: "p=jax_cart_display_viafla",
     success: function(xml){
     
     display_cart(xml);
     
     }//eo.success
    });//eo.post
  
  
  }//eo.func



  /****
  * ADD in Cart and display *all* cart itemz   
  */
  function cart_add(p_id, p_type){
  //var o = $(this); 
   var o = $("#add_" + p_type + "_" + p_id);
   
  var trackId = p_id;     var objetType = p_type; 
  //alert(o.attr("id"));
  
    // post
    $.ajax({
    type: "POST",
    url: "./includes/ajax.lib.php",
    data: "p=jax_cart_add2&type="+ objetType +"&id=" + trackId,
     success: function(xml){
        
          ////
      if($(xml).read("msg")){
        var msg_err = "";

        if($(xml).read("err_tra_tra") != "0"){msg_err = "Doublon titre";}
        if($(xml).read("err_tra_alb") != "0"){msg_err = "Ce titre appartient � un album d�j� pr�sent dans votre panier";}//err_tra_alb
        if($(xml).read("err_alb_tra") != "0"){msg_err = "Cet album poss�de un titre d�j� pr�sent dans votre panier";}//err_alb_tra
        if($(xml).read("err_alb_alb") != "0"){msg_err = "Doublon Album";}
        var sp = document.createElement("p");$(sp).attr({"id":"msg-error" + p_id, "class":"err-msg-cart-add"});
        $(sp).html(""+ msg_err + "");
  
        //o.before($(sp).fadeIn(400));//affichage du msg
        $.facebox(msg_err);
        o.remove();// suppr du lien
      
      }else{
      ///
      // on affiche le cart
        display_cart(xml);
        
        $.facebox($.add2cart_confirmation); setTimeout("$(document).trigger('close.facebox');", 1600);//mod.070109-18286//030209-182937
          
          if(objetType == "2"){
          inhib_sc_album(p_id);
          tl_disabled(p_id);
          }else{//track
          inhib_a_track(p_id);
          }
        
      }//eo.if dbl
     }//eo.success
    });//eo.post
  
  
  }//eo.func
  
  /**
   * Display cart
   *
   */        
  function display_cart(p_xml_cart){
    var xml = p_xml_cart;
    var var_li = "";
    var nb_itemz = parseFloat($(xml).read("items_nb"));
    
   
    if(nb_itemz > 0){
      $(xml).find("item").each(function() { // 
        var_li += "<tr id=\"cartLi_"+$(this).read("cart_type")+"_"+$(this).read("cart_track_album_id")+"\">\n";
        var_li += "<td class=\"c-title\"><b>" + $(this).read("cart_title") + "</b> / "+ $(this).read("cart_artist_name") +"</td>\n";// titre + artiste name
        var_li += "<td class=\"c-type\">"+ $(this).read("cart_type_libele") +"</td>\n";
        var_li += "<td class=\"c-price\"><b><span id=\"checkout-prix-item_"+$(this).read("cart_type")+"_"+ $(this).read("cart_track_album_id") +"\">" + $(this).read('cart_prix') + "</span></b>\n";
        var_li += "<td class=\"c-suppr\"><input type=\"button\" onClick=\"delete_fc('"+$(this).read("cart_track_album_id")+"', '"+$(this).read("cart_type")+"', '"+$(this).read("cart_id")+"');\" class=\"cart-ico-suppr\" id=\""+$(this).read("cart_type")+"_"+$(this).read("cart_track_album_id")+"\" value=\"&nbsp;\" title=\""+$.cart_action_supprItem+"\" /></td>\n";
        var_li += "</tr>";
      });//loop
    }else{
      var_li += "<tr id=\"cart-id-empty\">\n";
      var_li += "<td class=\"c-title\">" + $.cart_empty + "</td>\n";// titre + artiste name
      var_li += "</tr>";
    }
      

      // suppr. msg par default s'il existe
      $("#cart-id-empty").remove();
      // nb item
      $('#cart-item-nb').html(nb_itemz);
      
      // amount
      $("#cart-total").html($(xml).read("items_total_amount"));
      
      // suppr. ce qu'il ya avant
      $("#panier tr, #cart-checkout-lien, #fc-content").remove();
      
      //ajoute le contenu xml
      $("#panier").append(var_li); 
      
      

      var fl_cart_bt_cko = "<div id=\"fc-content\">"
     // fl_cart_bt_cko += "<p class='pastille'>" + nb_itemz +  "</p>";
      fl_cart_bt_cko += "<div class='fc-cko'><a href=\"\" onClick=\"$('#cart-itemz').fadeIn('slow'); $('html,body').animate({scrollTop: '0px'}, 1000); return false;\">"+$.bt_flottant_libelle + "</a>";
      fl_cart_bt_cko += "</div>";
      fl_cart_bt_cko += "</div>";
      
      $("#float-cart").html(fl_cart_bt_cko);
      
      // affiche
      $("#cart-itemz").fadeIn("slow");
      
    // lien checkout si besoin

      if(nb_itemz == 0){
      $("#cart-checkout-lien").remove();
      $("#cart-itemz, #float-cart").fadeOut("slow");
      }
    
      if(nb_itemz > 0){
      var d = document.createElement("a"); $(d).attr("href","checkout.php");$(d).attr("id","cart-checkout-lien");
      $(d).html($.checkout_now); $(d).addClass("cart-checkout-lien");
       $("#panier").after(d);
      }
  }//eo.func


  /***
   * Checkout :: Suppr. an item � partir du checkout
   * 061008-121235   
   */         
  function delete_fcko(p_id, p_type, p_cartid){
  
  // post
  $.ajax({
  type: "POST",
  url: "./includes/ajax.lib.php",
  data: "p=jax_cart_suppr_an_item&type="+ p_type +"&id=" + p_id+"&value="+p_cartid,
    success: function(xml){   

    var var_li = "";
    var nb_itemz = parseFloat($(xml).read("items_nb"));
    // xml cart
    if(nb_itemz > 0){
      $(xml).find("item").each(function() { // TrackListing
        var_li += "<tr id=\"cartLi_"+$(this).read("cart_type")+"_"+$(this).read("cart_track_album_id")+"\" class=\"li-item\">\n";
        var_li += "<td class=\"c-title\"><b>" + $(this).read("cart_title") + "</b> / "+ $(this).read("cart_artist_name") +"</td>\n";// titre + artiste name
        var_li += "<td class=\"c-type\">"+ $(this).read("cart_type_libele") +"</td>\n";
        var_li += "<td class=\"c-price\"><b><span id=\"checkout-prix-item_"+$(this).read("cart_type")+"_"+ $(this).read("cart_track_album_id") +"\">" + $(this).read('cart_prix') + "</span></b>\n";
        var_li += "<td class=\"c-suppr\"><input type=\"button\" onClick=\"delete_fcko('"+$(this).read("cart_album_id")+"', '"+$(this).read("cart_type")+"', '"+$(this).read("cart_id")+"');\" class=\"cart-ico-suppr\" id=\""+$(this).read("cart_type")+"_"+$(this).read("cart_track_album_id")+"\" value=\"&nbsp;\"/></td>\n";
        var_li += "</tr>";
      });//loop
    }else{
      document.location.href = "/";
    }
    
    // efface le contenu du cart
    $("#panier .li-item").remove();
    // maj amount
    $("#cart-total-olcart").html($(xml).read("items_total_amount"));
    // maj nb item
    $("#cart-item-nb-olcart").html(nb_itemz);
      if(nb_itemz > 1){$("#item-item").html($.cart_item_pluriel);}else{$("#item-item").html($.cart_item);}
    
    // display itemz
    $("#panier").prepend(var_li);


    }//fct $$ success
  });//eo.ajax
  
  };//.delete_fcko()

    /***
     * Suppr. an item
     */         
    function delete_fc(p_id, p_type, p_cartid){

    // post
    $.ajax({
    type: "POST",
    url: "./includes/ajax.lib.php",
    data: "p=jax_cart_suppr_an_item&type="+ p_type +"&id=" + p_id +"&value="+p_cartid,
    success: function(xml){   
      
      // xml cart
      display_cart(xml);   
       
    // si la suppr. se fait au niveau du shortcut album, on reactive le bt add_track dans le TL

    if(p_type == "2"){
      // r�-activation du bt addalbum complet
      //$("#shortcut-add_" + p_id).css({"opacity":"1","color":"#000"}).attr("disabled",false);
      uninhib_sc_album(p_id);
      //reactive l'ensemble des bt "add_track" dans le TL
      tl_all_enabled(p_id);
      
    }else{
      uninhib_a_track(p_id);
    
      // suppr. bt suppr du TL
      //$("#tl-suppr_" + p_type + "_"  +  p_id).remove();
      //$("#add_" + p_type + "_"  + p_id).attr("disabled",false).removeClass("track_isbought").addClass("bt-cart-track");// tracklisting
      
    }//eo.if
  

     
      }//fct $$ success
    });//eo.ajax
      //------------------------- history
      // nb item -1
      //cart_calc_qtt("-");
      
      // total amount -1 item
      //$("#cart-total").html(cart_calc_total_amount(prix_item_o, "-"));
      
      // suppr. lien checkout si besoin
      //var nb_item = parseFloat($('#cart-item-nb').text());
     // var nb_itemz = $(xml).read("items_nb");
      //if(nb_itemz == 0 ){ $("#cart-checkout-lien").remove(); }
      
      //parentLi.css({"background":color,"color":"#fff"});
      // suppr. de l'item du cart
      //parentLi.remove();
    };//$.fn.delete
    


    /***
     * disab. ajout au track via le TL
     */         
    var tl_disabled = function(p_album_id){
      var tab_tl = $("#tab-tl_" + p_album_id);
        tab_tl.find(".bt-cart-track").each(function() {
        $(this).attr("disabled",true).removeClass("bt-cart-track").addClass("track_isbought");
        });
    
    }//eo.func


    /***
     * disab. ajout au track via le TL
     */         
    var tl_all_enabled = function(p_album_id){
      //alert(p_album_id);
      var tab_tl = $("#tab-tl_" + p_album_id);
        tab_tl.find(".track_isbought").each(function() {
        $(this).attr("disabled",false).removeClass("track_isbought").addClass("bt-cart-track");
        });
        
    }//eo.func


  function inhib_sc_album(p_id){
  $("#a_"+ p_id + "").find(".bt-alb-buy").removeClass("bt-alb-buy").addClass("alb-isbought").attr("onclick","").html($.alb_isbought);
  }
  function uninhib_sc_album(p_id){
  $("#a_"+ p_id + "").find(".alb-isbought").removeClass("alb-isbought").addClass("bt-alb-buy").attr("onclick","").html($.alb_2cart);
  }
  
  function inhib_a_track(p_id){
  $("#add_1_"  + p_id).attr("disabled",true).removeClass("bt-cart-track").addClass("track_isbought");
  //NB : appel post_cadi_datas() [ajax cadi data] obligatoire en cas de bouton genere via js
  //$("#add_1_"  + p_id).after("<input type=\"button\" jstag=\"track_delete_track-"+p_id+"\" onClick=\"delete_fc('"+p_id+"', '1');post_cadi_datas($(this).attr('jstag'));\" class=\"cart-ico-suppr\" id=\"tl-suppr_1_"+ p_id +"\" value=\"&nbsp;\" />");
  }  
            
  function uninhib_a_track(p_id){
  $("#add_1_"  + p_id).attr("disabled",false).removeClass("track_isbought").addClass("bt-cart-track");
  }     





    

    
    /***
     * Suppr. 1 item du tracklisting --depre
     */         
    $.fn.delete_from_tl = function(){
    
    var a = $(this); var id = a.attr("id"); 
    var itemid = id.replace(/tl-suppr_/,"");
    var prix_item_o = "#checkout-prix-item_" + itemid;
    
      // post
      $.ajax({
      type: "POST",
      url: "./includes/ajax.lib.php",
      data: "p=jax_cart_suppr_an_item&id=" + itemid,
      success: function(msg){
      
      var color; var var_li; 
        if(msg != 0){
        color = "green";
        
        // nb item -1
        cart_calc_qtt("-");
        
        // total amount -1 item
        $("#cart-total").html(cart_calc_total_amount(prix_item_o, "-"));
        
        // suppr. lien checkout si besoin
        var nb_item = parseFloat($('#cart-item-nb').text());
          if(nb_item == 0 ){ $("#cart-checkout-lien").remove(); }
          
        }else{
        color = "red";
        }
      
      // suppr. bt 'suppr' TL + activation du bt add
      a.prev("input").css({"opacity":"1","background":"url(./templates/img/ico_cart_mini.png) no-repeat 4px 0px"}).attr("disabled",false);
      a.remove();
      
      // suppr. item du cart
      $("#cartLi_" + itemid).remove();

      }//fct
      });//eo.ajax
    
    };//$.fn.delete_from_tl
    


    /**** QUANTITE ***/
    var cart_calc_qtt = function(p_ope){
      // nb items
      var cart_item_nb = $('#cart-item-nb'); var tot = parseFloat(cart_item_nb.text());
      // check si tot == vide
      tot = (isNaN(tot))?tot = 0:tot = tot; // DBG :alert(cart_item_nb.html() + " " +tot);

      // recup cart
      if(p_ope == "+"){
      cart_item_nb.html((tot + 1));
      }else{
      cart_item_nb.html((tot - 1));
      }
      //DBG :console.log("1/ cart_item_nb : "+cart_item_nb + " nb+1:" + (cart_item_nb +1) +"");

      //cart-item-pluriel
      tot = parseFloat($('#cart-item-nb').text());// refresh nb items
      if(tot > 1){ $("#jax-cart-item-pluriel").html("s");}else{$("#jax-cart-item-pluriel").html("");}
      
      if(isNaN(tot)){
      $('#cart-item-nb').html("aucun");// total == 0 -> nb item == 'aucun'
      // on cache le cart
      $("#cart-itemz").hide("slow");
      $(".cart-checkout-lien, .bt-submit-step").remove();
      
      }
    }
    

    /**** TOTAL **
     *input : id de l'input o� se trouve la chaine a calculer
     * ope : '+' ou '-' 
     * */
    var cart_calc_total_amount = function(p_input, p_ope){
      var prix_item;
      var cart_value = parseFloat($('#cart-total').text());// recup cart
      
        if(p_ope == "+"){
          if($(p_input).read("prix") == ""){
          prix_item = 0;
          }else{
          prix_item = parseFloat($(p_input).read("prix"));// prix de l'item (from xml)
          }
        return (Math.round((cart_value + prix_item)*100)/100);//prix
        
        }else{
          
        prix_item = parseFloat($(p_input).html());
        
      //alert(p_input +"-"+ $(p_input).attr("id") +"-" +prix_item + "--" + $("#checkout-prix-item_2_18313").html());
        
        
        var calcul = (Math.round((cart_value - prix_item)*100)/100);
          if(calcul != 0){
          return calcul;
          }else{
          return "0";// str '0'
          }
        }
    }
    /*********/
/***************************************************************/

  /***
  * Suppr. an item
  */         
  $.fn.delete_olcart = function(p_type,p_id){
    /* _/!\_ id == obj_type+_+obj_id+_+cart_itemid */
    var a = $(this); var itemid = a.attr("id");
    var parentLi = a.parents("tr");
    var cart_value = $("#cart-total-olcart").text();
    var itemidtype = itemid.replace(/del-oc/,"");
      var s = itemidtype.split("_");
      var itemid = s[1];
      var itemtype = s[0]; 
    //var prix_item = $("#prix-item-olcart" + itemtype+"_"+itemid).text();---depre $$ 150808-181217 $$ on passe par argument
    var prix_item = $("#prix-item-olcart" + p_type+"_"+p_id).text();

//alert("type" + itemtype + " id "+itemid + " prix :" + prix_item);
 /**/   
    // post
    $.ajax({
    type: "POST",
    url: "./includes/ajax.lib.php",
    data: "p=jax_cart_suppr_an_old_item&id=" + itemidtype,
    success: function(msg){   
      var color; var var_li; 
        if(msg != 0){
         color = "green";
          
        //// Calcul du nb d'item (-1)
        var cart_item_nb = $('#cart-item-nb-olcart'); var tot = parseFloat(cart_item_nb.text());
        // check si tot == vide
        tot = (isNaN(tot))?tot = 0:tot = tot; // DBG : alert(cart_item_nb.html() + " " +tot);
        //calc
        cart_item_nb.html((tot - 1));
        
        //cart-item-pluriel
        tot = parseFloat(cart_item_nb.text());// refresh nb items
        if(tot > 1){ $("#jax-cart-item-pluriel-olcart").html("s");}else{$("#jax-cart-item-pluriel-olcart").html("");}
        
        if(isNaN(tot)){
        cart_item_nb.html("aucun");// total == 0 -> nb item == 'aucun'
        }
        
        //// total amount -1 item
        var calcul = (Math.round((cart_value - prix_item)*100)/100);
          if(calcul != 0){calcul = calcul;}else{calcul = "0";}// str '0'
        $("#cart-total-olcart").html(calcul);
        
        //// suppr. visuelle de l'item de la liste des items
        parentLi.remove();

  
        }else{
        color = "red";
        }
     
      }//fct $$ success

    });//eo.ajax
    
  };//$.fn.delete_olcart  
  
  
  /***
    * recup a cart
  ***/         
  $.fn.olcart_2_newcart = function(){
    var a = $(this); var obj_itemid = a.attr("id");// id == obj_type+_+obj_id
    var parentLi = a.parents("tr");
    var item_id_type = obj_itemid.replace(/oc2nc/,"");
      var s = item_id_type.split("_");
      var itemid = s[1];
      var itemtype = s[0]; 
      
    a.delete_olcart(itemtype,itemid );// suppr de l'ancien cart
    a.cart_add(itemid, itemtype);// insert dans le nouveau
    
    //// suppr. visuelle de l'item de la liste des items
    parentLi.remove();

    };//$.fn.recup










    /****
    * ADD in Cart  --- old   
    */    
    $.fn.cart_add_old = function (p_id, p_type){
      var o = $(this);
     // o.parents('td').css({"background":"yellow"});
      var trackId = p_id;     var objetType = p_type; 

    // post
    $.ajax({
    type: "POST",
    url: "./includes/ajax.lib.php",
    data: "p=jax_cart_add&type="+ objetType +"&id=" + trackId,
    success: function(msg){
        
    var color; var var_li = ""; 
      
    if(msg != 0){// AJAX ok
    color = "green";

    // PROBL. DE DOUBLON
    if($(msg).read("msg")){
      var msg_err = "";
      // create a conteiner
      if($(msg).read("err_tra_tra") != "0"){msg_err = "Doublon titre";}
      if($(msg).read("err_tra_alb") != "0"){msg_err = "alert err_tra_alb";}
      if($(msg).read("err_alb_tra") != "0"){msg_err = "alert err_alb_tra";}
      if($(msg).read("err_alb_alb") != "0"){msg_err = "Doublon Album";}
      var sp = document.createElement("p");$(sp).attr({"id":"msg-error" + p_id, "class":"err-msg-cart-add"});
      $(sp).html(""+ msg_err + "");

      o.before($(sp).fadeIn(400));//affichage du msg
      o.remove();// suppr du lien
    
    }else{
    // affiche le cart
    $("#cart-itemz").fadeIn("slow");
    
    switch(objetType){
      case '1' :// track $$ $(msg).read('duration_mn')
      var_li += "<tr id=\"cartLi_"+objetType+"_"+$(msg).read("track track")+"\">";
      var_li += "<td class=\"c-title\"><b>" + $(msg).read("titre_track") + "</b> / artiste name";
      var_li += "<td class=\"c-type\">Titre</td>";
      var_li += "<td class=\"c-price\"><span id=\"checkout-prix-item_"+objetType+"_"+ $(msg).read("track track") +"\">" + $(msg).read('prix') + "</span></b>"+ $(msg).read("currency_symbol") +"";
      var_li += "<td class=\"c-suppr\"><input type=\"button\" onClick=\"$(this).delete_fc();\" class=\"cart-ico-suppr\" id=\""+objetType+"_"+$(msg).read("track track")+"\" value=\"&nbsp;\"/></td>";
      var_li += "</tr>";
      break;
      
      case '2':// album
      var_li += "<tr id\"cartLi_"+objetType+"|"+$(msg).read("album album")+"\">";
      var_li += "<b>" + $(msg).read("art_name") + "</b> - " +  "<span onClick=\"$('#panier-album_"+$(msg).read("album album")+"').toggle();\">" + $(msg).read("alb_title") + "</span>";
      var_li += " // <b>album</b> (" + $(msg).read("duree_totale_mn") + ") <b><span id=\"checkout-prix-item_"+objetType+"_"+$(msg).read("album album")+"\">"+$(msg).read("prix") + "</span>" + $(msg).read("currency_symbol");
      var_li += " <input type=\"button\" onClick=\"$(this).delete_fc();\" class=\"cart-ico-suppr\" id=\""+objetType+"_"+$(msg).read("album album")+"\" value=\"&nbsp;\" />";  
      //var_li += "  <img src='" + $(msg).read("images mini") + "'>";
      var_li += " <ul id=\"panier-album_"+$(msg).read("album album")+"\" class=\"cart-album-list\">";
        $(msg).find("track").each(function() { // TrackListing
        var_li += "<li>" + $(this).read("titre_track") + " " + $(this).read('duration_mn') + "</li>";
      });//loop
      var_li += " </ul>";
      var_li += "</tr>";
      break;
    }//eo.switch


    // suppr. msg par default s'il existe
    $("#cart-id-empty").remove();

    // qtt + total
    $("#cart-total").html(cart_calc_total_amount(msg, "+"));
    cart_calc_qtt("+");

    //ajoute l'item
     $("#panier").append(var_li);
    
    // lien checkout si besoin
    var nb_item = parseFloat($('#cart-item-nb').text());
      if(nb_item == 1 ){
      var d = document.createElement("a"); $(d).attr("href","checkout.php");$(d).attr("id","cart-checkout-lien");$(d).html("Terminer ma commande"); $(d).addClass("cart-checkout-lien");
       $("#panier").after(d);
      }

    // En cas d'ajout d'album, on cache par default le contenu de l'album
    $(".cart-album-list").hide();
    
    
    // au niveau du click
    // if(o.val() == "&nbsp;"){ ** tl-add_1|
      if(o.is("input")){
        // tab tl
        tl_disabled($(msg).read("album album"));
      
        //disab. butt
        o.attr("disabled",true);
        o.css({"color":"#fff","margin":"0 5px 0 0","opacity":"0.4"});
        if(p_type == "1"){//dans le cas du TL
               // o.remove();//
        o.after(" <img src=\"./templates/img/ico_famfam/tick.png\" /> <input type=\"button\" onClick=\"$(this).delete_from_tl();\" class=\"cart-ico-suppr\" id=\"tl-suppr_"+objetType+"_"+$(msg).read("track track")+"\" value=\"&nbsp;\" />");
        }      
      }else{
      o.css({"color":"#fff","background":"#000"}).html("item ajout�");
      }
    
    }//eo.if $$ doublon
    
    
    
    }else{
    //erreur
    color = "red";
    }


    }//eo.success
    });//eo.ajax

  
    }//eo.func $$ $.fn.cart_add






    /*
    --------------- HISTORY :: fct add ------------
    1.--
  
        if(p_action_type == "+"){
          if($(this).read("cart_type") == "2"){
          // inhib achat alb entier
          $("#a_"+$(this).read("cart_album_id") + "").find(".bt-alb-buy").toggleClass("alb-isbought").attr("onclick","").html("Album Achet�");
          tl_disabled($($(this)).read("cart_track_album_id:eq(0)"));// premier album ajout� au cart
          }else{
          var bt_add = "#add_"+ $(this).read("cart_type") + "_" + $(this).read("cart_track_album_id");
          $(bt_add).attr("disabled",true).toggleClass("track_isbought");
          
            if($(bt_add).is(":disabled")){
            }else{
            $(bt_add).after("<input type=\"button\" onClick=\"delete_from_tl();\" class=\"cart-ico-suppr\" id=\"tl-suppr_"+$(this).read("cart_type")+"_"+$(this).read("cart_track_album_id:eq(0)")+"\" value=\"&nbsp;\" />");
            }
      
        //disab. butt
        //o.attr("disabled",true);
        //o.css({"color":"#fff","margin":"0 5px 0 0"});
        //if(p_type == "1"){//dans le cas du TL
        //o.css({"background":"url(./templates/img/ico_famfam/tick.png) no-repeat 2px 0px"});
        //o.after("<input type=\"button\" onClick=\"$(this).delete_from_tl();\" class=\"cart-ico-suppr\" id=\"tl-suppr_"+objetType+"_"+$(xml).read("cart_track_album_id:eq(0)")+"\" value=\"&nbsp;\" />");
          }

          }
        }else{//suppr
        
        var p_type = $(this).read("cart_type"); //alert(p_type + "--" + $(this).read("cart_track_album_id"));
        if(p_type == "2"){
          // r�-activation du bt addalbum complet
          $("#shortcut-add_" + $(this).read("cart_track_album_id")).css({"opacity":"1","color":"#000"}).attr("disabled",false);
          //reactive l'ensemble des bt "add_track" dans le TL
          tl_all_enabled($(this).read("cart_track_album_id"));
        }else{
          // suppr. bt suppr du TL

          $("#tl-suppr_" + p_type + "_" + $(this).read("cart_track_album_id")).remove();
          $("#add_" + p_type + "_"  + $(this).read("cart_track_album_id")).toggleClass("bt-cart-track");// tracklisting

        }//eo.if
        
        
        }

    2.-----
    if(o.is("a.bt-alb-buy")){
        // tab tl
        alert(o.attr("id") );
        
        tl_disabled($(xml).read("cart_track_album_id:eq(0)"));// premier album ajout� au cart

        //disab. butt
        o.attr("disabled",true);
        o.css({"color":"#fff","margin":"0 5px 0 0"});
        if(p_type == "1"){//dans le cas du TL
        o.css({"background":"url(./templates/img/ico_famfam/tick.png) no-repeat 2px 0px"});
        o.after("<input type=\"button\" onClick=\"$(this).delete_from_tl();\" class=\"cart-ico-suppr\" id=\"tl-suppr_"+objetType+"_"+$(xml).read("cart_track_album_id:eq(0)")+"\" value=\"&nbsp;\" />");
        }      
    }else{
      o.css({"color":"#fff","background":"#000"}).html("item ajout�");
    }
    */
