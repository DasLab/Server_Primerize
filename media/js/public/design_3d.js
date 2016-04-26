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
    var l = $(this).val().length;
    $(this).next().children().children().children().text(l);

    var val = $(this).val().match(/[ACGTUacgtu]+/g);
    if (val) { $(this).val(val.join('')); }
    value += $(this).val() + ',';
  });
  value = value.substring(0, value.length - 1);
  $("#id_primers").val(value);
}


function track_structure_list() {
  var value = '';
  $("input.structure_input").each(function () {
    var l = $(this).val().length;
    $(this).next().children().children().children().text(l);

    var val = $(this).val().match(/[\.\(\)\[\]]+/g);
    if (val) { $(this).val(val.join('')); }
    value += $(this).val() + ',';
  });
  value = value.substring(0, value.length - 1);
  $("#id_structures").val(value);
}


function track_input_length() {
  var val = $("#id_sequence").val().match(/[ACGTUacgtu\ \n]+/g);
  if (val) { $("#id_sequence").val(val.join('')); }
  var l = $("#id_sequence").val().length;

  $("#count").text(l);
  if (l < 60) {
      $("#count").parent().parent().css("color", "#ff5c2b");
  } else {
      $("#count").parent().parent().css("color", "#29be92");
      if (l > 500) {
        if (l > 1000) {
          $("#count").parent().parent().css("color", "#ff5c2b");
        } else {
          $("#count").parent().parent().css("color", "#ff912e");
        }
      }
  }
}

function ajax_load_html(job_id) {
  $.ajax({
    url: '/site_data/3d/result_' + job_id + '.html',
    cache: false,
    dataType: "html",
    success: function(data) {
      $("#result").html(data);
      if ($("#result").html().indexOf("alert-danger") == -1) {
        draw_96_plate(job_id, 3);
      }
    }
  });
}

function ajax_update_result(data) {
  clearInterval(ajax_timeout);
  if (data.error) {
    html = '<br/><hr/><div class="container theme-showcase"><h2>Output Result:</h2><div class="alert alert-danger"><p><span class="glyphicon glyphicon-remove-sign"></span>&nbsp;&nbsp;<b>ERROR</b>: ' + data.error + '</p></div>';
    $("#result").html(html);
  } else {
    $("#result").load('/site_data/3d/result_' + data.job_id + '.html');

    var interval = Math.max($("#id_sequence").val().length * 4, 1000);
    $("#id_sequence").val(data.sequence);
    $("#id_tag").val(data.tag);
    $("#id_offset").val(data.offset);
    $("#id_min_muts").val(data.min_muts);
    $("#id_max_muts").val(data.max_muts);
    $("#id_lib").val(data.lib);
    $("#id_num_mutations").val(data.num_mutations);
    $("#id_is_single").prop("checked", data.is_single);
    $("#id_is_fill_WT").prop("checked", data.is_fill_WT);

    sync_structure_input(data.structures);
    sync_primer_input(data.primers);
    track_input_length();
    track_structure_list();
    track_primer_list();

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

function sync_primer_input(data) {
  var idx = $("#primer_sets").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  }
  if (data.length > idx) {
    for (var i = 0; i < Math.ceil((data.length - idx) / 2); i++) {
      expand_primer_input();
    }
  }
  var idx = $("#primer_sets").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  }
  for (var i = 0; i < idx; i++) {
    if (i < data.length) {
      $("#id_primer_" + (i + 1).toString()).val(data[i]);
    } else {
      $("#id_primer_" + (i + 1).toString()).val('');
    }
  }
  track_primer_list();
}

