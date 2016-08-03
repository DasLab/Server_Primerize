var ajax_timeout, hover_timeout;

app.modPrimerize.fnPrimerLabel = function(num) {
  if (num % 2) {
    return '<b>' + num + '</b> <span class="label label-info">F</span>';
  } else {
    return '<b>' + num + '</b> <span class="label label-danger">R</span>';
  }
};


app.modPrimerize.fnUpdateFields = function(data) {
  $("#id_sequence").val(data.data.sequence);
  $("#id_tag").val(data.data.tag);
  if (app.modPrimerize.job_type === 1) {
    $("#id_min_Tm").val(data.data.params.min_Tm);
    $("#id_max_len").val(data.data.params.max_len);
    $("#id_min_len").val(data.data.params.min_len);
    $("#id_num_primers").val(data.data.params.num_primers);
    $("#id_is_num_primers").prop("checked", data.data.params.is_num_primers);
    $("#id_is_check_t7").prop("checked", data.data.params.is_check_t7);
  } else {
    $("#id_offset").val(data.data.params.offset);
    $("#id_min_muts").val(data.data.params.min_muts);
    $("#id_max_muts").val(data.data.params.max_muts);
    $("#id_lib").val(data.data.params.which_lib[0]);
    if (app.modPrimerize.job_type === 3) {
      $("#id_num_mutations").val(data.data.params.num_mutations);
      $("#id_is_single").prop("checked", data.data.params.is_single);
      $("#id_is_fill_WT").prop("checked", data.data.params.is_fill_WT);
      app.modPrimerize.fnSyncStructureInput(data.data.structures);
      app.modPrimerize.fnTrackStructureList();
    }

    app.modPrimerize.fnSyncPrimerInput(data.data.primers);
    app.modPrimerize.fnTrackInputLength();
    app.modPrimerize.fnTrackPrimerList();
  }
};

app.modPrimerize.fnAjaxLoadHTML = function() {
  if (typeof app.modPrimerize.job_id === "undefined") { return; }
  $.ajax({
    url: '/site_data/' + app.modPrimerize.job_type + 'd/result_' + app.modPrimerize.job_id + '.html',
    cache: false,
    dataType: "html",
    success: function(data) {
      $("#result").html(data);
      $("#btn-result-to-protocol").on("click", function(event) {
        event.preventDefault();
        app.href = $(this).attr("href");
        $("#content").fadeTo(100, 0, app.fnChangeLocation);
      });

      if (app.modPrimerize.job_type !== 1) {
        var result = $("#result").html();
        if (result.indexOf("alert-danger") == -1 && result.indexOf("Primerize is running") == -1) {
          app.mod96Plate.fnDrawResultPlates();
        }
        if (app.modPrimerize.job_type === 3) {
          $("span[class^='seqpos_']").hover(function() {
            var cls = $(this).attr("class");
            clearTimeout(hover_timeout);
            hover_timeout = setTimeout(function() { $("span." + cls + ", circle." + cls).addClass("active"); }, 50);
          }, function() {
            clearTimeout(hover_timeout);
            $("span[class^='seqpos_'].active, circle[class^='seqpos_'].active").removeClass("active");
          });
        } else {
          $("#btn-2d-to-3d").on("click", function(event) {
            event.preventDefault();
            app.href = $(this).attr("href") + "?from=" + app.modPrimerize.job_id;
            $("#content").fadeTo(100, 0, app.fnChangeLocation);
          });
        }
      } else {
        $("#btn-1d-to-3d, #btn-1d-to-2d").on("click", function(event) {
          event.preventDefault();
          app.href = $(this).attr("href") + "?from=" + app.modPrimerize.job_id;
          $("#content").fadeTo(100, 0, app.fnChangeLocation);
        });
      }
    }
  });
};

app.modPrimerize.fnAjaxRefreshResult = function() {
  var interval = Math.max($("#id_sequence").val().length * 4, 1500);

  ajax_timeout = setInterval(function() {
    var result = $("#result") ? $("#result").html(): "";
    if (typeof result !== "undefined" && result.length && result.indexOf("Primerize is running") == -1) {
      if (app.modPrimerize.job_type !== 1 && !$("#result svg").length) { app.modPrimerize.fnAjaxLoadHTML(); }
      clearInterval(ajax_timeout);
      if (window.history.pushState) {
        window.history.pushState(null , null, '/result/?job_id=' + app.modPrimerize.job_id);
      } else {
        window.location.href = '/result/?job_id=' + app.modPrimerize.job_id;
      }
      window.onpopstate = function() { location.reload(); };
    } else {
      app.modPrimerize.fnAjaxLoadHTML();
    }
  }, interval);
};

app.modPrimerize.fnAjaxSubmitJob = function(data) {
  clearInterval(ajax_timeout);
  if (data.error) {
    html = '<br/><hr/><div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><h2>Output Result:</h2></div></div><br/><div class="alert alert-danger"><p><span class="glyphicon glyphicon-remove-sign"></span>&nbsp;&nbsp;<b>ERROR</b>: ' + data.error + '</p></div>';
    $("#result").html(html);
  } else {
    app.modPrimerize.job_id = data.job_id;
    app.modPrimerize.fnUpdateFields(data);
    app.modPrimerize.fnAjaxLoadHTML();
    app.modPrimerize.fnAjaxRefreshResult();
  }
};

