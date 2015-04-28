$(document).ready(function () {
  $('[id^=tab_], #up').on('click', function () {
    $('html, body').stop().animate({scrollTop: $($(this).attr("href")).offset().top - 50}, 500);
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
