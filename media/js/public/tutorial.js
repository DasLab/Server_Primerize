function resize() {
  $("#main").addClass("pull-right");
  $("#sidebar").css("width", $("#navbar").width() - $("#main").width() - 30);

  if ($("#sidebar").width() < 200) {
    degree = 1;
    $("#side").removeClass("col-lg-2 col-md-2 col-sm-2 col-xs-2").addClass("row");
    $("#main").addClass("row").removeClass("pull-right");
    $("#sidebar").css("width", "auto").removeAttr("data-spy").removeClass("affix").removeClass("affix-top");
    $("#side_con").addClass("container");
  } else {
    $("#side").addClass("col-lg-2 col-md-2 col-sm-2 col-xs-2").removeClass("row");
    $("#main").removeClass("row").addClass("pull-right");
    $("#sidebar").attr("data-spy","affix").affix( { offset: { top: $("#main").position().top } } );
    $("#side_con").removeClass("container");

    if ($("#navbar").width() >= 1680) {
      $("#sidebar").css("width", ($("#navbar").width() - $("#main").width())/2 -25);
      // $("#side").css("padding-right","0px");
      // $("#side_con").css("padding-right","0px");
      $("#main").removeClass("pull-right").addClass("row");
      degree = 3;
    } else {
      $("#main").addClass("pull-right");
      $("#sidebar").css("width", ($("#navbar").width() - $("#main").width()) -25);
      degree = 2;
    }
  }

  // $("#mid-3").css("width", $("#mid-1").css("width"));
  // $("#mid-2").css("width", $("#mid-4").css("width"));

}

var degree = 0;

$(document).ready(function () {
  resize();

  $('[id^=tab_], #up').on('click', function () {
    $('html, body').stop().animate({scrollTop: $($(this).attr("href")).offset().top - 75}, 500);
  });

  $('ul.panel-collapse').on('show.bs.collapse', function () {
    $(this).parent().find("a>span.glyphicon.pull-right")
      .removeClass("glyphicon-triangle-bottom")
      .addClass("glyphicon-triangle-top");
  });
  $('ul.panel-collapse').on('hide.bs.collapse', function () {
    $(this).parent().find("a>span.glyphicon.pull-right")
      .removeClass("glyphicon-triangle-top")
      .addClass("glyphicon-triangle-bottom");
  });

});

$(window).on("scroll", function () {
	if ($(this).scrollTop() > $(window).height()/2) {
		$('#up').fadeIn();
	} else {
		$('#up').fadeOut();
	}
  if (degree == 1) {
    $("#sidebar").css("width", "auto").removeAttr("data-spy").removeClass("affix").removeClass("affix-top");
  }
});

$(window).on("resize", function() {
  clearTimeout($.data(this, 'resizeTimer'));
  $.data(this, 'resizeTimer', setTimeout(resize(), 200));
});

