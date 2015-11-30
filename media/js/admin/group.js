$.ajax({
    url : "/admin/group_dash",
    dataType: "json",
    success: function (data) {
        var html = '<table class="table table-hover"><thead><tr class="active"><th class="col-lg-3 col-md-3 col-sm-3 col-xs-3"><span class="glyphicon glyphicon-th-list"></span>&nbsp;&nbsp;Group</th><th class="col-lg-9 col-md-9 col-sm-9 col-xs-9"><span class="glyphicon glyphicon-credit-card"></span>&nbsp;&nbsp;SUNet IDs</th></tr></thead><tbody><tr><td><span class="label label-violet"><span class="glyphicon glyphicon-king"></span>&nbsp;&nbsp;Administrator</span></td><td>';
        for (var i = 0; i < data.admin.length; i++) {
            html += '<kbd>' + data.admin[i] + '</kbd>&nbsp;';
        }
        html += '</td></tr><tr class="active"><td><span class="label label-green"><span class="glyphicon glyphicon-queen"></span>&nbsp;&nbsp;Current Member</span></td><td>';
        for (var i = 0; i < data.group.length; i++) {
            html += '<kbd>' + data.group[i] + '</kbd>&nbsp;';
        }
        html += '</td></tr><tr><td><span class="label label-info"><span class="glyphicon glyphicon-pawn"></span>&nbsp;&nbsp;Alumni Member</span></td><td>';
        for (var i = 0; i < data.alumni.length; i++) {
            html += '<kbd>' + data.alumni[i] + '</kbd>&nbsp;';
        }
        html += '</td></tr><tr class="active"><td><span class="label label-orange"><span class="glyphicon glyphicon-bishop"></span>&nbsp;&nbsp;Rotation Student</span></td><td>';
        for (var i = 0; i < data.roton.length; i++) {
            html += '<kbd>' + data.roton[i] + '</kbd>&nbsp;';
        }
        html += '</td></tr><tr><td><span class="label label-magenta"><span class="glyphicon glyphicon-knight"></span>&nbsp;&nbsp;Visitor</span></td><td>';
        for (var i = 0; i < data.other.length; i++) {
            html += '<kbd>' + data.other[i] + '</kbd>&nbsp;';
        }
        html += '</td></tr><tr><td colspan="2" style="padding: 0px;"></td></tr></tbody></table>';
        $("#changelist-form").append($(html));

    }
});


