$(document).ready(function () {

  var str_title = "Primerize: Primer Design for PCR Assembly";
  var path_icon = "/res/images/ico_primerize.png?";

  var path_logo_primerize = "/res/images/logo_primerize.png?";
  var path_logo_das = "/res/images/logo_das.jpg?";
  var path_logo_stanford = "/res/images/logo_stanford.png?";
  var path_logo_eterna = "/res/images/logo_eterna.png?";
  var path_background_rna = "/res/images/bg_rna.png?";
  var path_button_loading = "/res/images/fg_load.gif?";
  var path_button_top = "/res/images/fg_top.png?";
  var path_button_question = "/res/images/fg_question.png?";

  var path_home = "/res/html/index.html?";
  var path_design = "/res/html/design.html?";
  var path_tutorial = "/res/html/tutorial.html?";
  var path_download = "/res/html/download.html?";
  var path_downlink = "/res/html/download_link.htm?l";
  var path_about = "/res/html/about.html?";
  var path_navbar = "/res/html/_navbar.html?";
  var path_footer = "/res/html/_footer.html?";
  
	var url = window.location.href;

  $("#navbar").load(path_navbar, function () {
    if (url.indexOf("Design") > -1 || url.indexOf("example") > -1) {
      $("#nav_design").addClass("active");
    } else if (url.indexOf("Tutorial") > -1) {
      $("#nav_tutorial").addClass("active");
    } else if (url.indexOf("About") > -1) {
      $("#nav_about").addClass("active");
    } else if (url.indexOf("Download") > -1 || (url.indexOf("icense") > -1)) {
      $("#nav_download").addClass("active");
    } else {
    $("#nav_logo").css("text-decoration","underline");
    }

    $("#footer").load(path_footer, function () {
      document.title = str_title;
      $("#favicon").attr("href", path_icon + "?");
      var today = new Date();
      $("#cp_year").text(today.getFullYear());
      
      $(".path_logo_primerize").attr("src", path_logo_primerize);
      $(".path_logo_das").attr("src", path_logo_das);
      $(".path_logo_stanford").attr("src", path_logo_stanford);
      $(".path_logo_eterna").attr("src", path_logo_eterna);
      $(".path_background_rna").attr("src", path_background_rna);
      $(".path_button_loading").attr("src", path_button_loading);
      $(".path_button_top").attr("src", path_button_top);
      $(".path_button_question").attr("src", path_button_question);

      $(".path_home").attr("href", path_home);
      $(".path_design").attr("href", path_design);
      $(".path_tutorial").attr("href", path_tutorial);
      $(".path_download").attr("href", path_download);
      $(".path_downlink").attr("href", path_downlink);
      $(".path_about").attr("href", path_about);

      $(".bgimg").css("background-image", 'url("' + path_background_rna + '")');
      $(".navbar .navbar-brand").css("background-image", 'url("' + path_background_rna + '")');
      $(".modal").css("background-image", 'url("' + path_button_loading + '")');

    });
  });
    
	$("[data-toggle='popover']").popover({trigger: "hover"}); 
	$("[data-toggle='tooltip']").tooltip(); 

});
