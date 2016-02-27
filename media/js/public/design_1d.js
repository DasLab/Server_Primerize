var ajax_timeout;

function track_input_length() {
  var val = $("#id_sequence").val().match(/[ACGTUacgtu\ \n]+/g);
  if (val) { $("#id_sequence").val(val.join('')); }
  var l = $("#id_sequence").val().length;

  $("#count").text(l);
  if (l < 60) {
      $("#count").parent().parent().css("color", "#ff5c2b");
      $("#warn_500, #warn_1000").css("display", "none");
      $("#btn_submit").prop("disabled", false);
  } else {
      $("#count").parent().parent().css("color", "#29be92");
      if (l > 500) {
        if (l > 1000) {
          $("#count").parent().parent().css("color", "#ff5c2b");
          $("#warn_1000").css("display", "inline-block");
          $("#warn_500").css("display", "none");
          $("#btn_submit").prop("disabled", true);
        } else {
          $("#count").parent().parent().css("color", "#ff912e");
          $("#warn_500").css("display", "inline-block");
          $("#warn_1000").css("display", "none");
          $("#btn_submit").prop("disabled", false);
        }
      } else {
        $("#warn_500, #warn_1000").css("display", "none");
      }
  }
}

function ajax_load_html(job_id) {
  $.ajax({
    url: '/site_data/1d/result_' + job_id + '.html',
    cache: false,
    dataType: "html",
    success: function(data) { $("#result").html(data); }
  });
} 

function ajax_update_result(data) {
  clearInterval(ajax_timeout);
  if (data.error) {
    html = '<br/><hr/><div class="container theme-showcase"><h2>Output Result:</h2><div class="alert alert-danger"><p><span class="glyphicon glyphicon-remove-sign"></span>&nbsp;&nbsp;<b>ERROR</b>: ' + data.error + '</p></div>';
    $("#result").html(html);
  } else {
    $("#result").load('/site_data/1d/result_' + data.job_id + '.html');

    var interval = Math.max($("#id_sequence").val().length * 4, 1000);
    $("#id_sequence").val(data.sequence);
    $("#id_tag").val(data.tag);
    $("#id_min_Tm").val(data.min_Tm);
    $("#id_max_len").val(data.max_len);
    $("#id_min_len").val(data.min_len);
    $("#id_num_primers").val(data.num_primers);
    $("#id_is_num_primers").prop("checked", data.is_num_primers);
    $("#id_is_check_t7").prop("checked", data.is_check_t7);

    track_input_length();

    ajax_timeout = setInterval(function() {
      ajax_load_html(data.job_id);
      if ($("#result").html().indexOf("Primerize is running") == -1) {
        clearInterval(ajax_timeout);
        if (window.history.replaceState) {
          window.history.replaceState({} , '', '/result/?job_id=' + data.job_id);
        } else {
          window.location.href = '/result/?job_id=' + data.job_id;
        }
      }
    }, interval);
  }
}

$(document).ready(function () {
  $("#warn_500, #warn_1000").css("display", "none");

  track_input_length();
  $("#id_sequence").on("keyup", track_input_length);
  $("#id_tag").on("keyup", function () {
    var val = $(this).val().match(/[a-zA-Z0-9\ \.\-\_]+/g);
    if (val) { $(this).val(val.join('')); }
  });

  if ($("#id_is_num_primers").is(":checked")) {
      $("#id_num_primers").removeAttr("disabled");
  } else {
      $("#id_num_primers").attr("disabled", "disabled");
  }
  $("#id_is_num_primers").on("click", function () {
    if ($(this).is(":checked")) {
        $("#id_num_primers").removeAttr("disabled");
    } else {
        $("#id_num_primers").attr("disabled", "disabled");
    }
  });

  $("#form_1d").submit(function(event) {
    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: $(this).serialize(),
      success: function(data) { ajax_update_result(data); },
    });
    event.preventDefault();
  });
  $("#btn_demo").on("click", function(event) {
    $.ajax({
      type: "GET",
      url: $(this).attr("href"),
      success: function(data) { ajax_update_result(data); },
    });
    event.preventDefault();
  });
  
});



