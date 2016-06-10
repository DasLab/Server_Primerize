var scrollTimer, resizeTimer, side_toggle = true, apache_interval;

app.fnParseLocation = function() {
    var urls = {
        "sys": ["apache", "aws", "ga", "git", "dir", "backup", "bot"],
        "job": ["jobids", "jobgroups", "design1d", "design2d", "design3d"],
        "user": ["auth", "sourcedownloader", "historyitem"],
        "doc": ["man", "ref", "cherrypy"]
    };
    var page = window.location.pathname.replace('/admin', '').replace(/^\//, '').split('/');
    app.page = (page[0] == "src")? page[1] : page[0];
    for (var key in urls) {
        if (urls[key].indexOf(app.page) != -1) {
            app.key = key;
            return;
        }
    }
    app.key = 'home';
};

app.fnChangeBreadcrumb = function() {
    $("ul.breadcrumb li:not(:first-child)").remove();
    if (app.key == "sys") {
        if (app.page == "dir" || app.page == "backup") {
            $("ul.breadcrumb").css("border-bottom", "5px solid #ff69bc");
        } else {
            $("ul.breadcrumb").css("border-bottom", "5px solid #ff5c2b");
        }
        $('<li><span style="color: #000;" class="glyphicon glyphicon-cog"></span>&nbsp;&nbsp;<a href="">System</a></li>').insertAfter($("ul.breadcrumb > li:first"));

        if (app.page == "apache") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-grain"></span>&nbsp;&nbsp;Apache Status</li>');
        } else if (app.page == "aws") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_aws"></i></div>&nbsp;&nbsp;Amazon Web Services</li>');
        } else if (app.page == "ga") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_ga"></i></div>&nbsp;&nbsp;Google Analytics</li>');
        } else if (app.page == "git") {
            $("ul.breadcrumb").append('<li class="active"><div class="sprite i_21"><i class="i_git"></i></div>&nbsp;&nbsp;GitHub Repository</li>');
        } else if (app.page == "dir") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-folder-open"></span>&nbsp;&nbsp;Directory Browser</li>');
        } else if (app.page == "backup") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-floppy-open"></span>&nbsp;&nbsp;Backup Schedule</li>');
        }

    } else if (app.key == "job") {
        $("ul.breadcrumb").css("border-bottom", "5px solid #50cc32");
        $("ul.breadcrumb > li:first").next().remove();

        if (app.page == "jobids") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-credit-card"></span>&nbsp;&nbsp;Job IDs</li>');
        } else if (app.page == "jobgroups") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-qrcode"></span>&nbsp;&nbsp;Job Groups</li>');
        } else if (app.page == "design1d") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-tint"></span>&nbsp;&nbsp;Simple Assembly Designs</li>');
        } else if (app.page == "design2d") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-fire"></span>&nbsp;&nbsp;Mutate-and-Map Designs</li>');
        } else if (app.page == "design3d") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-leaf"></span>&nbsp;&nbsp;Mutation/Rescue Sets</li>');
        }

        $('<li><span style="color: #000;" class="glyphicon glyphicon-inbox"></span>&nbsp;&nbsp;<a href="">Job Management</a></li>').insertAfter($("ul.breadcrumb > li:first"));

    } else if (app.key == "user") {
        if (app.page == "auth") {
            $("ul.breadcrumb").css("border-bottom", "5px solid #ff912e");
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-lock"></span>&nbsp;&nbsp;User Autherization</li>');
        } else {
            $("ul.breadcrumb").css("border-bottom", "5px solid #eeb211");

            if (app.page == "sourcedownloader") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-cloud-download"></span>&nbsp;&nbsp;Source Downloaders</li>');
            } else if (app.page == "historyitem") {
                $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-list-alt"></span>&nbsp;&nbsp;History Items</li>');
            }
        }
        $('<li><span style="color: #000;" class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;<a href="">User Management</a></li>').insertAfter($("ul.breadcrumb > li:first"));

    } else if (app.key == "doc") {
        $("#nav_doc_lg").addClass("active");
        $("ul.breadcrumb").css("border-bottom", "5px solid #c28fdd");

        if (app.page == "man") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-scale"></span>&nbsp;&nbsp;Manual</li>');
        } else if (app.page == "ref") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-briefcase"></span>&nbsp;&nbsp;Reference</li>');
        } else if (app.page == "cherrypy") {
            $("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-apple"></span>&nbsp;&nbsp;CherryPy (Obsolete)</li>');
        }

    } else {
        $("ul.breadcrumb").css("border-bottom", "5px solid #3ed4e7");
    }
};

