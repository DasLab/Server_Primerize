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

  $("#sequence").on("keyup", function () {
    $("#count").text($(this).val().length);
    if ($(this).val().length < 60) {
        $("#count").parent().parent().css("color","red");
    } else {
        $("#count").parent().parent().css("color","black");
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

    $("#modal_wait").modal("show");
    $("#wait").fadeIn(1000);
  });
  $("#btn_demo").on("click", function () {
    $("#wait").fadeIn(1000);
  });
  
});