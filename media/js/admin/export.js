$(document).ready(function() {
	// $("#iframe").css("width", parseInt($("#content").css("width")) - 50);
	// $("#iframe").css("height", $("#footer").position().top - $("#content").position().top - 175);
	$("ul.breadcrumb").append('<li class="active"><span style="color: #000;" class="glyphicon glyphicon-floppy-save"></span>&nbsp;&nbsp;Publication Export</li>');
	$("ul[id^=id_]").css("list-style-type", "none");

	$("[id^=id_text_type]").on("change", function() {
		if ($(this).is(":checked")) {
			if ($(this).attr("id").indexOf("_0") != -1) {
				$("#id_bold_author, #id_bold_year, #id_underline_title, #id_italic_journal, #id_bold_volume").attr("disabled", "disabled");
				$("[class^=item_]").css({"font-weight":"normal", "font-style":"normal", "text-decoration":"none"})
			} else {
				$("#id_bold_author, #id_bold_year, #id_underline_title, #id_italic_journal, #id_bold_volume").removeAttr("disabled");
				$("#id_bold_author, #id_bold_year, #id_underline_title, #id_italic_journal, #id_bold_volume").trigger("change");
			}
		}
	});

	$("[id^=id_sort_order]").on("change", function() {
		if ($(this).is(":checked")) {
			if ($(this).attr("id").indexOf("_0") != -1) {
				$("#prv_item_1").detach().insertAfter($("#prv_item_3"));
				$("#prv_item_2").detach().insertAfter($("#prv_item_3"));
				$("[id^=id_number_order]").trigger("change");
			} else {
				$("#prv_item_1").detach().insertBefore($("#prv_item_3"));
				$("#prv_item_2").detach().insertBefore($("#prv_item_3"));
				$("[id^=id_number_order]").trigger("change");

			}
		}
	});
	$("[id^=id_number_order]").on("change", function() {
		if ($(this).is(":checked") && $("#id_order_number").is(":checked")) {
			if ($(this).attr("id").indexOf("_0") != -1) {
				var list = $("[id^=prv_item_]>span.item_num");
				for (var i = 0; i < list.length; i++) {
					$(list[i]).html((i + 1).toString() + '.');
				}
			} else {
				var list = $("[id^=prv_item_]>span.item_num");
				for (var i = 0; i < list.length; i++) {
					$(list[i]).html((list.length - i).toString() + '.');
				}
			}
		}
	});
	$("#id_order_number").on("change", function() {
		$(".item_num").toggle();
		$("[id^=id_number_order]").trigger("change");
	});
	$("[id^=id_number_order]").trigger("change");

	$(".item_das").css("font-weight", "bold");
	$("#id_bold_author").on("change", function() {
		if ($("#id_bold_author").is(":checked")) {
			$(".item_das").css("font-weight", "bold");
		} else {
			$(".item_das").css("font-weight", "normal");
		}
	});
	$(".item_year").css("font-weight", "bold");
	$("#id_bold_year").on("change", function() {
		if ($("#id_bold_year").is(":checked")) {
			$(".item_year").css("font-weight", "bold");
		} else {
			$(".item_year").css("font-weight", "normal");
		}
	});
	$(".item_quote").css("display", "inline-block");
	$("#id_quote_title").on("change", function() {
		if ($("#id_quote_title").is(":checked")) {
			$(".item_quote").css("display", "inline-block");
		} else {
			$(".item_quote").css("display", "none");
		}
	});
	$(".item_title").css("text-decoration", "underline");
	$("#id_underline_title").on("change", function() {
		if ($("#id_underline_title").is(":checked")) {
			$(".item_title").css("text-decoration", "underline");
		} else {
			$(".item_title").css("text-decoration", "none");
		}
	});
	$(".item_journal").css("font-style", "italic");
	$("#id_italic_journal").on("change", function() {
		if ($("#id_italic_journal").is(":checked")) {
			$(".item_journal").css("font-style", "italic");
		} else {
			$(".item_journal").css("font-style", "normal");
		}
	});
	$(".item_volume").css("font-weight", "bold");
	$("#id_bold_volume").on("change", function() {
		if ($("#id_bold_volume").is(":checked")) {
			$(".item_volume").css("font-weight", "bold");
		} else {
			$(".item_volume").css("font-weight", "normal");
		}
	});
	$("#id_double_space").on("change", function() {
		if ($("#id_double_space").is(":checked")) {
			$("[id^=prv_item_]").each( function() {
				$('<br class="item_br"/>').insertAfter($(this));
			});
		} else {
			$(".item_br").remove();
		}
	});

	$("#export_save, #export_view").on("click", function() {$(window).unbind();});
});