function expand_primer_input() {
  var idx = $("#primer_sets").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  } else {
    idx = 0;
  }
  $('<div style="padding-bottom:10px;" id="primer_' + (idx + 1).toString() + '" class="input-group"><span class="input-group-addon">' + primer_label(idx + 1) + '</span><input class="primer_input form-control monospace translucent" type="text" id="id_primer_' + (idx + 1).toString() + '" name="id_primer_' + (idx + 1).toString() + '" placeholder="Enter primer ' + (idx + 1).toString() + ' sequence"/><span class="input-group-addon"><i><b><span id="count_primer_' + (idx + 1).toString() + '">0</span></b></i> nt</span></div>').appendTo($("#primer_sets"));
  $('<div style="padding-bottom:10px;" id="primer_' + (idx + 2).toString() + '" class="input-group"><span class="input-group-addon">' + primer_label(idx + 2) + '</span><input class="primer_input form-control monospace translucent" type="text" id="id_primer_' + (idx + 2).toString() + '" name="id_primer_' + (idx + 2).toString() + '" placeholder="Enter primer ' + (idx + 2).toString() + ' sequence"/><span class="input-group-addon"><i><b><span id="count_primer_' + (idx + 2).toString() + '">0</span></b></i> nt</span></div>').appendTo($("#primer_sets"));
  $("#id_primer_" + (idx + 1).toString()).on("keyup", track_primer_list);
  $("#id_primer_" + (idx + 2).toString()).on("keyup", track_primer_list);
}


function sync_structure_input(data) {
  var idx = $("#structures").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  }
  if (data.length > idx) {
    for (var i = 0; i < Math.ceil((data.length - idx) / 2); i++) {
      expand_structure_input();
    }
  }
  var idx = $("#structures").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  }
  for (var i = 0; i < idx; i++) {
    if (i < data.length) {
      $("#id_structure_" + (i + 1).toString()).val(data[i]);
    } else {
      $("#id_structure_" + (i + 1).toString()).val('');
    }
  }
  track_structure_list();
}

function expand_structure_input() {
  var idx = $("#structures").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  } else {
    idx = 0;
  }
  $('<div style="padding-bottom:10px;" id="structure_' + (idx + 1).toString() + '" class="input-group"><span class="input-group-addon"><b>' + (idx + 1).toString() + '</b></span><input class="primer_input form-control monospace translucent" type="text" id="id_structure_' + (idx + 1).toString() + '" name="id_structure_' + (idx + 1).toString() + '" placeholder="Enter secondary structure #' + (idx + 1).toString() + '"/><span class="input-group-addon"><i><b><span id="count_structure_' + (idx + 1).toString() + '">0</span></b></i> nt</span></div>').appendTo($("#structures"));
  $("#id_structure_" + (idx + 1).toString()).on("keyup", track_structure_list);
}


$(document).ready(function () {
  track_input_length();
  $("#id_sequence").on("keyup", track_input_length);
  $("#id_tag").on("keyup", function () {
    var val = $(this).val().match(/[a-zA-Z0-9\ \.\-\_]+/g);
    if (val) { $(this).val(val.join('')); }
  });

  $("input.structure_input").on("keyup", track_structure_list);
  $("input.primer_input").on("keyup", track_primer_list);
  $("#btn-add-str").on("click", expand_structure_input);
  $("#btn-add-prm").on("click", expand_primer_input);

  $("#form_3d").submit(function(event) {
    $("input.structure_input").prop("disabled", true);
    $("input.primer_input").prop("disabled", true);
    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: $(this).serialize(),
      success: function(data) { ajax_update_result(data); },
    });
    $("input.structure_input").prop("disabled", false);
    $("input.structure_input").prop("readonly", false);
    $("input.primer_input").prop("disabled", false);
    $("input.primer_input").prop("readonly", false);
    $("#id_sequence").prop("readonly", false);
    $("#btn-add-str").prop("disabled", false);
    $("#btn-add-prm").prop("disabled", false);
    event.preventDefault();
  });
  
  $("#btn_demo_1, #btn_demo_2").on("click", function(event) {
    $.ajax({
      type: "GET",
      url: $(this).attr("href") + '?mode=' + $(this).attr('id').slice(-1),
      success: function(data) { ajax_update_result(data); },
    });
    event.preventDefault();
  });
  
});