app.modPrimerize.fnAjaxRetrieveResult = function(job_id) {
  $.ajax({
    type: "GET",
    url: "/result/",
    data: {"job_id": job_id, "json": true},
    success: app.modPrimerize.fnOnSubmit,
    complete: app.modPrimerize.fnOnLoad
  });
};


app.modPrimerize.fnOnSubmit = function(data) {
  app.modPrimerize.job_id = undefined;
  app.modPrimerize.job_type = data.type;
  app.modPrimerize.fnAjaxSubmitJob(data);

  if (app.modPrimerize.job_type !== 1) {
    $("input.primer_input").prop("disabled", false).prop("readonly", false);
    $("#id_sequence").prop("readonly", false);
    $("#btn_add_prm").prop("disabled", false);

    if (app.modPrimerize.job_type === 3) {
      $("textarea.structure_input").prop("disabled", false).prop("readonly", false);
      $("#id_offset").prop("disabled", false).prop("readonly", false);
      $("#id_min_muts").prop("disabled", false).prop("readonly", false);
      $("#id_max_muts").prop("disabled", false).prop("readonly", false);
      $("#btn_add_str").prop("disabled", false);
    }
  }
};

app.modPrimerize.fnOnDisable = function() {
  $("#btn_submit").removeClass("btn-primary").addClass("btn-danger");
  $("#btn_submit > span.glyphicon").removeClass("glyphicon-ok-sign").addClass("glyphicon-remove-sign");
  $("#div_btns > p > button").prop("disabled", true);
  setTimeout(function() {
    $("#btn_submit").prop("disabled", false).removeClass("btn-danger").addClass("btn-primary");
    $("#btn_submit > span.glyphicon").removeClass("glyphicon-remove-sign").addClass("glyphicon-ok-sign");
    $("#div_btns > p > button").prop("disabled", false);
  }, 2500);
};


