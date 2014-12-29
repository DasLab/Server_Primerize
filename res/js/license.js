$(document).ready(function () {

  $("#license_content").load("/LICENSE.md", function (txt) {
    $(this).html(function () {
      return txt.split(/\n/).join("<br>") + "</strong>";
    });
  });

});
