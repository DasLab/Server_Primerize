app.fnIndexResize = function() {
    $("#col-1").css("height", "auto");
    $("#col-2").css("height", "auto");
    $("#col-3").css("height", "auto");
    $("#col-4").css("height", "auto");

    var col_h = Math.max(parseInt($("#col-1").css("height")), parseInt($("#col-2").css("height")), parseInt($("#col-3").css("height")), parseInt($("#col-4").css("height")));
    $("#col-1").css("height", col_h);
    $("#col-2").css("height", col_h);
    $("#col-3").css("height", col_h);
    $("#col-4").css("height", col_h);

    $(window).on("resize", function() {
        clearTimeout($.data(this, 'resizeTimer'));
        $.data(this, 'resizeTimer', setTimeout(app.fnIndexResize, 200));
    });
};

app.fnTutorialResize = function() {
    $("#main").addClass("pull-right");
    $("#sidebar").css("width", $("#navbar").width() - $("#main").width() - 30);

    if ($("#sidebar").width() < 200) {
        app.resize_degree = 1;
        $("#side").removeClass("col-lg-2 col-md-2").addClass("row");
        $("#main").addClass("row").removeClass("pull-right");
        $("#sidebar").css("width", "auto").removeAttr("data-spy").removeClass("affix").removeClass("affix-top");
        $("#side_con").addClass("container");
    } else {
        $("#side").addClass("col-lg-2 col-md-2").removeClass("row");
        $("#main").removeClass("row").addClass("pull-right");
        $("#sidebar").attr("data-spy", "affix").affix({"offset": {"top": $("#main").position().top}});
        $("#side_con").removeClass("container");

        if ($("#navbar").width() >= 1680) {
            $("#sidebar").css("width", ($("#navbar").width() - $("#main").width())/2 - 25);
            // $("#side").css("padding-right","0px");
            // $("#side_con").css("padding-right","0px");
            $("#main").removeClass("pull-right").addClass("row");
            app.resize_degree = 3;
        } else {
            $("#main").addClass("pull-right");
            $("#sidebar").css("width", ($("#navbar").width() - $("#main").width()) - 25);
            app.resize_degree = 2;
        }
    }

    $(window).on("resize", function() {
        clearTimeout($.data(this, 'resizeTimer'));
        $.data(this, 'resizeTimer', setTimeout(app.fnTutorialResize, 200));
    });
};

app.fnDesignResize = function() {
    $("#col-res-l").css("height", "auto");
    $("#col-res-r").css("height", "auto");

    var col_h = Math.max(parseInt($("#col-res-l").css("height")), parseInt($("#col-res-r").css("height")));
    $("#col-res-l").css("height", col_h);
    $("#col-res-r").css("height", col_h);

    $(window).on("resize", function() {
        clearTimeout($.data(this, 'resizeTimer'));
        $.data(this, 'resizeTimer', setTimeout(app.fnDesignResize, 200));
    });
};


app.callbackLoadD3 = function(func) {
    if (!app.isLoaded) {
        if (app.isCDN) {
            var d3_js = [
                'https://cdnjs.cloudflare.com/ajax/libs/d3/' + app.js_ver.d3 + '/d3.min.js',
                'https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/' + app.js_ver.clip + '/clipboard.min.js',
                '/site_media/js/public/' + app.DEBUG_DIR + 'plate' + app.DEBUG_STR + '.js'
            ];
        } else {
            var d3_js = ['/site_media/js/public/min/plt.min.js'];
        }
        head.test(d3, [], d3_js, function(flag) {
            $.getScript('/site_media/js/public/' + app.DEBUG_DIR + 'design' + app.DEBUG_STR + '.js', function(data, code, xhr) {
                if (func === "init") { func = app.modPrimerize.fnOnLoad; }
                if (typeof func === "function") { func(); }
            });
        });
    } else {
        if (func === "init") { func = app.modPrimerize.fnOnLoad; }
        if (typeof func === "function") { func(); }
    }
};


app.modPrimerize.job_id = undefined;
app.modPrimerize.job_type = undefined;
app.resize_degree = 0;

$(".btn-spa").on("click", function(event) {
    event.preventDefault();
    app.href = $(this).attr("href");
    $("#content").fadeTo(100, 0, app.fnChangeLocation);
});
$("div.svg_tooltip").css({"opacity": 0, "top": 0, "left": 0});


