function resize() {
  $("#col-1").css("height", "auto");
  $("#col-2").css("height", "auto");
  $("#col-3").css("height", "auto");
  $("#col-4").css("height", "auto");

  var col_h = Math.max(parseInt($("#col-1").css("height")), parseInt($("#col-2").css("height")), parseInt($("#col-3").css("height")), parseInt($("#col-4").css("height")));
  $("#col-1").css("height", col_h);
  $("#col-2").css("height", col_h);
  $("#col-3").css("height", col_h);
  $("#col-4").css("height", col_h);
}


$(document).ready(function () {
  setTimeout(resize, 200);

  $("#btn_retrieve").on("click", function () { $("#wait").fadeIn(1000); });
  $("#btn_retrieve").prop("disabled", true);
  $("#input_job_id").on("keyup", function () {
    var val = $(this).val().match(/^([a-fA-F0-9]){0,16}/g);
    if (val) { $(this).val(val.join('')); }
    if ($(this).val().length == 16) {
		$("#btn_retrieve").prop("disabled", false);
    } else {
		$("#btn_retrieve").prop("disabled", true);
    }
  });
});


$(window).on("resize", function() {
  clearTimeout($.data(this, 'resizeTimer'));
  $.data(this, 'resizeTimer', setTimeout(resize(), 200));
});



