var gapi = {
    'gviz_handles': [],
    'fnFormatSize': function(bytes) {
        if      (bytes >= 1000000000) {bytes = (bytes / 1000000000).toFixed(2) + ' GB';}
        else if (bytes >= 1000000)    {bytes = (bytes / 1000000).toFixed(2) + ' MB';}
        else if (bytes >= 1000)       {bytes = (bytes / 1000).toFixed(2) + ' KB';}
        else if (bytes > 1)           {bytes = bytes + ' bytes';}
        else if (bytes == 1)          {bytes = bytes + ' byte';}
        else                          {bytes = '0 byte';}
        return bytes;
    },
    'fnRemovePlaceHolder': function() {
        $(".place_holder").each(function() {
            if ($(this).html().length > 0) { $(this).removeClass("place_holder"); }
        });
    },

    'fnRenderPage': function() {
        if (app.page == 'aws') {
            $.ajax({
                url : "/admin/dash/aws/?qs=init&sp=init&tqx=reqId%3A52",
                dataType: "json",
                success: function (data) {
                    $("#aws_table_body").parent().remove();

                    $("#table_ec2_id").html(data.ec2.id);
                    $("#table_ec2_type").html(data.ec2.instance_type);
                    $("#table_ec2_img").html(data.ec2.image_id);
                    $("#table_ec2_arch").html(data.ec2.architecture);
                    $("#table_ec2_vpc").html(data.ec2.vpc_id);
                    $("#table_ec2_subnet").html(data.ec2.subnet_id);
                    $("#table_ebs_type").html(data.ebs.type);
                    $("#table_ebs_id").html(data.ebs.id);
                    $("#table_ebs_size").html(data.ebs.size);
                    $("#table_ebs_snap").html(data.ebs.snapshot_id);
                    $("#table_ebs_zone").html(data.ebs.zone);
                    $("#table_elb_vpc").html(data.elb.vpc_id);
                    $("#table_elb_health").html(data.elb.health_check);

                    $("#table_elb_pns").html(data.elb.dns_name);
                    $("#table_elb_pns").parent().css("href", "http://" + data.elb.dns_name);
                    $("#table_ec2_pub_dns").html(data.ec2.public_dns_name);
                    $("#table_ec2_pub_dns").parent().css("href", "http://" + data.ec2.public_dns_name);
                    $("#table_ec2_prv_dns").html(data.ec2.private_dns_name);
                    $("#table_ec2_prv_dns").parent().css("href", "http://" + data.ec2.private_dns_name);
                }
            });


            var chart = new google.visualization.ChartWrapper({
                'chartType': 'ColumnChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=latency&sp=48h',
                'containerId': 'plot_lat1',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'none'},
                    'title': 'Last 48 Hours',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Milliseconds (ms)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true}
                    },
                    'bar': {'groupWidth': '500%' },
                    'colors': ['#8ee4cf'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=latency&sp=7d',
                'containerId': 'plot_lat2',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'none'},
                    'title': 'Last 7 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Milliseconds (ms)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM dd'
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#8ee4cf'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
                'chartType': 'ColumnChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=request&sp=48h',
                'containerId': 'plot_req1',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'none'},
                    'title': 'Last 48 Hours',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true}
                    },
                    'bar': {'groupWidth': '500%' },
                    'colors': ['#5496d7'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=request&sp=7d',
                'containerId': 'plot_req2',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'none'},
                    'title': 'Last 7 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM dd'
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#5496d7'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
                'chartType': 'ColumnChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=cpu&sp=48h',
                'containerId': 'plot_cpu1',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'none'},
                    'title': 'Last 48 Hours',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Percent (%)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true}
                    },
                    'bar': {'groupWidth': '500%' },
                    'colors': ['#c28fdd'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=cpu&sp=7d',
                'containerId': 'plot_cpu2',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'none'},
                    'title': 'Last 7 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Percent (%)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM dd'
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#c28fdd'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=host&sp=7d',
                'containerId': 'plot_host',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Last 7 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                        'viewWindow': {'max': 2, 'min': 0},
                        'ticks': [0, 1, 2]
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM dd'
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#50cc32', '#ff69bc'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=credit&sp=7d',
                'containerId': 'plot_credit',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Last 7 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                        'viewWindow': {'min': 0},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM dd'
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#ff5c2b', '#29be92'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=status&sp=7d',
                'containerId': 'plot_status',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Last 7 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                        'viewWindow': {'min': 0}
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM dd'
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#ff5c2b', '#ff69bc', '#ff912e'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=network&sp=7d',
                'containerId': 'plot_net',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Last 7 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Kilobytes/Second (kb/s)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM dd'
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#ff912e', '#3ed4e7'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=volbytes&sp=7d',
                'containerId': 'plot_vol',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Last 7 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Kilobytes/Second (kb/s)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM dd'
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#ff912e', '#3ed4e7'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=23xx&sp=7d',
                'containerId': 'plot_23xx',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Last 7 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM dd'
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#5496d7', '#29be92'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/aws/?qs=45xx&sp=7d',
                'containerId': 'plot_45xx',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Last 7 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM dd'
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#c28fdd', '#ff5c2b'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

        } else if (app.page == 'ga') {
            $.ajax({
                url : "/admin/dash/ga/?qs=init&tqx=reqId%3A52",
                dataType: "json",
                success: function (data) {
                    $("#br").html(data.bounceRate + ' %').removeClass('place_holder');
                    $("#br_prv").html(data.bounceRate_prev + ' %');
                    $("#u").html(data.users).removeClass('place_holder');
                    $("#u_prv").html(data.users_prev);
                    $("#sd").html(data.sessionDuration).removeClass('place_holder');
                    $("#sd_prv").html(data.sessionDuration_prev);
                    $("#s").html(data.sessions).removeClass('place_holder');
                    $("#s_prv").html(data.sessions_prev);
                    $("#pvs").html(data.pageviewsPerSession).removeClass('place_holder');
                    $("#pvs_prv").html(data.pageviewsPerSession_prev);
                    $("#pv").html(data.pageviews).removeClass('place_holder');
                    $("#pv_prv").html(data.pageviews_prev);
                },
                complete: function () {
                    var green = "#50cc32", red = "#ff5c2b";
                    if ($("#br_prv").html().indexOf('-') != -1) {
                        $("#br_prv_ico").html('<sup><span class="label label-green"><span class="glyphicon glyphicon-arrow-down"></span></span></sup>');
                        $("#br_prv").css("color", green);
                    } else {
                        $("#br_prv_ico").html('<sup><span class="label label-danger"><span class="glyphicon glyphicon-arrow-up"></span></span></sup>');
                        $("#br_prv").css("color", red);
                        $("#br_prv").html('+' + $("#br_prv").html());
                    }
                    if ($("#u_prv").html().indexOf('-') != -1) {
                        $("#u_prv_ico").html('<sup><span class="label label-green"><span class="glyphicon glyphicon-arrow-down"></span></span></sup>');
                        $("#u_prv").css("color", green);
                    } else {
                        $("#u_prv_ico").html('<sup><span class="label label-danger"><span class="glyphicon glyphicon-arrow-up"></span></span></sup>');
                        $("#u_prv").css("color", red);
                        $("#u_prv").html('+' + $("#u_prv").html());
                    }
                    if ($("#sd_prv").html().indexOf('-') != -1) {
                        $("#sd_prv_ico").html('<sup><span class="label label-green"><span class="glyphicon glyphicon-arrow-down"></span></span></sup>');
                        $("#sd_prv").css("color", green);
                    } else {
                        $("#sd_prv_ico").html('<sup><span class="label label-danger"><span class="glyphicon glyphicon-arrow-up"></span></span></sup>');
                        $("#sd_prv").css("color", red);
                        $("#sd_prv").html('+' + $("#sd_prv").html());
                    }
                    if ($("#s_prv").html().indexOf('-') != -1) {
                        $("#s_prv_ico").html('<sup><span class="label label-green"><span class="glyphicon glyphicon-arrow-down"></span></span></sup>');
                        $("#s_prv").css("color", green);
                    } else {
                        $("#s_prv_ico").html('<sup><span class="label label-danger"><span class="glyphicon glyphicon-arrow-up"></span></span></sup>');
                        $("#s_prv").css("color", red);
                        $("#s_prv").html('+' + $("#s_prv").html());
                    }
                    if ($("#pvs_prv").html().indexOf('-') != -1) {
                        $("#pvs_prv_ico").html('<sup><span class="label label-green"><span class="glyphicon glyphicon-arrow-down"></span></span></sup>');
                        $("#pvs_prv").css("color", green);
                    } else {
                        $("#pvs_prv_ico").html('<sup><span class="label label-danger"><span class="glyphicon glyphicon-arrow-up"></span></span></sup>');
                        $("#pvs_prv").css("color", red);
                        $("#pvs_prv").html('+' + $("#pvs_prv").html());
                    }
                    if ($("#pv_prv").html().indexOf('-') != -1) {
                        $("#pv_prv_ico").html('<sup><span class="label label-green"><span class="glyphicon glyphicon-arrow-down"></span></span></sup>');
                        $("#pv_prv").css("color", green);
                    } else {
                        $("#pv_prv_ico").html('<sup><span class="label label-danger"><span class="glyphicon glyphicon-arrow-up"></span></span></sup>');
                        $("#pv_prv").css("color", red);
                        $("#pv_prv").html('+' + $("#pv_prv").html());
                    }
                }
            });

            var chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/ga/?qs=chart&sp=24h',
                'containerId': 'chart_24h',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'none'},
                    'title': 'Last 24 Hours',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true}
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#c28fdd'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/ga/?qs=chart&sp=7d',
                'containerId': 'chart_7d',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'none'},
                    'title': 'Last 7 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true}
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#d86f5c'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/ga/?qs=chart&sp=1m',
                'containerId': 'chart_1m',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'none'},
                    'title': 'Last 30 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true}
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#ff912e'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/ga/?qs=chart&sp=3m',
                'containerId': 'chart_3m',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'none'},
                    'title': 'Last 90 Days',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true}
                    },
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#29be92'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
                'chartType': 'PieChart',
                'dataSourceUrl': '/admin/dash/ga/?qs=pie&sp=session',
                'containerId': 'pie_session',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Sessions',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'pieHole': 0.33,
                    'colors': ['#50cc32', '#ff69bc'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'PieChart',
                'dataSourceUrl': '/admin/dash/ga/?qs=pie&sp=user',
                'containerId': 'pie_user',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Visitors',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'pieHole': 0.33,
                    'colors': ['#3ed4e7', '#ff912e'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'PieChart',
                'dataSourceUrl': '/admin/dash/ga/?qs=pie&sp=browser',
                'containerId': 'pie_browser',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Browser',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'pieHole': 0.33,
                    'colors': ['#29be92', '#ff912e', '#5496d7', '#ff5c2b'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
            chart = new google.visualization.ChartWrapper({
                'chartType': 'PieChart',
                'dataSourceUrl': '/admin/dash/ga/?qs=pie&sp=pageview',
                'containerId': 'pie_pageview',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Page Views',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'pieHole': 0.33,
                    'colors': ['#8ee4cf', '#c28fdd'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
                'chartType': 'GeoChart',
                'dataSourceUrl': '/admin/dash/ga/?qs=geo',
                'containerId': 'geo_session',
                'options': {
                    'height': 300,
                    'displayMode': 'regions',
                    'legend': {'position': 'bottom'},
                    'title': 'Sessions',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'colors': ['#ddf6f0','#5496d7'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

        } else if (app.page == 'git') {
            $.ajax({
                url : "/admin/dash/git/?qs=init&tqx=reqId%3A52",
                dataType: "json",
                success: function (data) {
                    var html = "";
                    for (var i = 0; i < data.contrib.length; i++) {
                        html += '<tr><td>' + data.contrib[i].Contributors + '</td><td><span class="pull-right" style="color:#00f;">' + data.contrib[i].Commits + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#080;">' + data.contrib[i].Additions + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></td><td><span class="pull-right" style="color:#f00;">' + data.contrib[i].Deletions + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></td></tr>';
                    }
                    html += '<tr><td colspan="4" style="padding: 0px;"></td></tr>';
                    $("#git_table_body").html(html).removeClass('place_holder');
                }
            });

            $.ajax({
                url : "/admin/dash/git/?qs=num&tqx=reqId%3A53",
                dataType: "json",
                success: function (data) {
                    $("#git_num_body").html('<tr><td><span class="label label-green">created</span></td><td><span class="label label-primary">' + data.created_at + '</span></td></tr><tr><td><span class="label label-dark-green">last pushed</span></td><td><span class="label label-primary">' + data.pushed_at + '</span></td></tr><tr><td><span class="label label-danger">issue</span></td><td>' + data.num_issues + '</td></tr><tr><td><span class="label label-info">download</span></td><td>' + data.num_downloads + '</td></tr><tr><td><span class="label label-info">pull</span></td><td>' + data.num_pulls + '</td></tr><tr><td><span class="label label-orange">branch</span></td><td>' + data.num_branches + '</td></tr><tr><td><span class="label label-orange">fork</span></td><td>' + data.num_forks + '</td></tr><tr><td><span class="label label-violet">watcher</span></td><td>' + data.num_watchers + '</td></tr><tr><td colspan="2" style="padding: 0px;"></td></tr>').removeClass('place_holder');
                }
            });

            var chart = new google.visualization.ChartWrapper({
                'chartType': 'Calendar',
                'dataSourceUrl': '/admin/dash/git/?qs=c',
                'containerId': 'plot_c',
                'options': {
                    'title': 'Last Year',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'calendar': {
                        'cellColor': {'stroke': '#fff'},
                        'underYearSpace': 20,
                        'yearLabel': {'color': '#c28fdd', 'bold': true},
                        'monthLabel': {'color': '#000'},
                        'monthOutlineColor': {'stroke': '#d86f5c', 'strokeOpacity': 0.8, 'strokeWidth': 2},
                        'dayOfWeekLabel': {'color': '#000'}
                    },
                    'colorAxis': {
                        'values': [0, 3, 6, 9, 12],
                        'colors': ['#f8f8f8', '#fae621', '#5cc861', '#23888d', '#3a518a']
                    },
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
                'chartType': 'AreaChart',
                'dataSourceUrl': '/admin/dash/git/?qs=ad',
                'containerId': 'plot_ad',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Weekly Aggregation',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'vAxis': {
                        'title': 'Count (#)',
                        'titleTextStyle': {'bold': true},
                        'scaleType': 'mirrorLog',
                        'format': 'scientific',
                        'gridlines': {'count': 5}
                    },
                    'hAxis': {
                        'gridlines': {'count': -1},
                        'textStyle': {'italic': true},
                        'format': 'MMM yy'
                    },
                    'tooltip': {'showColorCode': true},
                    'focusTarget': 'category',
                    'lineWidth': 3,
                    'pointSize': 5,
                    'colors': ['#29be92', '#ff5c2b'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);

            chart = new google.visualization.ChartWrapper({
                'chartType': 'PieChart',
                'dataSourceUrl': '/admin/dash/git/?qs=au',
                'containerId': 'plot_pie',
                'options': {
                    'chartArea': {'width': '90%', 'left': '10%'},
                    'legend': {'position': 'bottom'},
                    'title': 'Contributors Commits',
                    'titleTextStyle': {'bold': false, 'fontSize': 16},
                    'pieHole': 0.33,
                    'colors': ['#3ed4e7', '#ff912e', '#29be92', '#ff5c2b'],
                    'animation': {'startup': true, 'duration': 1000, 'easing': 'inAndOut'}
                }
            });
            google.visualization.events.addListener(chart, 'ready', gapi.fnRemovePlaceHolder);
            chart.draw();
            gapi.gviz_handles.push(chart);
        }
    }
};

var gapi_callback = setTimeout(function() {
    if (google.charts) {
        clearTimeout(gapi_callback);
        $("#view-selector-container").hide();
        gapi.fnRenderPage();
    }
}, 1000);


$(window).on("resize", throttle(function() {
    for (var i = 0; i < gapi.gviz_handles.length; i++) {
        gapi.gviz_handles[i].draw();
    }
}, 200, 1000));
