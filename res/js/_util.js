$(document).ready(function () {

  var str_title = "Primerize: Primer Design for PCR Assembly";
  var path_icon = "/res/images/ico_primerize.png?";

  var path_logo_primerize = "/res/images/logo_primerize_2.png";
  var path_logo_das = "/res/images/logo_das.jpg";
  var path_logo_stanford = "/res/images/logo_stanford.png";
  var path_logo_eterna = "/res/images/logo_eterna_flat2.png";
  var path_background_rna = "/res/images/bg_rna.png";
  var path_button_loading = "/res/images/fg_load.gif";
  var path_button_top = "/res/images/fg_top.png";
  var path_button_question = "/res/images/fg_question.png";
  var path_background_404 = "/res/images/bg_404.png";
  var path_background_500 = "/res/images/bg_500.png";

  var path_pcr_ele = '/res/images/docs/PCR_electrophoresis.jpg';
  var path_pcr_gel = '/res/images/docs/PCR_gel.png';
  var path_tx_gel = '/res/images/docs/TX_gel.jpg';

  var path_home = "/home";
  var path_tutorial = "/tutorial";
  var path_protocol = "/protocol";
  var path_license = "/license";
  var path_download = "/download";
  var path_about = "/about";

  var path_design_1d = "/design_1d";
  var path_demo_1d = "/demo_1d_P4P6";

	var url = window.location.href;

  if (url.indexOf("design") > -1 || url.indexOf("example") > -1) {
    $("#nav_design").addClass("active");
  } else if (url.indexOf("tutorial") > -1) {
    $("#nav_tutorial").addClass("active");
  } else if (url.indexOf("protocol") > -1) {
    $("#nav_protocol").addClass("active");
  } else if (url.indexOf("about") > -1) {
    $("#nav_about").addClass("active");
  } else if (url.indexOf("download") > -1 || (url.indexOf("icense") > -1)) {
    $("#nav_download").addClass("active");
  } else {
    $("#nav_logo > span").css("text-decoration","underline");
  }

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
  $(".path_background_404").attr("src", path_background_404);
  $(".path_background_500").attr("src", path_background_500);

  $(".path_pcr_ele").attr("src", path_pcr_ele);
  $(".path_pcr_gel").attr("src", path_pcr_gel);
  $(".path_tx_gel").attr("src", path_tx_gel);

  $(".path_home").attr("href", path_home);
  $(".path_design_1d").attr("href", path_design_1d);
  $(".path_demo_1d").attr("href", path_demo_1d);
  $(".path_tutorial").each(function () {
    $(this).attr("href", path_tutorial + $(this).attr("href"));
  });
  $(".path_protocol").each(function () {
    $(this).attr("href", path_protocol + $(this).attr("href"));
  });
  $(".path_license").attr("href", path_license);
  $(".path_download").attr("href", path_download);
  $(".path_about").each(function () {
    $(this).attr("href", path_about + $(this).attr("href"));
  });

  $(".dropdown-toggle").dropdown();
  $(".dropdown").hover(
    function () { $(this).addClass('open') },
    function () { $(this).removeClass('open') }
  );
    
	$("[data-toggle='popover']").popover({trigger: "hover"});
	$("[data-toggle='tooltip']").tooltip();

});
