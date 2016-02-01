var scrollTimer, resizeTimer;

$(document).ready(function () {
  $("#wait").fadeOut(500);
  var today = new Date();
  $("#cp_year").text(today.getFullYear());

  $(".dropdown-toggle").dropdown();
  $(".dropdown").hover(
    function(){ $(this).addClass("open"); },
    function(){ $(this).removeClass("open"); }
  );
  $("[data-toggle='popover']").popover({trigger: "hover"});
  $("[data-toggle='tooltip']").tooltip();

  $("#top").on("click", function () {
    event.preventDefault();
    $('#top > img').animate({'left':'-5%', 'opacity':'0'}, 125);
    $("html, body").stop().animate({scrollTop: 0}, 250);
  });
  $("#top").hover(
    function(){ $("#top > img").attr("src", "/site_media/images/fg_top.png"); },
    function(){ $("#top > img").attr("src", "/site_media/images/fg_top_hover.png"); }
  );

  var url = window.location.href;

  if (url.indexOf("design") > -1 || url.indexOf("example") > -1) {
    $("#nav_design").addClass("active");
  } else if (url.indexOf("tutorial") > -1) {
    $("#nav_tutorial").addClass("active");
  } else if (url.indexOf("protocol") > -1) {
    $("#nav_protocol").addClass("active");
  } else if (url.indexOf("about") > -1) {
    $("#nav_about").addClass("active");
  } else if (url.indexOf("download") > -1 || (url.indexOf("icense") > -1) || (url.indexOf("docs") > -1)) {
    $("#nav_code").addClass("active");
  } else {
    $("#nav_logo > span").css("text-decoration", "underline");
  }
});

$(window).on("beforeunload", function () {
  $("#wait").fadeIn(250);
});
$(window).on("scroll", function () {
  clearTimeout($.data(this, 'scrollTimer'));
  $.data(this, 'scrollTimer', setTimeout(function() {
    if ($(this).scrollTop() > $(window).height() / 2) {
      $('#top > img').animate({'left':'0%', 'opacity':'1.0'}, 125);
    } else {
      $('#top > img').animate({'left':'-5%', 'opacity':'0'}, 125);
    }
  }, 200));
});


function resize() {
  $("#col-res-l").css("height", "auto");
  $("#col-res-r").css("height", "auto");

  var col_h = Math.max(parseInt($("#col-res-l").css("height")), parseInt($("#col-res-r").css("height")));
  $("#col-res-l").css("height", col_h);
  $("#col-res-r").css("height", col_h);
}

$(window).on("resize", function() {
  clearTimeout($.data(this, 'resizeTimer'));
  $.data(this, 'resizeTimer', setTimeout(resize(), 200));
});
