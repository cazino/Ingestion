// Input functions


/*
 * v.1 (c) 2005 Nicolas Martin & Olivier Meunier and contributors ('resize.js' projet DotClear)
 * v.1.5 (c) 2007 (c) Fil -> resizehandle.js  
 * v.1.6 (c) 2008 $$ extend.250108-1156 $$ ajout de la notion de largeur pour le textarea
 * v.1.7 (c) 2008 $$ extend.010208-1747 $$ ajout de la notion de largeur pour le div simulant la poignée d'étirement "safari-like"
 * v.1.8 (c) 2008 $$ extend.280608-2002 $$ ajout 'settings'
 * ****
 * le script genere un div en dessous du textarea, supprime la border-bottom de ce textarea   
 * **  box model à suivre : div > form > textarea 
 */
$.fn.resizehandle = function(settings) {

settings = jQuery.extend({
			sliderWidth: 30,
			sliderBorderColor: "#FF00CC"
		}, settings);



if($.browser.safari){
return false;
}else{
  return this.each(function() {
  var a = document.createElement("div");$(a).attr("class", "slider");$(a).attr("title", "Cliquer pour agrandir");
  var me = $(this);
    
  //creation du slider ,margin:"5px 0 20px 0",, "width":w, 
  me.css({"border-bottom":"none"});// suppr. la border basse du textarea
  $(a).css({"border": "1px solid "+settings.sliderBorderColor, "border-top":"none","width":+ settings.sliderWidth +"px"});
  

  //alert(me.parents("box-input-comm:eq(0)") + " <- " + me.attr("id"));/**/
  
      $(a).bind('mousedown', function(e) {
        // textearea
        var h = me.height(); var y = e.clientY;
        var w = me.width();  var x = e.clientX;//v.1.6
        
        // slider //v.1.7
        var v_slider = $(this);
        var w_s = v_slider.width(); //alert(w_s);
          
        var moveHandler = function(e) {
          // permet d'agrandir le textarea
          me.height(Math.max(20, e.clientY + h - y));
          me.width(Math.max(20, e.clientX + w - x));//v.1.6
          
          // permet d'agrandir le div situé dessous //v.1.7
          v_slider.width(Math.max(20, e.clientX + w_s - x));
          
          me.parents("div:eq(0)").width(Math.max(20, e.clientX + w - x) );

        };
        var upHandler = function(e) {
          jQuery('html')
          .unbind('mousemove',moveHandler)
          .unbind('mouseup',upHandler);
        };
        jQuery('html')
        .bind('mousemove', moveHandler)
        .bind('mouseup', upHandler);
      });//eo.bind

   
    // ajout d'un "div" $$ apres la structure __label_/_input_/_br{clear:both}
    $("#" + $(this).attr("id") + "").next('br').after("<br style='clear:both;'>").after($(a));

  });
}//eo.if
}//oe.fonc



  /*
  - compte le nombre de caractère dans un textarea ("/emploi_offres_ajout.php" et "/pa_ajout.php")
  */
$.fn.character_counter = function(p_maxi_num_char){
  var char_cnt_label = $("#descr-nb-car");
  
  function keyUpEvent(e){
    var val = $(this).val();
    var err_str = "";

    err_str += "(Nombre de caractères autorisés : " + (p_maxi_num_char - val.length) + ")";
   
    if(val.length >= p_maxi_num_char){
      err_str += "<br>!! Nombre de caractères maximal atteinds !!";
      $(this).val($(this).val().substring(0, p_maxi_num_char)); 
      pulse(char_cnt_label, true); 
    }
    //ecriture du compteur    
    char_cnt_label.html(err_str);

  }//eo.func $$ keyUpEvent
  
  //(c) 2007 Tom Deater (http://www.tomdeater.com) 
  var p;
	function pulse(el, again) {                         
    if (p) {                               
    window.clearTimeout(p);                                 
    p = null;                         
    };                         
	el.animate({ opacity: 0.1 }, 100, function() {                                
 	$(this).animate({ opacity: 1.0 }, 100);                         
	});                        
    if (again) {                                 
    p = window.setTimeout(function() { pulse(el) }, 200);                         
    };                 
  }//eo.func. $$ pulse

  return this.each(function() {
  $(this).bind("keydown", keyUpEvent);
  $(this).bind("keypress", keyUpEvent);
  $(this).bind("keyup", keyUpEvent);
  $(this).bind("focus", keyUpEvent);

  });//eo.return this.each()
}//eo.func
