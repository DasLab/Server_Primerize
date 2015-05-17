$(document).ready(function () {
  $("#calc_DNA").on('click', function () { 
  	var A260 = $("#A260").val(),
  		l = $("#lbp").val();
  	$("#conc_DNA").val(parseFloat(A260) * 50000 / 660 / parseInt(l) );
  });
  $("#clc_DNA").on('click', function () {
  	$("#A260").val('');
  	$("#lbp").val('');
  	$("#conc_DNA").val('');
  });

});

