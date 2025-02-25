var throttle = function(func, delay, at_least) {
  var timer = null, previous = null;
  return function() {
    var now = +new Date();
    if (!previous) { previous = now; }
    if (now - previous > at_least) {
      func();
      previous = now;
    } else {
      clearTimeout(timer);
      timer = setTimeout(func, delay);
    }
  };
};

app.fnParseLocation = function() {
  var urls = {
    "design": ["design_1d", "design_2d", "design_3d", "demo_1d", "demo_2d", "demo_3d", "design_2d_from_1d", "design_3d_from_1d", "design_3d_from_2d", "result"],
    "tutorial": ["tutorial"],
    "protocol": ["protocol"],
    "about": ["about"],
    "code": ["download", "docs", "license"]
  };
  app.page = window.location.pathname.replace(/\/$/, '').replace(/^\//, '');
  for (var key in urls) {
      if (urls[key].indexOf(app.page) != -1) {
          app.key = key;
          return;
      }
  }
  app.key = 'home';
};

app.fnChangeView = function() {
  app.fnParseLocation();
  $("#nav > li.dropdown.active, #nav_home").removeClass("active");
  $("#nav_"+ app.key).addClass("active");

  $.getScript('/site_media/js/public/' + app.DEBUG_DIR + 'page' + app.DEBUG_STR + '.js', function(data, code, xhr) {
    $("#content").fadeTo(150, 1);
    if (window.location.hash) { $('html, body').stop().animate({"scrollTop": $(window.location.hash).offset().top - 75}, 500); }
    if (typeof app.callbackChangeView === "function") { app.callbackChangeView(); }
  });

  $("[data-toggle='popover']").popover({trigger: "hover"});
  $("[data-toggle='tooltip']").tooltip();
};

app.fnChangeLocation = function() {
  if (window.history.pushState) {
    window.history.pushState(null , null, app.href);
  } else {
      window.location.href = app.href;
  }
  $("html, body").scrollTop(0);
  $("#content").load(app.href + " #content > *", app.fnChangeView);
};


$(document).ready(function() {
  var today = new Date();
  $("#cp_year").text(today.getFullYear());

  $(".dropdown-toggle").dropdown();
  $(".dropdown").hover(
    function(){ $(this).addClass("open"); },
    function(){ $(this).removeClass("open"); }
  );

  $("#top").on("click", function() {
    event.preventDefault();
    $('#top > div').animate({'right':'-5%', 'opacity':'0'}, 125);
    $("html, body").stop().animate({"scrollTop": 0}, 250);
  });

  $("#nav > li:not(#nav_code) > a, #nav > li:not(#nav_code) li > a, #nav_home").on("click", function(event) {
      event.preventDefault();
      app.href = $(this).attr("href");
      $("#content").fadeTo(100, 0, app.fnChangeLocation);
  });

  $("#navbar").css({"opacity": 1, "top": "-50px"}).animate({"top": "0px"}, {"duration": 200, "queue": false, "complete": app.fnChangeView});
});


$(window).on("scroll", throttle(function() {
  if ($(this).scrollTop() > $(window).height() / 2) {
    $('#top > div').animate({'right': '5%', 'opacity': 0.85}, 125);
  } else {
    $('#top > div').animate({'right': '-5%', 'opacity': 0}, 125);
  }
}, 200, 500));

window.onpopstate = function() { location.reload(); };

