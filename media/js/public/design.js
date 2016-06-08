var ajax_timeout, hover_timeout;

app.fnPrimerize.primerLabel = function(num) {
  if (num % 2) {
    return '<b>' + num + '</b> <span class="label label-info">F</span>';
  } else {
    return '<b>' + num + '</b> <span class="label label-danger">R</span>';
  }
};

app.fnPrimerize.ajaxLoadHTML = function() {
  $.ajax({
    url: '/site_data/' + app.fnPrimerize.job_type + 'd/result_' + app.fnPrimerize.job_id + '.html',
    cache: false,
    dataType: "html",
    success: function(data) {
      $("#result").html(data);

      if (app.fnPrimerize.job_type !== 1) {
        if ($("#result").html().indexOf("alert-danger") == -1) {
          draw_96_plate(app.fnPrimerize.job_id, app.fnPrimerize.job_type);
        }
        if (app.fnPrimerize.job_type === 3) {
          $("span[class^='seqpos_']").hover(function() {
            var cls = $(this).attr("class");
            clearTimeout(hover_timeout);
            hover_timeout = setTimeout(function() { $("span." + cls + ", circle." + cls).addClass("active"); }, 50);
          }, function() {
            clearTimeout(hover_timeout);
            $("span[class^='seqpos_'].active, circle[class^='seqpos_'].active").removeClass("active");
          });
        }
      } else {

      }
    }
  });
};

app.fnPrimerize.ajaxRefresh = function() {
  var interval = Math.max($("#id_sequence").val().length * 4, 1500);

  ajax_timeout = setInterval(function() {
    app.fnPrimerize.ajaxLoadHTML();
    if ($("#result").html().indexOf("Primerize is running") == -1) {
      clearInterval(ajax_timeout);
      if (window.history.replaceState) {
        window.history.replaceState({} , '', '/result/?job_id=' + app.fnPrimerize.job_id);
      } else {
        window.location.href = '/result/?job_id=' + app.fnPrimerize.job_id;
      }
    }
  }, interval);
};

app.fnPrimerize.ajaxUpdateResult = function(data) {
  app.fnPrimerize.job_id = data.job_id;
  clearInterval(ajax_timeout);

  if (data.error) {
    html = '<br/><hr/><div class="container theme-showcase"><h2>Output Result:</h2><div class="alert alert-danger"><p><span class="glyphicon glyphicon-remove-sign"></span>&nbsp;&nbsp;<b>ERROR</b>: ' + data.error + '</p></div>';
    $("#result").html(html);
  } else {
    $("#result").load('/site_data/' + app.fnPrimerize.job_type + 'd/result_' + data.job_id + '.html');

    $("#id_sequence").val(data.sequence);
    $("#id_tag").val(data.tag);
    if (app.fnPrimerize.job_type === 1) {
      $("#id_min_Tm").val(data.min_Tm);
      $("#id_max_len").val(data.max_len);
      $("#id_min_len").val(data.min_len);
      $("#id_num_primers").val(data.num_primers);
      $("#id_is_num_primers").prop("checked", data.is_num_primers);
      $("#id_is_check_t7").prop("checked", data.is_check_t7);
    } else {
      $("#id_offset").val(data.offset);
      $("#id_min_muts").val(data.min_muts);
      $("#id_max_muts").val(data.max_muts);
      $("#id_lib").val(data.lib);
      if (app.fnPrimerize.job_type === 3) {
        $("#id_num_mutations").val(data.num_mutations);
        $("#id_is_single").prop("checked", data.is_single);
        $("#id_is_fill_WT").prop("checked", data.is_fill_WT);
        app.fnPrimerize.syncStructureInput(data.structures);
        app.fnPrimerize.trackStructureList();
      }

      app.fnPrimerize.syncPrimerInput(data.primers);
      app.fnPrimerize.trackInputLength();
      app.fnPrimerize.trackPrimerList();
    }

    app.fnPrimerize.ajaxRefresh();
  }
};


app.fnPrimerize.trackPrimerList = function() {
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
};

