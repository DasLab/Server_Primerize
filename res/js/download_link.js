$(document).ready(function () {

  $("#first_name").attr("value", "");
  $("#last_name").attr("value", "");
  $("#inst").attr("value", "");
  $("#dept").attr("value", "");
  $("#email").attr("value", "");
  $("#is_subscribe").attr("checked", "checked");

  $("#message").attr("class", "alert alert-success");
  $("#message").html("<b class=\"lead\">Your registration was successful.</b><br/>You will be notified about future Primerize updates depending on your subscription preference.<br/><br/>Your download should start automatically. If not, please <a href=\"/src/primerize_release.zip\"><i>click here</i></a>.");

  $("head").append("<meta http-equiv=\"refresh\" content=\"1;url=/src/primerize_release.zip\">");

});
