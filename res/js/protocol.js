$(document).ready(function () {
  $("#calc_DNA").on('click', function () { 
  	var A260 = $("#A260_DNA").val(),
  		l = $("#l_DNA").val();
  	$("#conc_DNA").val(parseFloat(A260) * 50000 / 660 / parseInt(l) );
  });
  $("#clc_DNA").on('click', function () {
  	$("#A260_DNA").val('');
  	$("#l_DNA").val('');
  	$("#conc_DNA").val('');
  });

  $("#calc_RNA").on('click', function () { 
  	var A260 = $("#A260_RNA").val(),
  		l = $("#l_RNA").val();
  	$("#conc_RNA").val(parseFloat(A260) * 40000 / 330 / parseInt(l) );
  });
  $("#clc_RNA").on('click', function () {
  	$("#A260_RNA").val('');
  	$("#l_RNA").val('');
  	$("#conc_RNA").val('');
  });

});

