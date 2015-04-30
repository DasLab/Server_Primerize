$(document).ready(function () {
  $("#sidebar").css("width", $("#navbar").width() - $("#main").width() - 30);
  $("#sidebar").affix({
        offset: {
          top: $("#main").position().top
        }
  }); 

  $('[id^=tab_], #up').on('click', function () {
    $('html, body').stop().animate({scrollTop: $($(this).attr("href")).offset().top - 75}, 500);
  });

  $("#btn_demo").on('click', function () {
    $("#wait").fadeIn(1000);
  });
});

$(window).on("scroll", function () {
	if ($(this).scrollTop() > $(window).height()/2) {
		$('#up').fadeIn();
	} else {
		$('#up').fadeOut();
	}
});
