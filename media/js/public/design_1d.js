
function show_modal() {
  var job_id = random_id(16);
  $("#job_id").val(job_id.toString());
  $("#modal_id").text(job_id.toString());
  $("#url_id").text('http://primerize.stanford.edu/result?job_id='.concat(job_id.toString()));
  $("#copy-button").attr("data-clipboard-text", $("#url_id").text());

  // $("#wait").fadeIn(1000);
  $("#modal_wait").modal("show");

  $("#modal_warn_500").css("display", $("#warn_500").css("display"));
  $("#modal_warn_1000").css("display", $("#warn_1000").css("display"));
}

function track_input_length() {
  var l = $("#id_sequence").val().length;

  $("#count").text(l);
  if (l < 60) {
      $("#count").parent().parent().css({"color":"red", "background-color":"white"});
      $("#warn_500, #warn_1000").css("display", "none");
  } else {
      $("#count").parent().parent().css({"color":"black", "background-color":"white"});
      if (l > 500) {
        if (l > 1000) {
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
}

$(document).ready(function () {
  $("#id_tag").attr("placeholder", "Enter a tag").addClass("form-control");
  $("#id_sequence").attr({"rows": 8, "cols": 100, "placeholder": "Enter a sequence"}).addClass("form-control");
  $("#id_min_Tm").addClass("form-control");
  $("#id_max_len").addClass("form-control");
  $("#id_min_len").addClass("form-control");
  $("#id_num_primers").addClass("form-control");


  $("#warn_500, #warn_1000").css("display", "none");
  track_input_length();
  $("#id_sequence").on("keyup", function () { track_input_length(); });
  if (!$("id_is_num_primers").is(":checked")) { $("#id_num_primers").attr("disabled", "disabled"); }

  $("#id_is_num_primers").on("click", function () {
    if ($(this).is(":checked")) {
        $("#id_num_primers").removeAttr("disabled");
    } else {
        $("#id_num_primers").attr("disabled", "disabled");
    }
  });

  if (navigator.userAgent.indexOf("Chrome") > -1 | navigator.userAgent.indexOf("Firefox") > -1) {
    $("#btn_submit").on("click", function () { show_modal(); });
    $("#btn_demo").on("click", function () { $("#modal_demo").modal("show"); });
  } else {
    // stupid safari!!
    // console.log("safari");
    $("#btn_submit").on("click", function () { 
      event.preventDefault();
      show_modal();
      setTimeout(function(){ $("#form").trigger("submit"); }, 0);
    });
    $("#btn_demo").on("click", function () { 
      event.preventDefault();
      show_modal(); 
      setTimeout(function(){ location.href = "/demo_P4P6"; }, 0);
    });
  } 
  
});