app.modPrimerize.fnTrackInputLength = function() {
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

app.modPrimerize.fnTrackPrimerList = function() {
  var value = '';
  $("input.primer_input").each(function() {
    var l = $(this).val().length;
    $(this).next().children().children().children().text(l);

    var val = $(this).val().match(/[ACGTUacgtu]+/g);
    if (val) { $(this).val(val.join('')); }
    value += $(this).val() + ',';
  });
  value = value.substring(0, value.length - 1);
  $("#id_primers").val(value);
};

app.modPrimerize.fnSyncPrimerInput = function(data) {
  var idx = $("#primer_sets").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  }
  if (data.length > idx) {
    for (var i = 0; i < Math.ceil((data.length - idx) / 2); i++) {
      app.modPrimerize.fnExpandPrimerInput();
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
  app.modPrimerize.fnTrackPrimerList();
};

app.modPrimerize.fnExpandPrimerInput = function() {
  var idx = $("#primer_sets").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  } else {
    idx = 0;
  }
  $('<div style="padding-bottom:10px;" id="primer_' + (idx + 1).toString() + '" class="input-group"><span class="input-group-addon">' + app.modPrimerize.fnPrimerLabel(idx + 1) + '</span><input class="primer_input form-control monospace translucent" type="text" id="id_primer_' + (idx + 1).toString() + '" name="id_primer_' + (idx + 1).toString() + '" placeholder="Enter primer ' + (idx + 1).toString() + ' sequence"/><span class="input-group-addon"><i><b><span id="count_primer_' + (idx + 1).toString() + '">0</span></b></i> nt</span></div>').appendTo($("#primer_sets"));
  $('<div style="padding-bottom:10px;" id="primer_' + (idx + 2).toString() + '" class="input-group"><span class="input-group-addon">' + app.modPrimerize.fnPrimerLabel(idx + 2) + '</span><input class="primer_input form-control monospace translucent" type="text" id="id_primer_' + (idx + 2).toString() + '" name="id_primer_' + (idx + 2).toString() + '" placeholder="Enter primer ' + (idx + 2).toString() + ' sequence"/><span class="input-group-addon"><i><b><span id="count_primer_' + (idx + 2).toString() + '">0</span></b></i> nt</span></div>').appendTo($("#primer_sets"));
  $("#id_primer_" + (idx + 1).toString()).on("blur", app.modPrimerize.fnTrackPrimerList);
  $("#id_primer_" + (idx + 2).toString()).on("blur", app.modPrimerize.fnTrackPrimerList);
};


app.modPrimerize.fnTrackStructureList = function() {
  var value = '';
  $("textarea.structure_input").each(function() {
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

app.modPrimerize.fnSyncStructureInput = function(data) {
  var idx = $("#structures").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  }
  if (data.length > idx) {
    for (var i = 0; i < data.length - idx; i++) {
      app.modPrimerize.fnExpandStructureInput();
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
  app.modPrimerize.fnTrackStructureList();
};

app.modPrimerize.fnExpandStructureInput = function() {
  var idx = $("#structures").children().last().attr("id");
  if (idx) {
    idx = parseInt(idx.substring(idx.indexOf('_') + 1, idx.length));
  } else {
    idx = 0;
  }
  $('<div style="padding-bottom:10px;" id="structure_' + (idx + 1).toString() + '"><textarea class="structure_input form-control monospace translucent textarea-group" type="text" rows="4" cols="50" id="id_structure_' + (idx + 1).toString() + '" name="id_structure_' + (idx + 1).toString() + '" placeholder="Enter secondary structure #' + (idx + 1).toString() + '"></textarea><div class="list-group-item disabled" style="padding:6px 12px; color:#555; border-color:#ccc; background-color:#eee; border-top:0px; height:32px;"><p class="pull-left" style="margin:0px;"><b><span class="label label-success">SecStr</span> ' + (idx + 1).toString() + '</b></p><p class="pull-right" style="margin:0px;">Length: <i><b><span id="count_structure_' + (idx + 1).toString() + '">0</span></b></i> nt</p></div>').appendTo($("#structures"));
  $("#id_structure_" + (idx + 1).toString()).on("blur", app.modPrimerize.fnTrackStructureList);
};


app.modPrimerize.fnOnLoad = function() {
  app.modPrimerize.fnTrackInputLength();
  $("#id_sequence").unbind("blur").on("blur", app.modPrimerize.fnTrackInputLength);
  $("#id_tag").unbind("blur").on("blur", function() {
    var val = $(this).val().match(/[a-zA-Z0-9\ \.\-\_]+/g);
    if (val) { $(this).val(val.join('')); }
  });
  $("#btn_clear").unbind("click").on("click", function(event) {
    event.preventDefault();
    app.modPrimerize.job_id = undefined;
    clearTimeout(ajax_timeout);
    app.href = $(this).attr("href");
    $("#content").fadeTo(100, 0, app.fnChangeLocation);
  });

  var is_2d = (app.page.indexOf("design_2d") !== -1 || app.modPrimerize.job_type === 2),
      is_3d = (app.page.indexOf("design_3d") !== -1 || app.modPrimerize.job_type === 3);

  if (is_2d || is_3d) {
    $("input.primer_input").unbind("blur").on("blur", app.modPrimerize.fnTrackPrimerList);
    $("#btn_add_prm").unbind("blur").on("click", app.modPrimerize.fnExpandPrimerInput);

    if (is_2d) {
      $("#form_2d").submit(function(event) {
        event.preventDefault();
        app.modPrimerize.fnOnDisable();
        $("input.primer_input").prop("disabled", true);
        $.ajax({
          type: "POST",
          url: $(this).attr("action"),
          data: $(this).serialize(),
          success: app.modPrimerize.fnOnSubmit
        });
      });

      $("#btn_demo").unbind("click").on("click", function(event) {
        event.preventDefault();
        app.modPrimerize.fnOnDisable();
        $.ajax({
          type: "GET",
          url: $(this).attr("href"),
          success: app.modPrimerize.fnOnSubmit
        });
      });
    } else {
      $("textarea.structure_input").unbind("blur").on("blur", app.modPrimerize.fnTrackStructureList);
      $("#btn_add_str").unbind("click").on("click", app.modPrimerize.fnExpandStructureInput);

      $("#form_3d").submit(function(event) {
        event.preventDefault();
        app.modPrimerize.fnOnDisable();
        $("textarea.structure_input").prop("disabled", true);
        $("input.primer_input").prop("disabled", true);
        $.ajax({
          type: "POST",
          url: $(this).attr("action"),
          data: $(this).serialize(),
          success: app.modPrimerize.fnOnSubmit
        });
      });

      $("#btn_demo_1, #btn_demo_2").unbind("click").on("click", function(event) {
        event.preventDefault();
        app.modPrimerize.fnOnDisable();
        $.ajax({
          type: "GET",
          url: $(this).attr("href") + '?mode=' + $(this).attr('id').slice(-1),
          success: app.modPrimerize.fnOnSubmit
        });
      });
    }

  } else {
    if ($("#id_is_num_primers").is(":checked")) {
      $("#id_num_primers").removeAttr("disabled");
    } else {
      $("#id_num_primers").attr("disabled", "disabled");
    }
    $("#id_is_num_primers").unbind("click").on("click", function() {
      if ($(this).is(":checked")) {
        $("#id_num_primers").removeAttr("disabled");
      } else {
        $("#id_num_primers").attr("disabled", "disabled");
      }
    });

    $("#form_1d").submit(function(event) {
      event.preventDefault();
      app.modPrimerize.fnOnDisable();
      $.ajax({
        type: "POST",
        url: $(this).attr("action"),
        data: $(this).serialize(),
        success: app.modPrimerize.fnOnSubmit
      });
    });
    $("#btn_demo").unbind("click").on("click", function(event) {
      event.preventDefault();
      app.modPrimerize.fnOnDisable();
      $.ajax({
        type: "GET",
        url: $(this).attr("href"),
        success: app.modPrimerize.fnOnSubmit
      });
    });

  }
};

app.isLoaded = true;
