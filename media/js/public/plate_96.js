var cell_radius = 7, cell_stroke = 1.4, tick_width = 20;
var tooltip_timer;
var x_data = d3.range(1, 13), y_data = 'ABCDEFGH'.split('');
var tooltip = d3.select("body").append("div")
                .attr("class", "svg_tooltip")
                .style("opacity", 0);


function get_coord_y(num) {
    var y = (num - 1) % 8 + 1;
    return y * (cell_stroke + cell_radius * 2);
}

function get_coord_x(num) {
    var x = Math.floor((num - 1) / 8) + 1;
    return x * (cell_stroke + cell_radius * 2);
}

function get_stroke_color(d) {
    if (d.color) {
        if (d.color == 'blue') {
            return '#3ed4e7';
        } else if (d.color == 'orange') {
            return '#ff912e';
        } else if (d.color == 'magenta') {
            return '#ff69bc';
        } else if (d.color == 'primary') {
            return '#5496d7';
        } else if (d.color == 'default') {
            return '#a19193';
        } else if (d.color == 'danger') {
            return '#ff5c2b';
        } else if (d.color == 'green') {
            return '#29be92';
        }
    } else if (d.label) {
        if (d.label.indexOf("WT") != -1) {
            return "#29be92";
        } else {
            return "#c28fdd";
        }
    } else {
        return "#333";
    }
}

function get_fill_color(d) {
    if (d.color) {
        if (d.color == 'blue') {
            return '#c5f2f7';
        } else if (d.color == 'orange') {
            return '#ffdec0';
        } else if (d.color == 'magenta') {
            return '#ffd2ea';
        } else if (d.color == 'primary') {
            return '#cbdff3';
        } else if (d.color == 'default') {
            return '#f5f5f5';
        } else if (d.color == 'danger') {
            return '#ffcebf';
        } else if (d.color == 'green') {
            return '#beebde';
        }
    } else if (d.label) {
        if (d.label.indexOf("WT") != -1) {
            return "#beebde";
        } else {
            return "#ecddf4";
        }
    } else {
        return "#fff";
    }
}

function draw_single_plate(element, data, flag) {
    var svg = element.append("svg")
        .attr("width", (cell_stroke + cell_radius * 2) * 12.5 + tick_width + 1)
        .attr("height", (cell_stroke + cell_radius * 2) * 8.5 + tick_width + 1);

    svg.append("g").attr("class", "y_label");
    svg.append("g").attr("class", "x_label");
    svg.append("g").attr("class", "main");

    y_label = svg.select(".y_label").selectAll("g")
        .data(y_data).enter()
        .append("text")
        .text(function(d) {return d; })
        .style({"text-anchor": "middle", "font-size": 12, "fill": "#777"})
        .attr("y", function(d, i) { return (i + 1) * (cell_stroke + cell_radius * 2) + tick_width + cell_radius / 2; })
        .attr("x", tick_width * 0.8);

    x_label = svg.select(".x_label").selectAll("g")
        .data(x_data).enter()
        .append("text")
        .text(function(d) {return d; })
        .style({"text-anchor": "middle", "font-size": 12, "fill": "#777"})
        .attr("y", tick_width)
        .attr("x", function(d, i) { return (i + 1) * (cell_stroke + cell_radius * 2) + tick_width * 0.8 + cell_radius / 2; });

    plate = svg.select(".main").selectAll("g")
        .data(data).enter()
        .append("circle")
        .attr("cy", function(d) { return get_coord_y(d.coord) + tick_width; })
        .attr("cx", function(d) { return get_coord_x(d.coord) + tick_width; })
        .attr("r", cell_radius)
        .style("fill", function(d) { return get_fill_color(d); })
        .style("stroke", function(d) { return get_stroke_color(d); })
        .style("stroke-width", cell_stroke)
        .on("mouseover", function(d) {
            if (flag) {
                d3.select(this).transition().duration(200)
                    .style({"fill": "#ffd2ea", "stroke": "#ff69bc"});

                if (d.label) {
                    var pageX = d3.event.pageX, pageY = d3.event.pageY;
                    tooltip_timer = setTimeout(function() {
                        var lib = 'Lib <span class="label label-warning">' + d.label.substring(3, 4) + '</span> - ';
                        if (d.label.indexOf("WT") == -1) {
                            var temp = d.label.substring(5).split(';'), label = [];
                            for (var i = 0; i < temp.length; i++) {
                                label.push('<span class="label label-dark-blue">' + temp[i].substring(0, 1) + '</span><span class="label label-teal">' + temp[i].substring(1, temp[i].length - 1) + '</span><span class="label label-dark-red">' + temp[i].substring(temp[i].length - 1) + '</span>');
                            }
                            var label_more = '';
                            if (label.length > 1) {
                                for (var i = 1; i < label.length; i++) {
                                    label_more += '<tr><td></td><td></td><td><p>' + label[i] + '</p></td></tr>';
                                }
                            }
                        } else {
                            var label = ['<span class="label label-success">WT</span>'];
                        }

                        tooltip.transition().duration(200)
                            .style("opacity", 0.9);
                        tooltip.html('<table style="margin-top:5px;"><tbody><tr><td style="padding-right:20px;"><p><span class="label label-default">Well Position</span></p></td><td colspan="2"><p><span class="label label-primary">' + d.pos + '</span></p></td></tr><tr><td style="padding-right:20px;"><p><span class="label label-default">Name</span></p></td><td><p>' + lib + '</p></td><td><p>' + label[0] + '</p></td></tr>' + label_more + '<tr><td style="padding-right:20px;"><p><span class="label label-default">Sequence</span></p></td><td colspan="2" style="word-break:break-all"><code style="padding:0px; border-radius:0px;">' + d.sequence + '</code></td></tr></tbody></table>')
                            .style({"left": (pageX - 180) + "px", "top": (pageY + 20) + "px"});
                    }, 200);
                }
            }
        })
        .on("mouseout", function(d) {
            if (flag) {
                d3.select(this).transition().duration(200)
                    .style("fill", function(d) { return get_fill_color(d); })
                    .style("stroke", function(d) { return get_stroke_color(d); });

                if (d.label) {
                    tooltip.transition().duration(200)
                        .style("opacity", 0);
                    clearTimeout(tooltip_timer);
                }
            }
        });    
}

function draw_96_plate(job_id, type) {
    if (type !== 3) { type = 2; }
    $.ajax({
        url: '/site_data/' + type.toString() + 'd/result_' + job_id + '.json',
        cache: false,
        dataType: "json",
        success: function(data) {
            var unit = parseInt($("[id^='svg_plt_']").first().width() / 30);
            cell_radius = unit;
            cell_stroke = unit / 5;
            tick_width = unit * 3;

            for (var plt_key in data.plates) {
                for (var prm_key in data.plates[plt_key].primers) {
                    draw_single_plate(d3.select("#svg_plt_" + plt_key + "_prm_" + prm_key), data.plates[plt_key].primers[prm_key], true);
                }
            }
        }
    });
}
