$(document).ready(function () {
  $('[id^=tab_], #up').on('click', function () {
    $('html, body').stop().animate({scrollTop: $($(this).attr("href")).offset().top - 75}, 500);
  });
        $("#sidebar").css("width", $("#sidebar").width());
      $("#sidebar").affix({
          offset: {
            top: $("#main").position().top
          }
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
});