if (app.key == "home") {
    setTimeout(app.fnIndexResize, 200);

    $("#form_retrieve").submit(function(event) {
        event.preventDefault();
        app.href = $(this).attr("action") + "?" + $(this).serialize();
        // app.modPrimerize.job_id = $("#input_job_id").val();
        $("#content").fadeTo(100, 0, app.fnChangeLocation);
    });
    $("#btn_retrieve").prop("disabled", true);
    $("#input_job_id").on("change", function() {
        var val = $(this).val().match(/^([a-fA-F0-9]){0,16}/g);
        if (val) { $(this).val(val.join('')); }
        if ($(this).val().length == 16) {
            $("#btn_retrieve").prop("disabled", false);
        } else {
            $("#btn_retrieve").prop("disabled", true);
        }
    });

} else if (app.key == "design") {
    app.callbackLoadD3("init");

    if ($("#result_job_id").html().length > 0) {
        var result_timeout = setTimeout(function() {
            if (app.isLoaded) {
                app.modPrimerize.fnAjaxRetrieveResult($("#result_job_id").html());
                $("#result_job_id").html("");
                clearTimeout(result_timeout);
            }
        }, 500);
    } else if ($("#result_from_1d").html() === "True") {
        var result_timeout = setTimeout(function() {
            if (app.isLoaded) {
                app.modPrimerize.fnSyncPrimerInput($("#id_primers").val().split(','));
                $("input.primer_input").prop("readonly", true);
                $("#id_sequence").prop("readonly", true);
                $("#btn_add_prm").prop("disabled", true);
                $("#result_from_1d").html("");
                clearTimeout(result_timeout);
            }
        }, 500);
    } else if ($("#result_from_2d").html() === "True") {
        var result_timeout = setTimeout(function() {
            if (app.isLoaded) {
                app.modPrimerize.fnSyncPrimerInput($("#id_primers").val().split(','));
                $("input.primer_input").prop("readonly", true);
                $("#id_sequence").prop("readonly", true);
                $("#btn_add_prm").prop("disabled", true);
                $("#id_offset").prop("readonly", true);
                $("#id_offset").prop("disabled", true);
                $("#id_min_muts").prop("readonly", true);
                $("#id_min_muts").prop("disabled", true);
                $("#id_max_muts").prop("readonly", true);
                $("#id_max_muts").prop("disabled", true);
                $("#result_from_2d").html("");
                clearTimeout(result_timeout);
            }
        }, 500);
    }

} else if (app.key == "tutorial" || app.key == "protocol" || app.key == "code") {
    $('body').scrollspy({
        'target': '.scroll_nav',
        'offset': 150
    });
    $('.scroll_nav').on('activate.bs.scrollspy', function() {
        $('.scroll_nav > ul > li:not(.active) > ul.panel-collapse').collapse('hide');
        $('.scroll_nav > ul > li.active > ul.panel-collapse').collapse('show');
    });
    app.fnTutorialResize();

    $('[id^=tab_], #up').on('click', function() {
        $('html, body').stop().animate({"scrollTop": $($(this).attr("href")).offset().top - 75}, 500);
    });

    $('ul.panel-collapse').on('show.bs.collapse', function() {
        $(this).parent().find("a>span.glyphicon.pull-right")
        .removeClass("glyphicon-triangle-bottom")
        .addClass("glyphicon-triangle-top");
    });
    $('ul.panel-collapse').on('hide.bs.collapse', function() {
        $(this).parent().find("a>span.glyphicon.pull-right")
        .removeClass("glyphicon-triangle-top")
        .addClass("glyphicon-triangle-bottom");
    });

    $(window).on("scroll", function() {
        if ($(this).scrollTop() > $(window).height()/2) {
            $('#up').fadeIn();
        } else {
            $('#up').fadeOut();
        }
        if (app.resize_degree == 1) {
            $("#sidebar").css("width", "auto").removeAttr("data-spy").removeClass("affix").removeClass("affix-top");
        }
    });

    if (app.key == "protocol") {
        $("#calc_DNA").on('click', function() {
            var A260 = $("#A260_DNA").val(),
                l = $("#l_DNA").val();
            $("#conc_DNA").val(parseFloat(A260) * 50000 / 660 / parseInt(l) );
        });
        $("#clc_DNA").on('click', function() {
            $("#A260_DNA").val('');
            $("#l_DNA").val('');
            $("#conc_DNA").val('');
        });

        $("#calc_RNA").on('click', function() {
            var A260 = $("#A260_RNA").val(),
                l = $("#l_RNA").val();
            $("#conc_RNA").val(parseFloat(A260) * 40000 / 330 / parseInt(l) );
        });
        $("#clc_RNA").on('click', function() {
            $("#A260_RNA").val('');
            $("#l_RNA").val('');
            $("#conc_RNA").val('');
        });

        app.callbackLoadD3(function() {
            var unit = parseInt($("#par_plate_final1").width() / 33);
            app.mod96Plate.cell_radius = unit;
            app.mod96Plate.cell_stroke = unit / 5;
            app.mod96Plate.tick_width = unit * 3;

            $.ajax({
                url: '/site_media/images/docs/par_plate_final.json',
                dataType: "json",
                success: function(data) {
                    app.mod96Plate.fnDrawSinglePlate(d3.select("#par_plate_final1"), data.data, false);
                    app.mod96Plate.fnDrawSinglePlate(d3.select("#par_plate_final2"), data.data, false);
                }
            });
            for (var i = 1; i <= 4; i++) {
                (function(i) {
                    $.ajax({
                        url: '/site_media/images/docs/par_plate_primer' + i + '.json',
                        dataType: "json",
                        success: function(data) { app.mod96Plate.fnDrawSinglePlate(d3.select("#par_plate_primer" + i), data.data, false); }
                    });
                    $.ajax({
                        url: '/site_media/images/docs/par_plate_primer' + i + '_filled.json',
                        dataType: "json",
                        success: function(data) { app.mod96Plate.fnDrawSinglePlate(d3.select("#par_plate_primer" + i + "_filled"), data.data, false); }
                    });
                })(i);
            }
            $.ajax({
                url: '/site_media/images/docs/par_plate_helper.json',
                dataType: "json",
                success: function(data) { app.mod96Plate.fnDrawSinglePlate(d3.select("#par_plate_helper"), data.data, false); }
            });
        });

    } else if (app.key == "tutorial") {
        app.callbackLoadD3(function() {
            var unit = parseInt($("[id^='svg_2d_plt_']").first().width() / 33);
            app.mod96Plate.cell_radius = unit;
            app.mod96Plate.cell_stroke = unit / 5;
            app.mod96Plate.tick_width = unit * 3;

            $.ajax({
                url: '/site_data/2d/result_' + $("#job_id_2d").text() + '.json',
                dataType: "json",
                success: function(data) {
                    for (var plt_key in data.plates) {
                        for (var prm_key in data.plates[plt_key].primers) {
                            app.mod96Plate.fnDrawSinglePlate(d3.select("#svg_2d_plt_" + plt_key + "_prm_" + prm_key), data.plates[plt_key].primers[prm_key], false);
                        }
                    }
                    $("#svg_2d_plt_1_hidden").css("height", $("#svg_2d_plt_1_prm_6").css("height"));
                }
            });
            $.ajax({
                url: '/site_data/3d/result_' + $("#job_id_3d").text() + '.json',
                dataType: "json",
                success: function(data) {
                    for (var plt_key in data.plates) {
                        for (var prm_key in data.plates[plt_key].primers) {
                            app.mod96Plate.fnDrawSinglePlate(d3.select("#svg_3d_plt_" + plt_key + "_prm_" + prm_key), data.plates[plt_key].primers[prm_key], false, function() {
                               if (plt_key == 1 && prm_key == 3) {
                                    $("#svg_3d_plt_1_prm_3 circle.seqpos_168.seqpos_173").addClass("active");
                                    $(".svg_tooltip").html('<table style="margin-top:5px;"><tbody><tr><td style="padding-right:20px;"><p><span class="label label-default">Well Position</span></p></td><td colspan="2"><p><span class="label label-primary">D03</span></p></td></tr><tr><td style="padding-right:20px;"><p><span class="label label-default">Name</span></p></td><td><p>Lib <span class="label label-warning">1</span></p></td><td><p><span class="label label-dark-blue">T</span><span class="label label-teal">168</span><span class="label label-dark-red">A</span></p></td></tr><tr><td></td><td></td><td><p><span class="label label-dark-blue">A</span><span class="label label-teal">173</span><span class="label label-dark-red">T</span></p></td></tr><tr><td style="padding-right:20px;"><p><span class="label label-default">Sequence</span></p></td><td colspan="2" style="word-break:break-all"><code style="padding:0px; border-radius:0px;">TTGCGGGAAAGGGGTCAACAGCCGTTCAGTACCAAGTCTCAGG</code></td></tr></tbody></table>').css({"top": $("#svg_3d_plt_1_prm_3").offset().top + 100, "left": $("#svg_3d_plt_1_prm_3").offset().left, "opacity": 0.6});
                                }
                            });
                        }
                    }
                }
            });
        });
    }

} else if (app.key == "code") {
    if (app.page == "license") {
        $("#btn_decline, #btn_accept").on("click", function(event) {
            event.preventDefault();
            app.href = $(this).attr("href");
            $("#content").fadeTo(100, 0, app.fnChangeLocation);
        });

    } else if (app.page == "download") {
        $("#form_dl").submit(function(event) {
            event.preventDefault();
            $.ajax({
                type: "POST",
                url: $(this).attr("action"),
                data: $(this).serialize(),
                success: function(data) {
                    if (data.status === 0) {
                        $("#form_dl_notice > span.glyphicon").addClass("glyphicon-remove-sign").removeClass("glyphicon-hourglass");
                        $("#form_dl_msg").html('<b>ERROR</b>: Invalid contact information. Please try again.');
                        $("#form_dl_notice").fadeIn(200);
                    } else if (data.status === 1) {
                        $("#form_dl_notice > span.glyphicon").addClass("glyphicon-ok-sign").removeClass("glyphicon-hourglass");
                        $("#form_dl_msg").html('<b class="lead">Your registration was successful.</b><br/>You will be notified about future Primerize updates depending on your subscription preference.<br/><br/>Your download should start automatically. If not, please click on <span class="glyphicon glyphicon-floppy-save" style="color:#345e91;"></span> icons below.');
                        $("#form_dl_notice").addClass("alert-success").removeClass("alert-danger").fadeIn(200);

                        $("a[id^='a_dl_']").css("color", "").removeAttr("onclick").on("click", function(event) {
                            event.preventDefault();
                            window.open($(this).attr("href") + "?" + $("#form_dl").serialize());
                        });
                        window.open($("#d_al_master").attr("href") + "?" + $("#form_dl").serialize());
                    }
                }
            });
        });
    }
}