app.fnPrimerize.trackInputLength = function() {
  var val = $("#id_sequence").val().match(/[ACGTUacgtu\ \n]+/g);
  if (val) { $("#id_sequence").val(val.join('')); }
  var l = $("#id_sequence").val().length;

  $("#count").text(l);
  if (l < 60) {
    $("#count").parent().parent().css("color", "#ff5c2b");
    if (app.page == "design_1d") {
      $("#warn_500, #warn_1000").css("display", "none");
      $("#btn_submit").prop("disabled", false);
    }
  } else {
    $("#count").parent().parent().css("color", "#29be92");
    if (l > 500) {
      if (l > 1000) {
        $("#count").parent().parent().css("color", "#ff5c2b");
        if (app.page == "design_1d") {
          $("#warn_1000").css("display", "inline-block");
          $("#warn_500").css("display", "none");
          $("#btn_submit").prop("disabled", true);
        }
      } else {
        $("#count").parent().parent().css("color", "#ff912e");
        if (app.page == "design_1d") {
          $("#warn_500").css("display", "inline-block");
          $("#warn_1000").css("display", "none");
          $("#btn_submit").prop("disabled", false);
        }
      }
    } else {
      if (app.page == "design_1d") { $("#warn_500, #warn_1000").css("display", "none"); }
    }
  }
};

app.fnPrimerize.syncPrimerInput = function(data) {
  var idx = $("#primer_sets").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  }
  if (data.length > idx) {
    for (var i = 0; i < Math.ceil((data.length - idx) / 2); i++) {
      app.fnPrimerize.expandPrimerInput();
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
  app.fnPrimerize.trackPrimerList();
};

app.fnPrimerize.expandPrimerInput = function() {
  var idx = $("#primer_sets").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  } else {
    idx = 0;
  }
  $('<div style="padding-bottom:10px;" id="primer_' + (idx + 1).toString() + '" class="input-group"><span class="input-group-addon">' + app.fnPrimerize.primerLabel(idx + 1) + '</span><input class="primer_input form-control monospace translucent" type="text" id="id_primer_' + (idx + 1).toString() + '" name="id_primer_' + (idx + 1).toString() + '" placeholder="Enter primer ' + (idx + 1).toString() + ' sequence"/><span class="input-group-addon"><i><b><span id="count_primer_' + (idx + 1).toString() + '">0</span></b></i> nt</span></div>').appendTo($("#primer_sets"));
  $('<div style="padding-bottom:10px;" id="primer_' + (idx + 2).toString() + '" class="input-group"><span class="input-group-addon">' + app.fnPrimerize.primerLabel(idx + 2) + '</span><input class="primer_input form-control monospace translucent" type="text" id="id_primer_' + (idx + 2).toString() + '" name="id_primer_' + (idx + 2).toString() + '" placeholder="Enter primer ' + (idx + 2).toString() + ' sequence"/><span class="input-group-addon"><i><b><span id="count_primer_' + (idx + 2).toString() + '">0</span></b></i> nt</span></div>').appendTo($("#primer_sets"));
  $("#id_primer_" + (idx + 1).toString()).on("keyup", app.fnPrimerize.trackPrimerList);
  $("#id_primer_" + (idx + 2).toString()).on("keyup", app.fnPrimerize.trackPrimerList);
};


app.fnPrimerize.trackStructureList = function() {
  var value = '';
  $("textarea.structure_input").each(function () {
    var l = $(this).val().length;
    var l_label = $(this).next().children().last().children().children();
    l_label.text(l);
    if (l !== $("#id_sequence").val().length) {
      l_label.css("color", "#ff5c2b");
    } else {
      l_label.css("color", "#29be92");
    }

    var val = $(this).val().match(/[\.\(\)\[\]]+/g);
    if (val) { $(this).val(val.join('')); }
    value += $(this).val() + ',';
  });
  value = value.substring(0, value.length - 1);
  $("#id_structures").val(value);
};

