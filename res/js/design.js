$(document).ready(function () {
  $("#is_agree").click(function() {
    if ($(this).is(":checked")) {
        $("#btn_submit").removeAttr("disabled");
        $("#btn_demo").removeAttr("disabled");
        $(this).parent().css("color","black");
    } else {
        $("#btn_submit").attr("disabled", "disabled");
        $("#btn_demo").attr("disabled", "disabled");
        $(this).parent().css("color","red");
    }
  });

  $("#sequence").keyup(function(){
    $("#count").text($(this).val().length);
    if ($(this).val().length < 60) {
        $("#count").parent().parent().css("color","red");
    } else {
        $("#count").parent().parent().css("color","black");
    }
  });

  $("#check_num_primers").click(function() {
    if ($(this).is(":checked")) {
        $("#text_num_primers").removeAttr("disabled");
    } else {
        $("#text_num_primers").attr("disabled", "disabled");
    }
  });

  $("#btn_submit").click(function() {
    $("#wait").show();   
  });
  $("#btn_demo").click(function() {
    $("#wait").show();   
  });
});