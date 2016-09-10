if (typeof app.fnFormatInput !== "function") {
    function replace_path(string) {
        return string.replace('home/ubuntu/Server_Primerize/data/', '/site_data/').replace('Website_Server/Primerize/data/', '/site_data/');
    }

    app.fnFormatInput = function() {
        $("label.required").css("font-weight", "bold");
        $("table").addClass("table-hover").removeClass("table-bordered table-condensed");
        $('[scope="col"]').addClass("info");

        $("a.deletelink").css("box-sizing", "border-box");
        $("input").addClass("form-control");
        $("select").addClass("form-control");
        $("textarea").addClass("form-control");
        $("#id_sequence, #id_structures, #id_primers, #id_params, #id_plates").addClass("monospace");
        $("#id_job_id, #id_job_1d, #id_job_2d, #id_job_3d").addClass("monospace job_id");
        $("span.add-on").html('<span class="glyphicon glyphicon-calendar"></span>').addClass("input-group-addon").removeClass("add-on");

        $('th > div.text > span > input[type="checkbox"]').each(function() {
            var parent = $(this).parent();
            $(this).css("display", "");
            $(this).detach().insertBefore(parent);
        });
        $('input[type="checkbox"], input[type="radio"]').each(function() {
            $(this).parent().addClass("checkbox");
            if ($(this).next().is("label")) {
                $(this).prependTo($(this).next());
            } else {
                $(this).removeClass("form-control");
                $(this).next().css("padding-left", "10px");
                $('<label></label>').insertBefore($(this));
                var elem = $(this).prev();
                $(this).next().appendTo(elem);
                $('<span class="cr"><span class="cr-icon glyphicon glyphicon-ok"></span></span>').prependTo(elem);
                $(this).prependTo(elem);
                $('<div class="checkbox"></div>').insertBefore(elem);
                elem.appendTo(elem.prev());
            }
        });

        $('p.file-upload > a').each(function() {
            $(this).replaceWith('<div class="form-inline"><label>Current:&nbsp;&nbsp;</label><input class="form-control" disabled="disabled" style="cursor:text;" value="' + $(this).attr("href") + '">&nbsp;&nbsp;<a href="'+ replace_path($(this).attr("href")) + '" class="form-file-view btn btn-default" target="_blank" rel="noopener"><span class="glyphicon glyphicon-cloud-download"></span>&nbsp;&nbsp;View&nbsp;&nbsp;</a></div>');
        });
        $('.clearable-file-input').each(function() {
            $(this).appendTo($(this).prev());
            $(this).children().contents().filter(function () {return this.data === "Clear";}).replaceWith("&nbsp;&nbsp;<span class='glyphicon glyphicon-remove-sign'></span>&nbsp;Clear");
        });
        $('input[type="file"]').each(function() {
            $('<div class="form-inline"><label>Change:&nbsp;&nbsp;</label><input id="' + $(this).attr("id") + '_disp" class="form-control" placeholder="No file chosen" disabled="disabled" style="cursor:text;"/>&nbsp;&nbsp;<div id="' + $(this).attr("id") + '_btn" class="fileUpload btn btn-info"><span><span class="glyphicon glyphicon-folder-open"></span>&nbsp;&nbsp;Browse&nbsp;&nbsp;</span></div>').insertAfter(this);
            $(this).detach().appendTo('#' + $(this).attr("id") + '_btn');

            $(this).on("change", function () {
                $('#' + $(this).attr("id") + '_disp').val($(this).val().replace("C:\\fakepath\\", ""));
            });
            $('.file-upload').contents().filter(function () {return this.data === "Change: " | this.data === "Currently: ";}).remove();
        });
        $('input[disabled="disabled"]').each(function() {
            $(this).width($(this).width()*2.5);
        });

        $(".toggle.descending").html('<span class="glyphicon glyphicon-chevron-up"></span>');
        $(".toggle.ascending").html('<span class="glyphicon glyphicon-chevron-down"></span>');
        $(".sortremove").html('<span class="glyphicon glyphicon-remove"></span>');
        $(".sortoptions").addClass("pull-right").removeClass("sortoptions");
        $("div.pagination-info").html("<br/>&nbsp;&nbsp;&nbsp;&nbsp;" + $("div.pagination-info").html());


        setTimeout(function() {
            $(".vDateField").each(function () {
                $(this).next().detach().appendTo($(this).parent());
                $(this).removeAttr("size");
                $(this).next().detach().insertAfter($(this).parent());
                $(this).parent().addClass("input-group").removeClass("");

                $('<div class="input-group-btn"><a class="btn btn-default" id="' + $(this).attr("id") + '_cal"><span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Calendar&nbsp;&nbsp;</a><a class="btn btn-primary" id="' + $(this).attr("id") + '_today"><span class="glyphicon glyphicon-map-marker"></span>&nbsp;&nbsp;Today&nbsp;&nbsp;</a></div>').insertAfter($(this));
                $(this).css("width", "auto");

                var elem;
                if ($(this).parent().next().hasClass("datetimeshortcuts")) {
                    elem = $(this).parent().next();
                } else {
                    // $('<br><br>').insertBefore($(this).parent().next());
                    $(this).parent().next().css("display", "block");
                    elem = $(this).siblings().last();
                }
                $('#' + $(this).attr("id") + '_cal').attr("href", elem.children().last().attr("href"));
                $('#' + $(this).attr("id") + '_cal').on("click", function() {
                    var self = $(this);
                    setTimeout(function () {
                        $(".calendarbox.module").css("left", self.offset().left);
                        $(".calendarbox.module").css("top", self.offset().top + 50);
                    }, 50);
                });
                $('#' + $(this).attr("id") + '_today').attr("href", elem.children().first().attr("href"));

                elem.css("display", "none");
                $('<p class="datetime input-group"></p>').insertBefore($(this));
                var p = $(this).prev();
                $(this).next().detach().appendTo(p);
                $(this).detach().prependTo(p);
                $("span.timezonewarning").addClass("label label-default");
                $("div.input-group-btn").css("display", "");
            });

            $(".vTimeField").each(function () {
                $(this).next().detach().appendTo($(this).parent());
                $(this).removeAttr("size");
                $(this).next().detach().insertAfter($(this).parent());
                $(this).parent().addClass("input-group").removeClass("");

                $('<div class="input-group-btn"><a class="btn btn-default" id="' + $(this).attr("id") + '_clk"><span class="glyphicon glyphicon-time"></span>&nbsp;&nbsp;Clock&nbsp;&nbsp;</a><a class="btn btn-primary" id="' + $(this).attr("id") + '_now"><span class="glyphicon glyphicon-map-marker"></span>&nbsp;&nbsp;Now&nbsp;&nbsp;</a></div>').insertAfter($(this));
                $(this).css("width", "auto");

                var elem;
                if ($(this).parent().next().hasClass("datetimeshortcuts")) {
                    elem = $(this).siblings().last();
                } else {
                    // $('<br><br>').insertBefore($(this).parent().next());
                    $(this).parent().next().css("display", "block");
                    elem = $(this).siblings().last();
                }
                $('#' + $(this).attr("id") + '_clk').attr("href", elem.children().last().attr("href"));
                $('#' + $(this).attr("id") + '_clk').on("click", function() {
                    var self = $(this);
                    setTimeout(function () {
                        $(".clockbox.module").css("left", self.offset().left);
                        $(".clockbox.module").css("top", self.offset().top + 50);
                    }, 50);
                });
                $('#' + $(this).attr("id") + '_now').attr("href", elem.children().first().attr("href"));

                elem.css("display", "none");
                $('<p class="datetime input-group"></p>').insertBefore($(this));
                var p = $(this).prev();
                $(this).next().detach().appendTo(p);
                $(this).detach().prependTo(p);
                $("span.timezonewarning").addClass("label label-default");
                $("div.input-group-btn").css("display", "");
            });


            if ($(location).attr("href").indexOf("admin/auth/user") != -1) {
                $("span.help-icon").removeClass("help help-tooltip help-icon").addClass("glyphicon glyphicon-question-sign");
                $("select").addClass("form-control").removeClass("filtered");
                $("input[placeholder='Filter']").addClass("form-control").parent().addClass("input-group");
                $("<br/>").insertAfter($("input[placeholder='Filter']").parent());
                $('<div class="input-group-addon"><span class="glyphicon glyphicon-search"></span></div>').insertAfter($("input[placeholder='Filter']"));
                $("img[src='/static/admin/img/selector-search.svg']").parent().remove();
                $('<span class="glyphicon glyphicon-question-sign"></span>').insertAfter($("img[src='/static/admin/img/icon-unknown.svg']"));
                $("img[src='/static/admin/img/icon-unknown.svg']").remove();

                $("a.selector-add").addClass("btn btn-inverse").html('<span class="glyphicon glyphicon-circle-arrow-right"></span>');
                $("a.selector-remove").addClass("btn btn-default").html('<span class="glyphicon glyphicon-circle-arrow-left"></span>');
                $("a.add-related").addClass("btn btn-blue").html('<span class="glyphicon glyphicon-plus-sign"></span>&nbsp;&nbsp;Add Group');
                $("<br/>").insertBefore($("a.selector-chooseall"));
                $("a.selector-chooseall").addClass("btn btn-info").html('<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;Choose All');
                $("<br/>").insertBefore($("a.selector-clearall"));
                $("a.selector-clearall").addClass("btn btn-default").html('<span class="glyphicon glyphicon-remove-sign"></span>&nbsp;&nbsp;Remove All');
            }

            $("img[src$='/static/admin/img/icon-yes.svg']").each(function() {
                var newElem = $('<span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span>');
                $(this).replaceWith(newElem);
            });
            $("img[src$='/static/admin/img/icon-no.svg']").each(function() {
                var newElem = $('<span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span>');
                $(this).replaceWith(newElem);
            });
            $("img[src$='/static/admin/img/icon-changelink.svg']").each(function() {
                var newElem = $('<span class="label label-warning"><span class="glyphicon glyphicon-edit"></span></span>');
                $(this).replaceWith(newElem);
            });
            $("img[src$='/static/admin/img/icon-addlink.svg']").each(function() {
                var newElem = $('<span class="label label-success"><span class="glyphicon glyphicon-plus-sign"></span></span>');
                $(this).replaceWith(newElem);
            });

        }, 50);
    };
}
app.fnFormatInput();


