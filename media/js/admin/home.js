var $ = django.jQuery;
var weekdayNames = new Array('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday');

$(document).ready(function() {
  $("ul.breadcrumb > li.active").text("System Dashboard");

  // $("#content").addClass("row").removeClass("row-fluid").removeClass("colM");
  $("#content > h2.content-title").remove();
  $("span.divider").remove();
  $("lspan").remove();

  $.ajax({
        url : "/admin/get_ver/",
        dataType: "text",
        success : function (data) {
            var txt = data.split(/\t/);

            $("#id_linux").html(txt[0]);
            $("#id_python").html(txt[1]);
            $("#id_django").html(txt[2]);
            $("#id_django_crontab").html(txt[3]);
            $("#id_django_environ").html(txt[4]);
            $("#id_mysql").html(txt[5]);
            $("#id_apache").html(txt[6]);
            $("#id_wsgi").html(txt[7]);
            $("#id_ssl").html(txt[8]);

            $("#id_jquery").html(txt[9]);
            $("#id_bootstrap").html(txt[10]);
            $("#id_django_suit").html(txt[11]);
            $("#id_django_adminplus").html(txt[12]);
            $("#id_django_filemanager").html(txt[13]);
            $("#id_d3").html(txt[14]);
            $("#id_zclip").html(txt[15]);
            $("#id_gvizapi").html(txt[16]);

            $("#id_ssh").html(txt[17]);
            $("#id_git").html(txt[18]);
            $("#id_llvm").html(txt[19]);
            $("#id_nano").html(txt[20]);
            $("#id_gdrive").html(txt[21]);
            $("#id_curl").html(txt[22]);
            $("#id_boto").html(txt[23]);
            $("#id_pygit").html(txt[24]);

            $("#id_request").html(txt[25]);
            $("#id_simplejson").html(txt[26]);
            $("#id_virtualenv").html(txt[27]);
            $("#id_pip").html(txt[28]);

            $("#id_numpy").html(txt[29]);
            $("#id_scipy").html(txt[30]);
            $("#id_matplotlib").html(txt[31]);
            $("#id_numba").html(txt[32]);

            $("#id_yui").html(txt[33]);
            $("#id_rdatkit").html(txt[34]);
            $("#id_primerize").html(txt[35]);

            var drive_free = parseFloat(txt[46]), drive_used = parseFloat(txt[45]), drive_total = parseFloat(txt[47]);
            $("#id_drive_space > div > div.progress-bar-success").css("width", (drive_free / drive_total * 100).toString() + '%' ).html(drive_free + ' G');
            $("#id_drive_space > div > div.progress-bar-danger").css("width", (drive_used / drive_total * 100).toString() + '%' ).html(drive_used + ' G');
            var disk_sp = txt[36].split(/\//);
            $("#id_disk_space > div > div.progress-bar-success").css("width", (parseFloat(disk_sp[0]) / (parseFloat(disk_sp[0]) + parseFloat(disk_sp[1])) * 100).toString() + '%' ).html(disk_sp[0]);
            $("#id_disk_space > div > div.progress-bar-danger").css("width", (parseFloat(disk_sp[1]) / (parseFloat(disk_sp[0]) + parseFloat(disk_sp[1])) * 100).toString() + '%' ).html(disk_sp[1]);
            var mem_sp = txt[37].split(/\//);
            $("#id_memory > div > div.progress-bar-success").css("width", (parseFloat(mem_sp[0]) / (parseFloat(mem_sp[0]) + parseFloat(mem_sp[1])) * 100).toString() + '%' ).html(mem_sp[0]);
            $("#id_memory > div > div.progress-bar-danger").css("width", (parseFloat(mem_sp[1]) / (parseFloat(mem_sp[0]) + parseFloat(mem_sp[1])) * 100).toString() + '%' ).html(mem_sp[1]);

            $("#id_backup").html('<span style="color:#00f;">' + txt[38] + '</span>');
            var cpu = txt[39].split(/\//);
            $("#id_cpu").html('<span style="color:#f00;">' + cpu[0] + '</span> | <span style="color:#080;">' + cpu[1] + '</span> | <span style="color:#00f;">' + cpu[2] + '</span>');

            $("#id_base_dir").html('<code>' + txt[40] + '</code>');
            $("#id_media_root").html('<code>' + txt[41] + '</code>');
            $("#id_static_root").html('<code>' + txt[42] + '</code>');
            $("#id_primerize_path").html('<code>' + txt[43] + '</code>');
            $("#id_rdatkit_path").html('<code>' + txt[44] + '</code>');
        }
    });

    $.ajax({
        url : "/admin/backup_form/",
        dataType: "json",
        success : function (data) {
            $("#id_week_backup").html($("#id_week_backup").html() + '<br/>On <span class="label label-primary">' + data.time_backup + '</span> every <span class="label label-inverse">' + weekdayNames[data.day_backup] + '</span> (UTC)');
            $("#id_week_upload").html($("#id_week_upload").html() + '<br/>On <span class="label label-primary">' + data.time_upload + '</span> every <span class="label label-inverse">' + weekdayNames[data.day_upload] + '</span> (UTC)');

            if (data.time_backup) {
                $("#id_week_backup_stat").html('<p class="lead"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></p>');
            } else {
                $("#id_week_backup_stat").html('<p class="lead"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></p>');
            }
            if (data.time_upload) {
                $("#id_week_upload_stat").html('<p class="lead"><span class="label label-green"><span class="glyphicon glyphicon-ok-sign"></span></span></p>');
            } else {
                $("#id_week_upload_stat").html('<p class="lead"><span class="label label-danger"><span class="glyphicon glyphicon-remove-sign"></span></span></p>');
            }
        }
    });

   $.ajax({
        url : "/admin/ssl_dash/",
        dataType: "json",
        success : function (data) {
            $("#id_ssl_exp").html('<span class="label label-inverse">' + data.exp_date + '</span> (UTC)');
        }
    });

});

