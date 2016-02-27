$(document).ready(function () {
    if (flag == -1) {
        $("#message").addClass("alert-danger");
        $("#message").html('<span class="glyphicon glyphicon-remove-sign"></span>&nbsp;&nbsp;<b>ERROR</b>: Invalid contact information. Please try again.');
    } else if (flag == 1) {
        $("#id_first_name").attr("value", "");
        $("#id_last_name").attr("value", "");
        $("#id_institution").attr("value", "");
        $("#id_department").attr("value", "");
        $("#id_email").attr("value", "");
        $("#id_is_subscribe").attr("checked", "checked");

        $("#message").addClass("alert-success");
        $("#message").html('<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;<b class="lead">Your registration was successful.</b><br/>You will be notified about future Primerize updates depending on your subscription preference.<br/><br/>Your download should start automatically. If not, please <a id="a_dl" href="/site_data/Primerize-master.zip" target="_blank" download><i>click here</i>&nbsp;&nbsp;<span class="glyphicon glyphicon-floppy-save"></span></a>.');
        $("#a_dl")[0].click();
    }
});
