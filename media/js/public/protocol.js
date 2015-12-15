$(document).ready(function () {
  $("#calc_DNA").on('click', function () {
    var A260 = $("#A260_DNA").val(),
      l = $("#l_DNA").val();
    $("#conc_DNA").val(parseFloat(A260) * 50000 / 660 / parseInt(l) );
  });
  $("#clc_DNA").on('click', function () {
    $("#A260_DNA").val('');
    $("#l_DNA").val('');
    $("#conc_DNA").val('');
  });

  $("#calc_RNA").on('click', function () {
    var A260 = $("#A260_RNA").val(),
      l = $("#l_RNA").val();
    $("#conc_RNA").val(parseFloat(A260) * 40000 / 330 / parseInt(l) );
  });
  $("#clc_RNA").on('click', function () {
    $("#A260_RNA").val('');
    $("#l_RNA").val('');
    $("#conc_RNA").val('');
  });


  var unit = parseInt($("#par_plate_final1").width() / 33);
  cell_radius = unit, cell_stroke = unit / 5, tick_width = unit * 3;

  $.ajax({
    url: '/site_media/images/docs/par_plate_final.json',
    dataType: "json",
    success: function(data) {
      draw_single_plate(d3.select("#par_plate_final1"), data.data, false);
      draw_single_plate(d3.select("#par_plate_final2"), data.data, false);
    }
  });
  $.ajax({
    url: '/site_media/images/docs/par_plate_primer1.json',
    dataType: "json",
    success: function(data) { draw_single_plate(d3.select("#par_plate_primer1"), data.data, false); }
  });
  $.ajax({
    url: '/site_media/images/docs/par_plate_primer2.json',
    dataType: "json",
    success: function(data) { draw_single_plate(d3.select("#par_plate_primer2"), data.data, false); }
  });
  $.ajax({
    url: '/site_media/images/docs/par_plate_primer3.json',
    dataType: "json",
    success: function(data) { draw_single_plate(d3.select("#par_plate_primer3"), data.data, false); }
  });
  $.ajax({
    url: '/site_media/images/docs/par_plate_primer4.json',
    dataType: "json",
    success: function(data) { draw_single_plate(d3.select("#par_plate_primer4"), data.data, false); }
  });
  $.ajax({
    url: '/site_media/images/docs/par_plate_primer1_filled.json',
    dataType: "json",
    success: function(data) { draw_single_plate(d3.select("#par_plate_primer1_filled"), data.data, false); }
  });
  $.ajax({
    url: '/site_media/images/docs/par_plate_primer2_filled.json',
    dataType: "json",
    success: function(data) { draw_single_plate(d3.select("#par_plate_primer2_filled"), data.data, false); }
  });
  $.ajax({
    url: '/site_media/images/docs/par_plate_primer3_filled.json',
    dataType: "json",
    success: function(data) { draw_single_plate(d3.select("#par_plate_primer3_filled"), data.data, false); }
  });
  $.ajax({
    url: '/site_media/images/docs/par_plate_primer4_filled.json',
    dataType: "json",
    success: function(data) { draw_single_plate(d3.select("#par_plate_primer4_filled"), data.data, false); }
  });
  $.ajax({
    url: '/site_media/images/docs/par_plate_helper.json',
    dataType: "json",
    success: function(data) { draw_single_plate(d3.select("#par_plate_helper"), data.data, false); }
  });





});

