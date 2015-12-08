var ajax_timeout;

function primer_label(num) {
  if (num % 2) {
    return '<b>' + num + '</b> <span class="label label-info">F</span>';
  } else {
    return '<b>' + num + '</b> <span class="label label-danger">R</span>';
  }
}

function track_primer_list() {
  var value = '';
  $("input.primer_input").each(function () {
    var val = $(this).val().match(/[ACGTUacgtu\ ]+/g);
    if (val) { $(this).val(val.join('')); }
    value += $(this).val() + ',';
  });
  value = value.substring(0, value.length - 1);
  $("#id_primers").val(value);
}


function track_input_length() {
  var val = $("#id_sequence").val().match(/[ACGTUacgtu\ \n]+/g);
  if (val) { $("#id_sequence").val(val.join('')); }
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

function ajax_load_html(job_id) {
  $.ajax({
      url: '/site_data/2d/result_' + job_id + '.html',
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
    $("#result").load('/site_data/2d/result_' + data.job_id + '.html');

    var interval = Math.max($("#id_sequence").val().length * 4, 1000);
    $("#id_sequence").val(data.sequence);
    $("#id_tag").val(data.tag);
    $("#id_offset").val(data.offset);
    $("#id_min_muts").val(data.min_muts);
    $("#id_max_muts").val(data.max_muts);
    $("#id_lib").val(data.lib);

    var idx = $("#primer_sets").children().last().attr("id");
    if (idx) {
      idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
    }
    if (data.primers.length > idx) {
      for (var i = 0; i < Math.ceil((data.primers.length - idx) / 2); i++) {
        $("#btn-add").trigger("click");
      }
    }
    var idx = $("#primer_sets").children().last().attr("id");
    if (idx) {
      idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
    }
    for (var i = 0; i < idx; i++) {
      if (i < data.primers.length) {
        $("#id_primer_" + (i + 1).toString()).val(data.primers[i]);
      } else {
        $("#id_primer_" + (i + 1).toString()).val('');
      }
    }

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
  $("#id_tag").attr("placeholder", "Enter a tag").addClass("form-control");
  $("#id_sequence").attr({"rows": 12, "cols": 50, "placeholder": "Enter a sequence"}).addClass("form-control");
  $("#id_primers").attr({"rows": 12, "cols": 50, "placeholder": "Enter the primer set"}).css("display", "none");
  $("#id_offset").addClass("form-control");
  $("#id_min_muts").addClass("form-control").css("width", parseInt($("#id_offset").css("width")) - parseInt($("#id_min_muts").next().css("width")));
  $("#id_max_muts").addClass("form-control").css("width", parseInt($("#id_offset").css("width")) - parseInt($("#id_max_muts").next().css("width")));
  $("#id_lib").addClass("form-control").css("width", parseInt($("#id_offset").css("width")) + parseInt($("#id_max_muts").next().css("width")));


  $("#warn_500, #warn_1000").css("display", "none");
  track_input_length();
  $("#id_sequence").on("keyup", function () { track_input_length(); });
  $("#id_tag").on("keyup", function () {
    var val = $(this).val().match(/[a-zA-Z0-9\ \.\-\_]+/g);
    if (val) { $(this).val(val.join('')); }
  });

  $("input.primer_input").on("keyup", track_primer_list);
  $("#btn-add").on("click", function () {
    var idx = $("#primer_sets").children().last().attr("id");
    if (idx) {
      idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
    } else {
      idx = 0;
    }
    $('<div style="padding-bottom:10px;" id="primer_' + (idx + 1).toString() + '" class="input-group"><span class="input-group-addon">' + primer_label(idx + 1) + '</span><input class="primer_input form-control" type="text" id="id_primer_' + (idx + 1).toString() + '" name="id_primer_' + (idx + 1).toString() + '"/></div>').appendTo($("#primer_sets"));
    $('<div style="padding-bottom:10px;" id="primer_' + (idx + 2).toString() + '" class="input-group"><span class="input-group-addon">' + primer_label(idx + 2) + '</span><input class="primer_input form-control" type="text" id="id_primer_' + (idx + 2).toString() + '" name="id_primer_' + (idx + 2).toString() + '"/></div>').appendTo($("#primer_sets"));
    $("#id_primer_" + (idx + 1).toString()).on("keyup", track_primer_list);
    $("#id_primer_" + (idx + 2).toString()).on("keyup", track_primer_list);
  });

  $("#form_2d").submit(function(event) {
    $("input.primer_input").prop("disabled", true);
    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: $(this).serialize(),
      success: function(data) { ajax_update_result(data); },
    });
    $("input.primer_input").prop("disabled", false);
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



