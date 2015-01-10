$(document).ready(function () {
  $('#up').on('click', function (e) {
    e.preventDefault();
    $('html, body').stop().animate({scrollTop: $('#down').offset().top}, 500);
  });
  $('#tab_1').on('click', function (e) {
    e.preventDefault();
    $('html, body').stop().animate({scrollTop: $('#web_input').offset().top}, 500);
  });
  $('#tab_2').on('click', function (e) {
    e.preventDefault();
    $('html, body').stop().animate({scrollTop: $('#web_output_primers').offset().top}, 500);
  });
  $('#tab_3').on('click', function (e) {
    e.preventDefault();
    $('html, body').stop().animate({scrollTop: $('#web_output_assembly').offset().top}, 500);
  });
  $('#tab_4').on('click', function (e) {
    e.preventDefault();
    $('html, body').stop().animate({scrollTop: $('#txt_output').offset().top}, 500);
  });
  $('#tab_5').on('click', function (e) {
    e.preventDefault();
    $('html, body').stop().animate({scrollTop: $('#idt_bulk').offset().top}, 500);
  });
  $('#tab_6').on('click', function (e) {
    e.preventDefault();
    $('html, body').stop().animate({scrollTop: $('#PCR').offset().top}, 500);
  });

  $("#btn_demo").on('click', function () {
    $("#wait").fadeIn(1000);
  });
});