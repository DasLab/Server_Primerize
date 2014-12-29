$(document).ready(function () {

  $("#license_content").load("/LICENSE.md", function (txt) {
    $(this).html(txt.split(/\n/).join("<br>") + "</strong>");
  });

});
