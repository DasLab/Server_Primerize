function resize() {
  $("#main").addClass("pull-right");
  $("#sidebar").css("width", $("#navbar").width() - $("#main").width() - 30);
  $("#sidebar").affix({
        offset: {
          top: $("#main").position().top
        }
  }); 
  if ($("#navbar").width() > 1500) {
    $("#main").removeClass("pull-right");
  } else {
    $("#main").addClass("pull-right");
  }
  $("#sidebar").css("max-width", 300);  
}


$(document).ready(function () {
  resize();

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

$(window).on("resize", function() {
  clearTimeout($.data(this, 'resizeTimer'));
  $.data(this, 'resizeTimer', setTimeout(resize(), 200));
});