if (app.page == "apache") {
    $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'apache' + app.DEBUG_STR + '.js');
} else {
    clearTimeout(apache_interval);
}

if (app.page == "backup") {
    $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'backup' + app.DEBUG_STR + '.js');
} else if (app.page == "dir") {
    $("#iframe").css("width", parseInt($("#content").css("width")) - 50);
    // $("#iframe").css("height", $("#footer").position().top - $("#content").position().top - 175);
    $("#iframe").css("height", 800);
} else if (app.page == "aws" || app.page == "ga" || app.page == "git") {
    $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'gapi' + app.DEBUG_STR + '.js');

} else if (app.page == "man" || app.page == "ref" || app.page == "cherrypy") {
    $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'doc' + app.DEBUG_STR + '.js');

} else if (app.page == "auth") {
    $("div.object-tools > a").attr({"disabled": "disabled", "onclick": "return false;", "id": "btn-auth-add"});

} else if (window.location.pathname.replace(/\/$/, '') == '/admin') {
    $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'home' + app.DEBUG_STR + '.js');
}

if (["apache", "aws", "ga", "git", "dir", "backup", "man", "ref", "cherrypy"].indexOf(app.page) == -1 && app.key != 'home') {
    $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'table' + app.DEBUG_STR + '.js');
    $("#content a:not(#btn-slack-add):not(#btn-auth-add):not(.form-file-view)").on("click", function(event) {
        event.preventDefault();
        app.href = $(this).attr("href");
        $("#content").fadeTo(100, 0, app.fnChangeLocation);
    });
}

