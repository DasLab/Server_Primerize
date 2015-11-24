$(document).ready(function () {
	result_data['params'] = JSON.parse(result_data['params']);
	$("#id_sequence").val(result_data['sequence']);
	$("#id_tag").val(result_data['tag']);
	$("#id_min_Tm").val(result_data['params']['min_Tm']);
	$("#id_max_len").val(result_data['params']['max_len']);
	$("#id_min_len").val(result_data['params']['min_len']);
	$("#id_num_primers").val(result_data['params']['num_primers']);
	$("#id_is_num_primers").prop("checked", result_data['params']['is_num_primers']);
	$("#id_is_check_t7").prop("checked", result_data['params']['is_check_t7']);

	track_input_length();
	if ($("#id_is_num_primers").is(":checked")) {
		$("#id_num_primers").removeAttr("disabled");
	} else {
		$("#id_num_primers").attr("disabled", "disabled");
	}
	$("#result").load('/site_data/1d/result_' + result_job_id + '.html');
});