app.fnPrimerize.syncStructureInput = function(data) {
  var idx = $("#structures").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  }
  if (data.length > idx) {
    for (var i = 0; i < data.length - idx; i++) {
      app.fnPrimerize.expandStructureInput();
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
  app.fnPrimerize.trackStructureList();
};

app.fnPrimerize.expandStructureInput = function() {
  var idx = $("#structures").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  } else {
    idx = 0;
  }
  $('<div style="padding-bottom:10px;" id="structure_' + (idx + 1).toString() + '"><textarea class="structure_input form-control monospace translucent textarea-group" type="text" rows="4" cols="50" id="id_structure_' + (idx + 1).toString() + '" name="id_structure_' + (idx + 1).toString() + '" placeholder="Enter secondary structure #' + (idx + 1).toString() + '"></textarea><div class="list-group-item disabled" style="padding:6px 12px; color:#555; border-color:#ccc; background-color:#eee; border-top:0px; height:32px;"><p class="pull-left" style="margin:0px;"><b><span class="label label-success">SecStr</span> ' + (idx + 1).toString() + '</b></p><p class="pull-right" style="margin:0px;">Length: <i><b><span id="count_structure_' + (idx + 1).toString() + '">0</span></b></i> nt</p></div>').appendTo($("#structures"));
  $("#id_structure_" + (idx + 1).toString()).on("keyup", app.fnPrimerize.trackStructureList);
};


app.fnPrimerize.onLoad = function() {
  app.fnPrimerize.trackInputLength();
  $("#id_sequence").on("keyup", app.fnPrimerize.trackInputLength);
  $("#id_tag").on("keyup", function () {
    var val = $(this).val().match(/[a-zA-Z0-9\ \.\-\_]+/g);
    if (val) { $(this).val(val.join('')); }
  });

  if (app.page == "design_2d" || app.page == "design_3d") {
    $("input.primer_input").on("keyup", app.fnPrimerize.trackPrimerList);
    $("#btn-add-prm").on("click", app.fnPrimerize.expandPrimerInput);

    if (app.page == "design_2d") {
      $("#form_2d").submit(function(event) {
        $("input.primer_input").prop("disabled", true);
        $.ajax({
          type: "POST",
          url: $(this).attr("action"),
          data: $(this).serialize(),
          success: function(data) {
            app.fnPrimerize.job_type = 2;
            app.fnPrimerize.ajaxUpdateResult(data);
          },
        });
        $("input.primer_input").prop("disabled", false);
        $("input.primer_input").prop("readonly", false);
        $("#id_sequence").prop("readonly", false);
        $("#btn-add-prm").prop("disabled", false);
        event.preventDefault();
      });

      $("#btn_demo").on("click", function(event) {
        $.ajax({
          type: "GET",
          url: $(this).attr("href"),
          success: function(data) {
            app.fnPrimerize.job_type = 2;
            app.fnPrimerize.ajaxUpdateResult(data);
          },
        });
        event.preventDefault();
      });
    } else {
      $("textarea.structure_input").on("keyup", app.fnPrimerize.trackStructureList);
      $("#btn-add-str").on("click", app.fnPrimerize.expandStructureInput);

      $("#form_3d").submit(function(event) {
        $("textarea.structure_input").prop("disabled", true);
        $("input.primer_input").prop("disabled", true);
        $.ajax({
          type: "POST",
          url: $(this).attr("action"),
          data: $(this).serialize(),
          success: function(data) {
            app.fnPrimerize.job_type = 3;
            app.fnPrimerize.ajaxUpdateResult(data);
          }
        });
        $("textarea.structure_input").prop("disabled", false);
        $("textarea.structure_input").prop("readonly", false);
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
          success: function(data) {
            app.fnPrimerize.job_type = 3;
            app.fnPrimerize.ajaxUpdateResult(data);
          },
        });
        event.preventDefault();
      });
    }

  } else {
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
        success: function(data) {
          app.fnPrimerize.job_type = 1;
          app.fnPrimerize.ajaxUpdateResult(data);
        },
      });
      event.preventDefault();
    });
    $("#btn_demo").on("click", function(event) {
      $.ajax({
        type: "GET",
        url: $(this).attr("href"),
        success: function(data) {
          app.fnPrimerize.job_type = 1;
          app.fnPrimerize.ajaxUpdateResult(data);
        },
      });
      event.preventDefault();
    });

  }
};

app.isLoaded = true;
