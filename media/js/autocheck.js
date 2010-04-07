

function txn_autocheck(){
  $("#msg_txn").remove();
  var aa = setTimeout("txn_autocheck()",5000);//check toute les 5 sec.

/**/
  $.ajax({
  type: "POST",
  url: "./includes/ajax.lib.php",
  data: "p=jax_txn_check",
  dataType:"json",
  
  success: function(msg){
  
    var sp = document.createElement("div");
    $(sp).attr({style:"position:absolute;background:white;width:300px;height:30px;" , id:"msg_txn"});
    $(sp).html('Status : ' + msg.pp_payment_status + '<br># Transaction : ' + msg.pp_txn_id);
    $("#box-panier").after($(sp));
    if(msg.pp_payment_status =="Completed"){
      clearTimeout(aa); 
      $("#txn-en-cours, #box-checkout-panier, #box-moyens-paiements").remove();// on cache
      }
  
  }//fct$$success
  });//eo.ajax

  
}///eo.func
