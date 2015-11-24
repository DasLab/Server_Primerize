$(document).ready(function () {
	$("#id_first_name").addClass("form-control");
	$("#id_last_name").addClass("form-control");
	$("#id_institution").addClass("form-control");
	$("#id_department").addClass("form-control");
	$("#id_email").addClass("form-control");

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
		$("#message").html('<span class="glyphicon glyphicon-ok-sign"></span>&nbsp;&nbsp;<b class="lead">Your registration was successful.</b><br/>You will be notified about future Primerize updates depending on your subscription preference.<br/><br/>Your download should start automatically. If not, please <a href="/site_data/primerize_release.zip"><i>click here</i>&nbsp;&nbsp;<span class="glyphicon glyphicon-floppy-save"></span></a>.');
		$("head").append('<meta http-equiv="refresh" content="1;url=/site_data/primerize_release.zip">');
	}
});
