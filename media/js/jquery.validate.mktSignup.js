 $(document).ready(function(){
 	
	jQuery.validator.addMethod("password", function( value, element ) {
		var result = this.optional(element) || value.length >= 6 && /\d/.test(value) && /[a-z]/i.test(value);
		if (!result) {
			element.value = "";
			var validator = this;
			setTimeout(function() {
				validator.blockFocusCleanup = true;
				element.focus();
				validator.blockFocusCleanup = false;
			}, 1);
		}
		return result;
	}, "Your password must be at least 6 characters long and contain at least one number and one character.");

	
	jQuery.validator.messages.required = "";

	$("#inscription").validate({
		onkeyup: false,
		rules: {
			fld_captcha: {
				required: true,
				remote: "./includes/captcha/process.php"
			}
		},
		messages: {
			fld_pass_ischeck: {
				required: " ",
				equalTo: "Votre mot de passe et sa confirmation ne sont pas identiques"	
			}
			,pro_email: {
				required: " ",
				email: "Veuillez entrer une adresse email valide, par example: votreprenom@adressesite.fr",
				remote: jQuery.format("{0} est déjà utilisé comme identifiant Mondomix Music.")	
			}
			,pro_password:{
        required: "Veuillez choisir un mot de passe",
        password: "Votre mot de passe doit être long d'au moins 6 caractères et contenir au moins un chiffre"
      }
			,fld_captcha:{
      required : "Veuillez recopier les lettres et chiffres ci-contre.",
      remote : jQuery.format("{0} ne correspond pas au captcha.")	
      }
			,pro_name:{
      required : "Champ obligatoire",
      }  
			,pro_firstname:{
      required : "Champ obligatoire",
      }   
			,pro_datebirth:{
      required : "Champ obligatoire",
      }      
      
		}
	});
	

  // masque de saisie de certain champs  
  $("input#pro_datebirth").mask("99/99/9999");
  //$("input#usr_codepostal").mask("99999");

	//regénérer captcha 
  $("#refreshimg").click(function(){
		$.post('./includes/captcha/newsession.php');
		$("#captcha-image").load('./includes/captcha/image_req.php');
		$("#fld_captcha").val("");//on vide le champ
		//return false;
	});

	

});//eo.$.ready()

