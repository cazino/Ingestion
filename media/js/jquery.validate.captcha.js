$(function(){
	$("#refreshimg").click(function(){
		$.post('./_includes/captcha/newsession.php');
		$("#captchaimage").load('./_includes/captcha/image_req.php');
		return false;
	});

	$("#captchaform").validate({
		rules: {
			captcha: {
				required: true,
				remote: "./_includes/captcha/process.php"
			}
		},
		messages: {
			captcha: "Correct captcha is required. Click the captcha to generate a new one"	
		},
		submitHandler: function() {
			alert("Correct captcha!");
		},

		success: function(label) {
			label.addClass("valid").text("Valid captcha!")
		},
		onkeyup: false
	});
});
