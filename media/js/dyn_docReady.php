<?php
  require_once "../../_wsite.conf.php";
/**
 * GLOBAL
 * 
 */
 
 // permet de sectionner le fichier JS ci-dessous
  $arr_tmp = $_GET['w'];
  $arr_w = explode(",", $arr_tmp);
  for($i=0;$i < count($arr_w);$i++){
    $ex = explode("=",$arr_w[$i]);
    eval("\$".$ex[0]." = '".$ex[1]."';");
  }

  $where_am_i = $arr_w[0];



  /**
   * Creation var. textes JS (stockees dans JQ)
   * 011008-161722
   */        
  reset($js_str2[LNG]); $cnt = 1;
  $str_json = "var js_l10n = {";
  while (list($key, $val) = each($js_str2[LNG])) {
    ($cnt != count($js_str2[LNG]))?$sep=", ":$sep="";
    $str_json .= $key ." : \"".$val."\"".$sep;
    $cnt++;
  }
  $str_json .= "};\n";

  
  


  //nav
  ?>
$(document).ready(function(){
  /***
   * Code Commun
  */

  //DBG : border  toutes les div
  //$("div").css("border","1px solid red");

  
  // on enleve le focus (bordure pointille) autour d'un lien lors d'un click sur les elem. ci-dessous
  $("a,:submit,:checkbox,:radio,:button").focus(function(){
    $(this)[0].blur();
  });


  // chaine de caractres traduites via PHP (ref.011008-161722)
  <?=$str_json;?>
  $.extend(js_l10n);



  //add.160708-163359 $$ champ 'recherche'
  var o_bxS = $("#fld_qs");

    if(o_bxS.val() == "par mots-clés" || o_bxS.val() == "by keywords" ){
    o_bxS.focus(function(){
      $(this).val("");
    });
    }
  
  /**
   * NL - Newsletter
   * 170608-001930 $$ 180908-201455       		   
   */
    var o_inputNL = $("#pro_email_nl");
    if(o_inputNL.val() == "Votre email" || o_inputNL.val() == "Your email" ){
      o_inputNL.focus(function(){
      $(this).css({background:'#DFDEC3'}).val('');
      });
    }



   /*////////////////////////////////////////////
    * Affichage permanent du panier 
    * 310708-154521 $$ 071008-000000    
    **/
      var fl_cart = document.createElement("div"); $(fl_cart).attr("id","float-cart");//$.cart_item+  +
      //var nb_itemzz = parseFloat($("#cart-item-nb").text());//---depre.081008-103728
      var fl_cart_bt_cko = "<div id=\"fc-content\">";
      //--deprefl_cart_bt_cko += "<div class='fc-cko'><a href=\"\" onClick=\"$('#cart-itemz').fadeIn('slow'); $('html,body').animate({scrollTop: '0px'}, 1000); return false;\">"+$.checkout_now + " ("+ nb_itemzz +")</a>";
      fl_cart_bt_cko += "<div class='fc-cko'><a href=\"\" onClick=\"$('#cart-itemz').fadeIn('slow'); $('html,body').animate({scrollTop: '0px'}, 1000); return false;\">"+$.bt_flottant_libelle + "</a>";
      fl_cart_bt_cko += "</div>";
      fl_cart_bt_cko += "</div>";

      $(fl_cart).html(fl_cart_bt_cko);
      $(fl_cart).prependTo("body");
      
  
      // event scroll
      $(window).scroll(function(){
      
      var fc_nbitem = parseFloat($('#cart-item-nb').text());
      
        if(!isNaN(fc_nbitem) || fc_nbitem > "0"){
          if ($(window).scrollTop() >= "170"){
          $("#float-cart").fadeIn("slow");
          }else{
          $("#float-cart").fadeOut("slow");
          }
        }else{
          $("#float-cart").fadeOut("slow");
        }
      });
    ////////////////////////////////////////////

}); //eo.document.ready()




  /***
   * Popup (et oui)
   * 100908-194345   
  **/
  function pop(mylink, w,h, nom){
  
  	if (! window.focus) return true;
  	var href;
  	if (typeof(mylink) == 'string') href=mylink;
  	else href=mylink.href;
  	var a = window.open(href, nom, 'width='+w+',height='+h+',scrollbars=no');
  	a.focus();
  	return false;
  }

  /**
   * Popup radio
   * 120908-19243
   */        
  function standalone_player(){
    pop("radio.php?lng=en","330","270","radio");
  }
  

  /***
  * Lire un noeud XML
  */ 
  $.fn.read = function(p_id){
    return $(this).find(p_id).text();
  }
  


  /***
   * Lire du contenu from dotCom
   * 120908-192612   
   */
  var dotCom_content = function(p_artist_rwURL){
    
    $.ajax({
      type: "POST",
      url: "/includes/ajax.lib.php",
      data: "p=dotCom_content&value=" + p_artist_rwURL,
      success: function(xml){
      
      //alert(xml);
      var conteiner = $(".txt-dotcom"); var str = "";var str_itw = "";
      var a = document.createElement("div"); 
      $(a).addClass("box-dotCom-portrait"); 
      
      var c = document.createElement("p");
      $(c).html($(xml).read("portrait texte")).attr("id", "portrait-dotcom");
      //alert($(xml).find("texte").text());
      
      var b = document.createElement("a");
      $(b).attr("href", $(xml).read("portrait url")).html("Plus d'infos sur mondomix.com").addClass("lien-dotcom");
      
      var d = document.createElement("ul");
      $(d).attr("id", "videos-dotcom");
      
        $(xml).find("video").each(function() {
          str += "<li><img src=\""+$(this).read("image")+ "\" />";
          str += "<a href=\""+$(this).read("url")+"\">" + $(this).read("titre") + "</a></li>";
        });
        $(d).append(""+ str +"");
        
      var e = document.createElement("ul");
      $(e).attr("id", "itw-dotcom");
      
        $(xml).find("interview").each(function() {
          str_itw += "<li><a href=\""+$(this).read("url")+"\">" + $(this).read("titre") + "</a></li>";
        
        });
        $(e).append(""+ str_itw +"");

      // insertion globale
      conteiner.append($(a).append(c, b, d,e));    

      
      
      }//eo.succ
    })//eo.jx
  
  
  }//eo.func $$         


      /**
       * Contexte menu $$ ctx       
       * 270608-22227
       * l10n ($js_str[]) : cf. _wsite.conf.php
       */
      
  var context_menu = function(p_objet_id, p_objet_type, p_origin_click){//

     var a = document.createElement("a"); $(a).attr("href","#");$(a).html($.add2cart); $(a).addClass("bt-lien-fleche");
     $(a).attr("id","ctxAdd_"+p_objet_type+"_"+p_objet_id);
      
     $(a).click(function(){
       cart_add(p_objet_id, p_objet_type);
       return true;
     });


    $.ajax({
      type: "POST",
      url: "/includes/ajax.lib.php",
      data: "p=jax_home_infos_alb&id=" + p_objet_id + "&value=" + p_objet_type,
      success: function(xml){
      var str = "";
      var b = document.createElement("a"); $(b).addClass("bt-lien-fleche");

      switch(p_objet_type){
        case "1": //titre
        $(b).html($.listen_track); $(b).attr("href","#");
        $(b).click(function(){
          pop('/player.php?oid=' + p_objet_id + '&otype=' + p_objet_type + '&olng='+$.flalng  ,'400','402','player');
        });        
        break;
        
        case "2":
        $(b).html($.listen_album); $(b).attr("href","#");
        $(b).click(function(){
          pop('/player.php?oid=' + p_objet_id + '&otype=' + p_objet_type + '&olng='+$.flalng ,'400','402','player');
        });
        break;
      }
       
        str += "<span class=\"info\">" + $.prix + " : <b>" + $(xml).read("prix") + $(xml).read("currency") + "</b></span>";
        str += "<span class=\"info\">" + $.format + " : <b>" + $(xml).read("format") + "</b> ("+ $(xml).read("bitrate") +"Kb/s)</span>";
        str += "<span class=\"info\">" + $.duree + " : <b>" + $(xml).read("duree") + "</b></span>";

        $("#ctx-menu").remove();//on efface avant d'afficher
        var sp = document.createElement("div");$(sp).attr("id","ctx-menu");
        $(sp).html(""+ str + "");

        $(sp).append($(a),$(b));
        
         
        if($.browser.msie){
          $(sp).appendTo("#" + p_origin_click +"-"+ p_objet_id).fadeIn(200);
        }else{
          $("#" + p_origin_click +"-"+ p_objet_id).prepend($(sp).fadeIn());
        }
        
      // Suppr. div : 'esc' key
      $(document).bind('keydown.ctx-menu', function(e) {
        if (e.keyCode == 27) $(sp).fadeOut(200);
        return true;
      });
      
      // si le curseur 'quitte' le layer
      $(sp).bind('mouseleave', function(e) {
        $(sp).fadeOut(200);
        return true;
      });

      }//eo.success
    
    });//eo.ajax
    
  }//eo.func

    /***
     * RECREER PASSWORD ----depre
     */         
    $.fn.forgot_pwd = function(){
      var a = $('#pro_email_forgot_pwd'); var msg;
      $("#err_forgotpwd").remove();
  //alert(a.val());
      // post
      $.ajax({
      type: "POST",
      url: "./includes/ajax.lib.php",
      data: "p=jax_profil_forgot&value=" + a.val(),
      success: function(feedb_code){
        switch(feedb_code){
          case "err_1": msg = "probl. recreate pass";break;          
          case "err_5": msg = "email inexistant dans bdd";break;
          case "err_10": msg = "deja log";break;
          case "1":
          msg = "pass re-cr ; vous avez recu un mail contenant votre nouveau mot de passe";
          $('#identification').show();$('#pro_email_forgot_pwd, #bt_forgot_pwd_valid').attr({disabled:"true",style:"opacity:.45;"})
          break;
          
        }//eo.switch
       var sp = document.createElement("div");
        $(sp).attr({style:"background:red;opacity:1;cursor:default;width:111px;height:30px;",id:"err_forgotpwd"});
        $(sp).html(msg);
        $("#forgot-pwd fieldset").after($(sp));
      }//fct
      });//eo.ajax
    
    };//$.fn.forgot_pwd
    

  /****
   * NL
   * 170908-224422
  **/
   function add_mail2nl(){

    var v = $('#pro_email_nl');
    var msg_Err="";
  
    // check structure adresse
    var poset = v.val().indexOf("@");
    var pospunto = v.val().indexOf(".");
  
    if(poset == -1 || pospunto == -1 || !v.val()){
      $.facebox('E-Mail non valide');
    }else{

    // post
      $.ajax({
       type: "POST",
       url: "./includes/ajax.lib.php",
       data: "p=checkNL_addNL&value=" + v.val(),
       success: function(msg){
          if (msg == 0){
          $.facebox('Vous tes dj inscrit  la newsletter');
          }else{
          // creation du msg ; ajout en bdd est via ajax
          $.facebox('Votre adresse a t ajoute');
         }
       }
      });//eo.ajax
    }
    
  }//eo.func


  /*
  * liste albums par genre et par lettre
  */
  $.fn.alb_par_lettre = function(p_genre, p_lettre){
    var o = $(this); var itemid = o.attr("id");
    $.ajax({
      type: "POST",
      url: "/includes/ajax.lib.php",
      data: "p=jax_hp_albums_par_genre-lettre&id=" + p_genre + "&value=" +p_lettre,
      success: function(xml){
       var str = "";
       
        if($(xml).read("object") == ""){
          str = "<li>Aucun rsultat pour la lettre '" + p_lettre + "'</li>\n";
        }else{
          $(xml).find("album_ssgenre").each(function() { 
          str += "<li jstag=\"alphabetical_list-" + p_lettre + "_artist-"+ $(this).read("artist") + "\"><a href=\""+$(this).read("rw_art_name")+"\"><b>" + $(this).read("art_name") + "</b> - "+$(this).read("alb_title")+"</a> ("+$(this).read("sty_name")+")</li>\n";
          });
        }
    
        $("#artistes-par-lettre-liste li").remove();// on vide l'UL
        $("#artistes-par-lettre-liste").append(str);// pop. mit nu results
        $("#artistes-par-lettre-liste").show(400);// display it!
        
        $("#artistes-par-pays-liste").hide();
        $("#pays-par-continent-liste").val("");// raz selectbox
        
        //layout
        $("#alfabeta li").removeClass("on").addClass("off");//raz 'class'  off
        $("#" + itemid).addClass("on");
        
        }//eo.success
      });//eo.ajax
    }//eo.func



  /*
  * liste albums par ssgenre et par lettre (ssgenre.php)
  * 110209-163211  
  */
  $.fn.alb_par_ssgenre_lettre = function(p_genre, p_lettre){
    var o = $(this); var itemid = o.attr("id");
    $.ajax({
      type: "POST",
      url: "/includes/ajax.lib.php",
      data: "p=jax_hp_albums_par_ssgenre-lettre&id=" + p_genre + "&value=" +p_lettre,
      success: function(xml){
       var str = "";
       
        if($(xml).read("object") == ""){
          str = "<li>Aucun rsultat pour la lettre '" + p_lettre + "'</li>\n";
        }else{
          $(xml).find("album_ssgenre").each(function() { 
          str += "<li jstag=\"alphabetical_list-" + p_lettre + "_artist-"+ $(this).read("artist") + "\"><a href=\"/"+$(this).read("rw_art_name")+"\"><b>" + $(this).read("art_name") + "</b> - "+$(this).read("alb_title")+"</a></li>\n";
          });
        }
    
        $("#artistes-par-lettre-liste li").remove();// on vide l'UL
        $("#artistes-par-lettre-liste").append(str);// pop. mit nu results
        $("#artistes-par-lettre-liste").show(400);// display it!
        
        $("#artistes-par-pays-liste").hide();
        $("#pays-par-continent-liste").val("");// raz selectbox
        
        //layout
        $("#alfabeta li").removeClass("on").addClass("off");//raz 'class'  off
        $("#" + itemid).addClass("on");
        
        }//eo.success
      });//eo.ajax
    }//eo.func    
    
    
  /*
  * liste albums par pays et par lettre (pays.php)
  * 020309-162442
  * 090309-123213 $$ l10n msg erreur  
  */
  $.fn.alb_par_pays_lettre = function(p_genre, p_lettre){
    var o = $(this); var itemid = o.attr("id");
    $.ajax({
      type: "POST",
      url: "/includes/ajax.lib.php",
      data: "p=jax_hp_albums_par_pays-lettre&id=" + p_genre + "&value=" +p_lettre,
      success: function(xml){
       var str = "";
       
        if($(xml).read("object") == ""){
          str = "<li>"+$.pays_liste_artiste_noresult+" '" + p_lettre + "'</li>\n";
        }else{
          $(xml).find("album_ssgenre").each(function() { 
          str += "<li jstag=\"alphabetical_list-" + p_lettre + "_artist-"+ $(this).read("artist") + "\"><a href=\"/"+$(this).read("rw_art_name")+"\"><b>" + $(this).read("art_name") + "</b> - "+$(this).read("alb_title")+"</a></li>\n";
          });
        }
    
        $("#artistes-par-lettre-liste li").remove();// on vide l'UL
        $("#artistes-par-lettre-liste").append(str);// pop. mit nu results
        $("#artistes-par-lettre-liste").show(400);// display it!
        
        $("#artistes-par-pays-liste").hide();
        $("#pays-par-continent-liste").val("");// raz selectbox
        
        //layout
        $("#alfabeta li").removeClass("on").addClass("off");//raz 'class'  off
        $("#" + itemid).addClass("on");
        
        }//eo.success
      });//eo.ajax
    }//eo.func  
    

  <?//PHP
  switch($where_am_i){
  
  case "inscription":?>
  /**
   * INSCRIPTION
   */
$(document).ready(function() {
	/*$("#inscription").validate();*/
});

  <?break;?>
  
    
  
    <?case "home":
    case "continent":
    case "genre":?>
    
  
  $(document).ready(function(){
      
      

    <?if($arr_w[1] == "err=artist"){?>
    // Gestion d'erreur dyn. en cas d'artiste n'ayant pas d'album à vendre
    //add.161208-150927
    $.facebox($.err_artist_no_available);
    <?}?>
    

    <?if($arr_w[1] == "err=unlog_sess"){?>
    // Gestion d'erreur dyn. en cas de péremption de session (donc delogg)
    //add.100209-150913    
    $.facebox($.err_unlog_peremption_session);
    <?}?>
    
    <?if($arr_w[1] == "err=err_log"){?>
    // Gestion d'erreur de login (mauvais mot de passe)
    //add.100209-162256
    $.facebox($.err_login);
    
    // affichage du champ de login    
    $('#fieldset,#box-forg-pwd').show();$('#bt-reg, #bt-auth').hide();
    
    <?}?>
      
      /**
      * suppr. last border nav top
      */  
      $("#nav-top li:last").css({border:"none"});
      

      
      /**
      * ajout 2px pour 1ere vignette "a la une"
      */
      $(".box-tof:first").css({padding:"4px 5px 2px 5px"});
      $(".box-texte:first,.box-texte:last").css({padding:"4px 0 0 0"});
      $(".box-tof:last").css({padding:"2px 5px 4px 5px"});
      
      $("#box-promotions img:eq(1)").css({margin:"26px 0 0 0"});
      
   
   

    
    
    //suppr. all border
    //$("div").css({border:"0"});

      
      
      
	});//eo $().ready()
	
    /*
    * infos liees au flash highlight
    */
    function ajx_highlight(p_id){
       
      $.ajax({
      type: "POST",
      url: "./includes/ajax.lib.php",
      data: "p=jax_hgl_items_home&id=" + p_id,
      success: function(ajax_feedbak){
      
      
        if(ajax_feedbak != 0){
  
        $("#box-slideshow-texte").html(ajax_feedbak);
        }else{
        $("#box-slideshow-texte").html("probl id : " + p_id);
        }
  
      }//fct
      });//eo.ajax
    }

  /*
  * liste pays par continent
  */
  $.fn.artistes_par_lettre = function(p_cont, p_lettre){
  
    var o = $(this); var itemid = o.attr("id");

    $.ajax({
      type: "POST",
      url: "./includes/ajax.lib.php",
      data: "p=jax_hp_artistes_par_continent-lettre&id=" + p_cont + "&value=" +p_lettre,
      success: function(xml){
       var str = "";
       
        if($(xml).read("object") == ""){
          str = "<li>Aucun rsultat pour la lettre '" + p_lettre + "'</li>\n";
        }else{
          $(xml).find("one_artist").each(function() { 
          // static ver.
          str += "<li><a href=\""+$(this).read("rw_art_name")+"\" jstag=\"alphabetical_list_artist-"+$(this).read("artist")+"\">" + $(this).read("art_name") + "</a></li>\n";
          //str += "<li onClick=\"artiste_par_pays('" + $(this).read("artist") + "');\">" + $(this).read("art_name") + "</li>\n";
          
          });
        }
  
        $("#artistes-par-lettre-liste li").remove();// on vide l'UL
        $("#artistes-par-lettre-liste").append(str);// pop. mit nu results
        $("#artistes-par-lettre-liste").show(400);// display it!
        
        $("#artistes-par-pays-liste").hide();
        $("#pays-par-continent-liste").val("");// raz selectbox
        
  
          //layout
          $("#alfabeta li").removeClass("on").addClass("off");//raz 'class'  off
          $("#" + itemid).addClass("on");
        //$(this).css("font-weight","bold");
  
  
        }//eo.success
    
      });//eo.ajax
      
    }//eo.func
    
    
  /*
  * liste artiste_par_pays
  */
  $.fn.artiste_par_pays = function(){//

  var p_id_pays = $(this).val();
  var select_id = $(this).attr('id');
  p_pays_name = $("#"+select_id+ " :selected").text();

  /*  */
  $.ajax({
    type: "POST",
    url: "./includes/ajax.lib.php",
    data: "p=jax_hp_artiste_par_pays&id=" + p_id_pays,
    success: function(xml){
     var str = ""; var void_;
     
      if($(xml).read("object") == ""){
        str = "<li>Aucun rsultat pour le pays '" + p_pays_name + "'</li>\n";
      }else{
        $(xml).find("artist_country").each(function() { 
        str += "<li><a href=\""+$(this).read("rw_art_name")+"\" jstag=\"country_list_artist-"+$(this).read("artist")+"\">" + $(this).read("art_name") + "</a></li>\n";
        });
      }

      $("#artistes-par-pays-liste li").remove();
      $("#artistes-par-pays-liste").append(str).show(400);
      
      $("#artistes-par-lettre-liste").hide();// cache l'autre liste

      }//eo.success
    });//eo.ajax

    }//eo.func  





  /************************************
  * liste artiste_par_ssgenre
  */
  $.fn.alb_par_ssgenre = function(){
  
  //console.log($(this).attr("id") + ": "+ $(this).val());alert(p_id_pays);
  p_id_pays = $(this).val();
  if(p_id_pays != ""){
    /*  */
    $.ajax({
      type: "POST",
      url: "./includes/ajax.lib.php",
      data: "p=jax_hp_albums_par_ssgenre&id=" + p_id_pays,
      success: function(xml){
       var str = "";
       
        if($(xml).read("object") == ""){
          str = "<li>Aucun rsultat pour le sous genre '" + $(xml).read("sty_name") + "'</li>\n";
        }else{
          $(xml).find("album_ssgenre").each(function() { 
          str += "<li jstag=\"style_list-" + p_id_pays + "_artist-" +$(this).read("artist")+ "\"><a href=\""+$(this).read("rw_art_name")+"\"><b>" + $(this).read("art_name") + "</b> - "+$(this).read("alb_title")+"</a></li>\n";
          });
        }
  
        $("#artistes-par-pays-liste li").remove();
        $("#artistes-par-pays-liste").append(str).show(400);
        
        $("#artistes-par-lettre-liste").hide();// cache l'autre liste
  
        }//eo.success
      });//eo.ajax
  }//eo.if
  }//eo.func  
    
      

      
      
    <?
   
    break;
    
    case "artiste":
    case "checkout":
    case "profil":
    
    /*
    Cart -> voir "panier.lib"
    */
    ?>
  
 


    
    <?
    //seuleent checkout
    if($where_am_i == "checkout"){
    ?>
    //* checkout only         
    $(document).ready(function(){
        
/******* --depre.170209-132238       
        //step no logged
        $("#pro_email_reg-com, #pro_email_log-com, #pro_password_log-com,#bt_reg_valid-com, #bt_identification_valid-com")
          .attr("disabled", true).css({"background":"#ccc","cursor":"default"});
          
      $("#cko-reg input[@type=radio]").click(function(){
      
        if($(this+"[@checked]")){
        $("#cko-reg input").attr("disabled", false).css({"background":"#fff","cursor":"default"});
        $("#cko-login input[@type=radio]").attr("checked", false);
        
        $("#cko-login input").css({"background":"#ccc","cursor":"default"});
        }else{
        //$("#cko-reg input").attr("disabled", true).css({"background":"#ccc","cursor":"default"});
        
        $("#cko-login input[@type=radio]").attr("checked", true);
        }
        
      });
      
      $("#cko-login input[@type=radio]").click(function(){
      
        if($(this+"[@checked]")){
        $("#cko-login input").attr("disabled", false).css({"background":"#fff","cursor":"default"});
        $("#cko-reg input[@type=radio]").attr("checked", false);
        
         $("#cko-reg input").css({"background":"#ccc","cursor":"default"});
        }else{
        //$("#cko-login input").attr("disabled", true).css({"background":"#ccc","cursor":"default"});
        
        $("#cko-reg input[@type=radio]").attr("checked", true);
        }
        
      });
******/        
        // step2
        $("#cko-submit-step2").attr("disabled", true).css({"color":"#ccc","cursor":"default"});
        $("#liste-credit-forfait").attr("disabled", true);
    });//$(document).ready(function(){
    


  /**
   * 311208-121435 $$ 160109-115140
   */     
  function choix_type_paiement(p_nb_credit, p_nb_objet){
       
      var checked_pp = $("#pay_type_pp").attr("checked");
      //(checked_pp)?$("#pay_wallet").attr("disabled", 1):$("#pay_wallet").attr("disabled", 0);
            
      var checked_pw = $("#pay_type_wallet_mdx").attr("checked");
      //(checked_pw)?$("#pay_paypal").attr("disabled", 1):$("#pay_paypal").attr("disabled", 0);
      
      if(checked_pp){
      $("#cko-submit-step2").attr("disabled", false).css({"color":"#fff","cursor":"pointer"});
      }else{
      $("#cko-submit-step2").attr("disabled", true).css({"color":"#ccc","cursor":"default"});
      }
      
      if(checked_pw){
        if(p_nb_credit < p_nb_objet){
        $("#liste-credit-forfait").attr("disabled", false);
        
        $("#liste-credit-forfait").change(function(){
          if($(this).val() != ""){
           $("#cko-submit-step2").attr("disabled", false).css({"color":"#fff","cursor":"pointer"});
          }else{
            $("#cko-submit-step2").attr("disabled", true).css({"color":"#ccc","cursor":"default"});
          }
        });
        }else{
        $("#cko-submit-step2").attr("disabled", false).css({"color":"#fff","cursor":"pointer"});
        }
      }else{
        $("#liste-credit-forfait").attr("disabled", true);
      }
      
      //$("#liste-credit-forfait").val() != ""
      
      /** -- depre
      if(checked_pw){
        if(p_nb_credit < p_nb_objet){
        $("#nucredit_tr").show();
        }
      }else{
        $("#nucredit_tr").hide();
      }
      **/
  }//eo.func
  
  
    
    <?
    }//eo.if $$ only checkout?>
  
    <?
    //seuleent Artiste
    if($where_am_i == "artiste"){
    ?> 


  /// DOC READY
  $(document).ready(function(){     
		
	// commentaire $$ resize handle --DEPRE.300109-182648
  //$(".com-texte").resizehandle({sliderWidth:"190", sliderBorderColor:"#000"});
  //$(".com-texte").character_counter('10');
		

		
  });//eo.$(document).ready()
    <?
    }//eo. only artiste
    ?>
  
    <?
    //seuleent profil
    if($where_am_i == "profil"){
    ?>
    //* profil only         

$(document).ready(function(){

  $(".album-titre").css({cursor:"pointer"});
  $(".album-titre").click(function(){
    $(this).parent(".li-titre-album").children('ul.album-tracklisting').toggle();
    //$(this).next()find('ul.album-tracklisting').toggle();
    
    // --DEPRE.110708-222349
    //var sp = $(this).next("span.toggle"); if(sp.html() == "+"){sp.html("-");}else{sp.html("+");}// - et +
  });
  //$(".cross").css({cursor:"crosshair"});

});//$(document).ready()
    
    
    /**
     * exp.100608-143525 $$
     */         
    function dotCom_xCnx(){
      $.ajax({
      type: "GET",
          url: "./includes/ajax.lib.php",
          data: "p=jax_dotCom_xCnx",
      error: function(json,z,u){
      
      $("#box-crossdomain_dataz").html(json + ' ' +z + '-'+ u);
      },
      success: function(json){
      //console.log('1' + json);
      
      //  $(sp).html('Status : ' + ws.dataz.pseudo + '<br># Transaction : ' + msg.pp_txn_id);
      $("#box-crossdomain_dataz").html( json);
      
      }//fct$$success
      });//eo.ajax
      
    }//eo.func $$ _xCnx()
    
    
    $.fn.GZ_track = function(p_track_id){
      //json.feedback_code == "0" : OK
      var sp = document.createElement("p");
      $(sp).attr({style:"width:180px;"});
      
      // AJAX
      $.ajax({
      type: "POST",
      url: "./includes/ajax.lib.php",
      data: "p=proxy-dl&id=" + p_track_id,
      //dataType:"json",
      error: function(json,z,u){$(sp).html("error ajax : " + z); $('#dl_tr_' + p_track_id).append(sp);},
      beforeSend: function (json){ $(sp).addClass('processing').html("loading..."); $('#dl_tr_' + p_track_id).append(sp);},
      success: function(json){

        $(sp).addClass('done').html(json.feedback_link);
        $('#' + p_item2zip).append(sp);
      }//fct$$success
      
      });//eo.ajax
    
    
    
    }
    
    
    /**
     * Zip un album en arriere plan
     * 140608-195744     
     */         
    $.fn.zip_alb = function(p_item2zip, p_cart_item_id){
    
      //json.feedback_code == "0" : OK
      var sp = document.createElement("p");
      $(sp).attr({style:"width:180px;"});
      
      // AJAX
      $.ajax({
      type: "POST",
      url: "./includes/ajax.lib.php",
      data: "p=jax_zip_alb&id=" + p_item2zip + "&value=" + p_cart_item_id,
      dataType:"json",
      error: function(json,z,u){$(sp).html("error ajax : " + z); $('#' + p_item2zip).append(sp);},
      beforeSend: function (json){ $(sp).addClass('processing').html("loading..."); $('#' + p_item2zip).append(sp);},
      success: function(json){

        $(sp).addClass('done').html(json.feedback_link);
        $('#' + p_item2zip).append(sp);
      }//fct$$success
      
      });//eo.ajax
      
       
    }//eo.func $$ zip() 
      
    /**
     * Ajout PL
     * todo.100608-181111     
     */         
    $.fn.pls_add = function(){
    var o = $(this);
    
    //console.log("1/ "+ o.parents(".li-titre-album").attr("id") );
    }
    
    

/*** STANDBY $$ jax_domain $$ TODO 090608-145316

///////////////./includes/ajax.lib.php  data: "p=jax_crossdomain"
$(document).ready(function(){

  $.ajax({
  type: "GET",
  url: "test.xml",
  dataType:"json",
  error: function(json,z,u){
  
  $("#box-crossdomain_dataz").html(json + ' ' +z + '-'+ u);
  },
  success: function(json){
  console.log('1' + json);
  
//  $(sp).html('Status : ' + ws.dataz.pseudo + '<br># Transaction : ' + msg.pp_txn_id);
  $("#box-crossdomain_dataz").html( json.description);

  }//fct$$success
  });//eo.ajax

});
*/
///////////////


   
    <?
    }//eo.if $$ only profil?>


    <?
    //seuleent artiste
    if($where_am_i == "artiste"){?>
    /*
    ---> ARTISTES
    */
    
  $(document).ready(function(){
    
    // tab
    //$("#box-tabs2 ul").idTabs();
    $("#box-tabs2").idTabs(function(id,list,set){ 
      $("a",set).removeClass("selected") 
      .filter("[@href='"+id+"']",set).addClass("selected"); 
      for(i in list) 
        $(list[i]).hide(); 
      $(id).fadeIn(); 
      return false; 
    }); 
    
    // photos in facebox :: img rel=facebox
    $('a[rel*=facebox]').facebox(); 
    // mimic above
    $(".ico-zoom").css({"cursor":"pointer"}).click(function(){
      var tofurl = $(this).next("a").attr("href");
      $.facebox({ image: tofurl });
    });
    
    });//eo.docready()


    <?
    }//eo.if $$ only artiste
    break;
    
    /**
     * recherche
     * 280708-12452     
     */         
    case "recherche":
    ?>
    $(document).ready(function(){
    
      $("ul.col-res li:first-child .box-tof").css({"padding-top":"5px"});
      $("ul.col-res li:last-child .box-tof").css({"padding-bottom":"5px"});
      $("ul.col-res li:last-child .box-texte").css({"padding-bottom":"2px"});
    });//eo.docready()
    
    <?
    break;
    

  }//eo.switch
//echo $where_am_i;
?>
