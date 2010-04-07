<?php
  
  /**
  
  Build the correct javascript for CADI spy, given the type of page which calls it
  
  */

  $id = $_GET['id'];
  ?>
  
function post_cadi_datas(jstag){
  $.ajax({
    type: "POST",
    url: "/includes/ajax.lib.php",
    data: 'p=cadi_post&jstag='+jstag,
		async: false,
    error: function(a,b,c){
		  alert("Erreur");
		},
    success: function(jstag){
		  //alert("Success="+jstag);
		}
	});		
}
		
  
  <?php
  switch($id){
  
  	case 'home':
		?>
		$(document).ready(function() {
						   
			$("a,#bt_valid_qs,option,#bg-cart-header").click(function(){
				var jstag = $(this).attr("jstag");
				post_cadi_datas(jstag);
			});
		});
		<?php
		break;
		
	case 'continent':
		?>
		
$(document).ready(function() {		   
  $("a,#bt_valid_qs,option,#bg-cart-header,.off").click(function(){	 
	 var jstag = $(this).attr("jstag");
	 post_cadi_datas(jstag);
	});
});
		
$(document).ready(function() { 
  $('#artistes-par-lettre-liste,#artistes-par-pays-liste').click(function(event) {
    var $tgt = $(event.target);
    if ($tgt.is("a")) {
      post_cadi_datas($tgt.attr("jstag"));
    }
	});
});
			
		<?php
		break;
  
  	case 'genre':
		?>
		
	
		$(document).ready(function() {
			$("a,#bt_valid_qs,option,#bg-cart-header,.off").click(function(){	 
				var jstag = $(this).attr("jstag");
				post_cadi_datas(jstag);
			});
		});
		
		$(document).ready(function() { 
  			$('#artistes-par-lettre-liste,#artistes-par-pays-liste').click(function(event) {
    			var $tgt = $(event.target);
    			if ($tgt.is('li a,li b')) {
      				post_cadi_datas($tgt.parents('li').attr("jstag"));
    			}
			});
		});
			
		<?php
		break;
  
  
  	case 'artiste':
		?>
				
		$(document).ready(function() {		   
			$("a,#bt_valid_qs,option,#bg-cart-header,.bt-cart-track,.cart-ico-suppr,.bt-ecoute").click(function(){	 
				var jstag = $(this).attr("jstag");
				post_cadi_datas(jstag);
			});			
		});	
				
		<?php
		break;
  }
?>
