function replace_path(string) {
    return string.replace('/home/ubuntu/Server_Primerize/data/', '/site_data/').replace('/Website_Server/Primerize/data/', '/site_data/');
}

function render_status(string) {
    var span_class = 'default';
    if (string == 'Success') {
        span_class = 'success';
    } else if (string == 'Error') {
        span_class = 'danger';
    } else if (string == 'Underway') {
        span_class = 'warning';
    } else if (string == 'Fail') {
        span_class = 'orange';
    } else if (string == 'Demo') {
        span_class = 'info';
    }
    return '<span class="label label-' + span_class + '">' + string + '</span>';
}

function render_type(string) {
    var span_class = 'default';
    if (string == 'Simple Assembly') {
        span_class = 'primary';
    } else if (string == 'Mutate-and-Map') {
        span_class = 'orange';
    } else if (string == 'Mutation/Rescue') {
        span_class = 'teal';
    }
    return '<span class="label label-' + span_class + '">' + string + '</span>';
}


$(document).ready(function () {
    // $('script[src="/static/admin/js/admin/DateTimeShortcuts.js"]').remove();
    // $('script[src="/static/admin/js/jquery.js"]').remove();
    // $('script[src="/static/admin/js/jquery.init.js"]').remove();

    if ($(location).attr("href").indexOf("admin/src/jobids") != -1) {
        $("th.column-date").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-job_id").addClass("col-lg-6 col-md-6 col-sm-6 col-xs-6");
        $("th.column-type").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");

        $("td.field-job_id").each(function() { $(this).html("<kbd>" + $(this).html() + "</kbd>"); });
        $("td.field-type").each(function() { $(this).html(render_type($(this).html())); });

        $("th.column-job_id > div.text > a").html('<span class="glyphicon glyphicon-credit-card"></span>&nbsp;&nbsp;Job IDs');
        $("th.column-type > div.text > a").html('<span class="glyphicon glyphicon-adjust"></span>&nbsp;&nbsp;Job Type');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-credit-card"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/jobgroups") != -1) {
        $("th.column-id").addClass("col-lg-1 col-md-1 col-sm-1 col-xs-1");
        $("th.column-tag").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-job_1d").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-job_2d").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-job_3d").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");

        $("td.field-tag").css("font-style", "italic");
        $("td.field-job_1d").each(function() { $(this).html("<kbd>" + $(this).html() + "</kbd>"); });
        $("td.field-job_2d").each(function() { $(this).html("<kbd>" + $(this).html() + "</kbd>"); });
        $("td.field-job_3d").each(function() { $(this).html("<kbd>" + $(this).html() + "</kbd>"); });

        $("th.column-id > div.text > a").html('<span class="glyphicon glyphicon-th-large"></span>');
        $("th.column-tag > div.text > a").html('<span class="glyphicon glyphicon-tag"></span>&nbsp;&nbsp;Job Tag');
        $("th.column-job_1d > div.text > a").html('<span class="glyphicon glyphicon-credit-card"></span>&nbsp;&nbsp;Job Entry of <code>Design1D</code>');
        $("th.column-job_2d > div.text > a").html('<span class="glyphicon glyphicon-credit-card"></span>&nbsp;&nbsp;Job Entry of <code>Design2D</code>');
        $("th.column-job_3d > div.text > a").html('<span class="glyphicon glyphicon-credit-card"></span>&nbsp;&nbsp;Job Entry of <code>Design3D</code>');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-qrcode"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/design1d") != -1) {
        $("th.column-date").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-job_id").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-tag").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-status").addClass("col-lg-1 col-md-1 col-sm-1 col-xs-1");
        $("th.column-sequence").addClass("col-lg-5 col-md-5 col-sm-5 col-xs-5");

        $("td.field-tag").css("font-style", "italic");
        $("td.field-job_id").each(function() { $(this).html("<kbd>" + $(this).html() + "</kbd>"); });
        $("td.field-status").each(function() { $(this).html(render_status($(this).html())); });
        $("td.field-sequence").css("word-break", "break-all");
        $("td.field-sequence").each(function() { $(this).html('<code style="padding:0px; border-radius:0px;">' + $(this).html() + "</code>"); });

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Submission Date');
        $("th.column-job_id > div.text > a").html('<span class="glyphicon glyphicon-credit-card"></span>&nbsp;&nbsp;Job ID');
        $("th.column-tag > div.text > a").html('<span class="glyphicon glyphicon-tag"></span>&nbsp;&nbsp;Tag');
        $("th.column-status > div.text > a").html('<span class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;Status');
        $("th.column-sequence > div.text > a").html('<span class="glyphicon glyphicon-console"></span>&nbsp;&nbsp;Sequence');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-tint"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/design2d") != -1) {
        $("th.column-date").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-job_id").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-tag").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-status").addClass("col-lg-1 col-md-1 col-sm-1 col-xs-1");
        $("th.column-sequence").addClass("col-lg-5 col-md-5 col-sm-5 col-xs-5");

        $("td.field-tag").css("font-style", "italic");
        $("td.field-job_id").each(function() { $(this).html("<kbd>" + $(this).html() + "</kbd>"); });
        $("td.field-status").each(function() { $(this).html(render_status($(this).html())); });
        $("td.field-sequence").css("word-break", "break-all");
        $("td.field-sequence").each(function() { $(this).html('<code style="padding:0px; border-radius:0px;">' + $(this).html() + "</code>"); });

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Submission Date');
        $("th.column-job_id > div.text > a").html('<span class="glyphicon glyphicon-credit-card"></span>&nbsp;&nbsp;Job ID');
        $("th.column-tag > div.text > a").html('<span class="glyphicon glyphicon-tag"></span>&nbsp;&nbsp;Tag');
        $("th.column-status > div.text > a").html('<span class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;Status');
        $("th.column-sequence > div.text > a").html('<span class="glyphicon glyphicon-console"></span>&nbsp;&nbsp;Sequence');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-tint"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/design3d") != -1) {
        $("th.column-date").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-job_id").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-tag").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-status").addClass("col-lg-1 col-md-1 col-sm-1 col-xs-1");
        $("th.column-sequence").addClass("col-lg-5 col-md-5 col-sm-5 col-xs-5");

        $("td.field-tag").css("font-style", "italic");
        $("td.field-job_id").each(function() { $(this).html("<kbd>" + $(this).html() + "</kbd>"); });
        $("td.field-status").each(function() { $(this).html(render_status($(this).html())); });
        $("td.field-sequence").css("word-break", "break-all");
        $("td.field-sequence").each(function() { $(this).html('<code style="padding:0px; border-radius:0px;">' + $(this).html() + "</code>"); });

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Submission Date');
        $("th.column-job_id > div.text > a").html('<span class="glyphicon glyphicon-credit-card"></span>&nbsp;&nbsp;Job ID');
        $("th.column-tag > div.text > a").html('<span class="glyphicon glyphicon-tag"></span>&nbsp;&nbsp;Tag');
        $("th.column-status > div.text > a").html('<span class="glyphicon glyphicon-hourglass"></span>&nbsp;&nbsp;Status');
        $("th.column-sequence > div.text > a").html('<span class="glyphicon glyphicon-console"></span>&nbsp;&nbsp;Sequence');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-tint"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/sourcedownloader") != -1) {
        $("th.column-date").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-full_name").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-affiliation").addClass("col-lg-5 col-md-5 col-sm-5 col-xs-5");
        $("th.column-email").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");

        $("td.field-full_name").css("font-weight", "bold");
        $("td.field-email").css("text-decoration", "underline");

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Request Date');
        $("th.column-full_name > div.text > a").html('<span class="glyphicon glyphicon-credit-card"></span>&nbsp;&nbsp;Full Name');
        $("th.column-affiliation > div.text > a").html('<span class="glyphicon glyphicon-education"></span>&nbsp;&nbsp;Affiliation');
        $("th.column-email > div.text > a").html('<span class="glyphicon glyphicon-envelope"></span>&nbsp;&nbsp;Email');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-cloud-download"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/src/historyitem") != -1) {
        $("th.column-date").addClass("col-lg-3 col-md-3 col-sm-3 col-xs-3");
        $("th.column-content_html").addClass("col-lg-9 col-md-9 col-sm-9 col-xs-9");

        $("td.field-content_html").each(function() { $(this).html($(this).text()); });

        $("th.column-date > div.text > a").html('<span class="glyphicon glyphicon-calendar"></span>&nbsp;&nbsp;Display Date');
        $("th.column-content_html > div.text > a").html('<span class="glyphicon glyphicon-globe"></span>&nbsp;&nbsp;HTML Content');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-list-alt"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    } else if ($(location).attr("href").indexOf("admin/auth/user") != -1) {
        $("th.column-username").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-email").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-last_login").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-is_active").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-is_staff").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");
        $("th.column-is_superuser").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2");

        $("th.field-username").css("font-style", "italic");
        $("td.field-email").css("text-decoration", "underline");

        $("th.column-username > div.text > a").html('<span class="glyphicon glyphicon-user"></span>&nbsp;&nbsp;Username');
        $("th.column-email > div.text > a").html('<span class="glyphicon glyphicon-envelope"></span>&nbsp;&nbsp;Email Address');
        $("th.column-last_login > div.text > a").html('<span class="glyphicon glyphicon-time"></span>&nbsp;&nbsp;Last Login');
        $("th.column-is_active > div.text > a").html('<span class="glyphicon glyphicon-pawn"></span>&nbsp;&nbsp;Active');
        $("th.column-is_staff > div.text > a").html('<span class="glyphicon glyphicon-queen"></span>&nbsp;&nbsp;Staff');
        $("th.column-is_superuser > div.text > a").html('<span class="glyphicon glyphicon-king"></span>&nbsp;&nbsp;Admin');

        $("div.col-md-6 > h2.legend").html('<span class="glyphicon glyphicon-lock"></span>&nbsp;' + $("div.col-md-6 > h2.legend").html() + '<span class="pull-right" style="font-weight:normal; font-size: 12px;">(Click values in first column to edit)</span>');
    }

});