app.fnChangeView = function() {
    app.fnParseLocation();
    $("#sidebar-wrapper ul li.active").removeClass("active");
    $("#nav_" + app.page).addClass("active");
    $("#nav_" + app.key).addClass("active");
    $("#nav_" + app.key + "_lg").addClass("active");

    app.fnChangeBreadcrumb();
    $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'page' + app.DEBUG_STR + '.js');

    $("#content").fadeTo(100, 1);
    if (typeof this.callbackChangeView === "function") {
        this.callbackChangeView();
    }
};

app.fnChangeLocation = function() {
    if (window.history.replaceState) {
        window.history.replaceState({} , '', app.href);
    } else {
        window.location.href = app.href;
    }
    $("#content_wrapper").load(app.href + " #content_wrapper > *", app.fnChangeView);
};

app.fnNavCollapse = function() {
    if ($("#nav_collapse").is(":visible")) {
        side_toggle = true;
        $("#nav_toggle").trigger("click");
        $("#nav_toggle").hide();
        $("#nav_public").unbind();
        $("#nav_time").unbind();
        $("#nav_profile").unbind();

        $("#nav_logo").css("width", "auto");
    } else {
        $("#nav_toggle").show();
        $("#nav_public").hover(
          function(){ $("#nav_public_text").fadeIn(250).siblings().css("color", "#eeb211"); },
          function(){ $("#nav_public_text").fadeOut(250).siblings().css("color", "#fff"); }
        );

        $(".dropdown-toggle").dropdown();
        $(".dropdown").hover(
          function(){ $(this).addClass("open"); },
          function(){ $(this).removeClass("open"); }
        );
        $("#nav_logo").css("width", parseInt($("#nav_logo").css("width")) + 250 - parseInt($("#nav_public").position().left));
    }
};

app.fnOnLoad = function() {
    $("ul.breadcrumb").css({"border-radius":"0px", "height":"50px"}).addClass("lead");
    $("ul.breadcrumb > li:first").prepend('<span style="color: #000;" class="glyphicon glyphicon-home"></span>&nbsp;&nbsp;');
    app.fnChangeView();

    $("#nav_toggle").on("click", function() {
        if (side_toggle) {
            $(".nav-ul").hide();
            $(".nav-ul-lg").fadeIn(500);
            $("#wrapper").css("padding-left", "50px");
            $("#sidebar-wrapper").css({"margin-left":"-65px", "left":"65px", "width":"65px"});
        } else {
            $("#wrapper").css("padding-left", "235px");
            $("#sidebar-wrapper").css({"margin-left":"-250px", "left":"250px", "width":"250px"});
            setTimeout(function() {
                $(".nav-ul-lg").hide();
                $(".nav-ul").not(".nav-ul-lg").fadeIn(100);
            }, 400);
        }
        side_toggle = !side_toggle;
    });
    $("#wrapper").css("width", (parseInt($("#wrapper").css("width")) + 15).toString() + "px");
    app.fnNavCollapse();

    $("#page-content-wrapper").css("opacity", 0);
    $("#nav_load").css({"opacity": 1, "top": "-50px"}).animate({"top": "0px"}, {"duration": 200, "queue": false});
    $("body > div").css("opacity", 1);
    $("#sidebar-wrapper").animate({"left": "0px"}, {"duration": 200, "queue": false});
    $("#page-content-wrapper").delay(500).fadeTo(150, 1);
};


$(document).ready(function() {
    var today = new Date();
    $("#cp_year").text(today.getFullYear());

    $(".dropdown-toggle").dropdown();
    $(".dropdown").hover(
        function() { $(this).addClass("open"); },
        function() { $(this).removeClass("open"); }
    );

    $('i[class^="icon"]').each(function() {
        $(this).replaceWith('<span class="glyphicon glyph' + $(this).attr("class") + '"></span>&nbsp;&nbsp;');
    });

    $("#sidebar-wrapper a, #nav_admin > a, #nav_logo").on("click", function(event) {
        event.preventDefault();
        app.href = $(this).attr("href");
        $("#content").fadeTo(100, 0, app.fnChangeLocation);
    });

    app.fnOnLoad();
});


$(window).on("resize", function() {
    clearTimeout($.data(this, 'resizeTimer'));
    $.data(this, 'resizeTimer', setTimeout(function() {
        app.fnNavCollapse();
        $("#wrapper").css("width", $(window).width() - $("#sidebar-wrapper").width() - 20);
    }, 200));
});
