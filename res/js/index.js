$(document).ready(function () {

  var col_h = Math.max(parseInt($("#col-1").css("height")), parseInt($("#col-2").css("height")), parseInt($("#col-3").css("height")), parseInt($("#col-4").css("height")));
  $("#col-1").css("height", col_h);
  $("#col-2").css("height", col_h);
  $("#col-3").css("height", col_h);
  $("#col-4").css("height", col_h);

  $("#btn_retrieve").on("click", function () { $("#wait").fadeIn(1000); });
  $("#btn_demo").on("click", function () { $("#modal_demo").modal("show"); });
  
});



