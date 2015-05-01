$(document).ready(function () {
  // $("#is_agree").on("click", function () {
  //   if ($(this).is(":checked")) {
  //       $("#btn_submit").removeAttr("disabled");
  //       $("#btn_demo").removeAttr("disabled");
  //       $(this).parent().css("color","black");
  //   } else {
  //       $("#btn_submit").attr("disabled", "disabled");
  //       $("#btn_demo").attr("disabled", "disabled");
  //       $(this).parent().css("color","red");
  //   }
  // });
  $("#warn_500, #warn_1000").css("display", "none");

  $("#sequence").on("keyup", function () {
    $("#count").text($(this).val().length);
    if ($(this).val().length < 60) {
        $("#count").parent().parent().css({"color":"red", "background-color":"white"});
        $("#warn_500, #warn_1000").css("display", "none");
    } else {
        $("#count").parent().parent().css({"color":"black", "background-color":"white"});
        if ($(this).val().length > 500) {
          if ($(this).val().length > 1000) {
            $("#count").parent().parent().css({"color":"red", "background-color":"black"});
            $("#warn_1000").css("display", "inline-block");
            $("#warn_500").css("display", "none");
          } else {
            $("#count").parent().parent().css({"color":"orange", "background-color":"black"});
            $("#warn_500").css("display", "inline-block");
            $("#warn_1000").css("display", "none");
          }
        } else {
          $("#warn_500, #warn_1000").css("display", "none");
        }
    }
  });

  $("#check_num_primers").on("click", function () {
    if ($(this).is(":checked")) {
        $("#text_num_primers").removeAttr("disabled");
    } else {
        $("#text_num_primers").attr("disabled", "disabled");
    }
  });

  $("#btn_submit").on("click", function () {
    var job_id = Math.random().toString(16).substring(2, 15) + Math.random().toString(16).substring(2, 15);
    $("#job_id").val(job_id.toString());
    $("#modal_id").text(job_id.toString());
    $("#url_id").text('http://primerize.stanford.edu/result?job_id='.concat(job_id.toString()));

    $("#modal_wait").modal("show");
    $("#wait").fadeIn(1000);
  });
  $("#btn_demo").on("click", function () {
    $("#wait").fadeIn(1000);
  });
  
});