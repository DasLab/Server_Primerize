var tooltip_timer;
app.mod96Plate.cell_radius = 7;
app.mod96Plate.cell_stroke = 1.4;
app.mod96Plate.tick_width = 20;
app.mod96Plate.x_data = d3.range(1, 13);
app.mod96Plate.y_data = 'ABCDEFGH'.split('');
app.mod96Plate.tooltip = d3.select("body").append("div")
    .attr("class", "svg_tooltip")
    .style("opacity", 0);


app.mod96Plate.fnGetCoordY = function(num) {
    var y = (num - 1) % 8 + 1;
    return y * (app.mod96Plate.cell_stroke + app.mod96Plate.cell_radius * 2);
};

app.mod96Plate.fnGetCoordX = function(num) {
    var x = Math.floor((num - 1) / 8) + 1;
    return x * (app.mod96Plate.cell_stroke + app.mod96Plate.cell_radius * 2);
};


app.mod96Plate.fnGetStrokeColor = function(d) {
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
};

app.mod96Plate.fnGetFillColor = function(d) {
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
};


app.mod96Plate.fnDrawSinglePlate = function(element, data, flag) {
    var svg = element.append("svg")
        .attr("width", (app.mod96Plate.cell_stroke + app.mod96Plate.cell_radius * 2) * 12.5 + app.mod96Plate.tick_width + 1)
        .attr("height", (app.mod96Plate.cell_stroke + app.mod96Plate.cell_radius * 2) * 8.5 + app.mod96Plate.tick_width + 1);

    svg.append("g").attr("class", "y_label");
    svg.append("g").attr("class", "x_label");
    svg.append("g").attr("class", "main");

    y_label = svg.select(".y_label").selectAll("g")
        .data(app.mod96Plate.y_data).enter()
        .append("text")
        .text(function(d) {return d; })
        .style({"text-anchor": "middle", "font-size": 12, "fill": "#777"})
        .attr("y", function(d, i) { return (i + 1) * (app.mod96Plate.cell_stroke + app.mod96Plate.cell_radius * 2) + app.mod96Plate.tick_width + app.mod96Plate.cell_radius / 2; })
        .attr("x", app.mod96Plate.tick_width * 0.8);

    x_label = svg.select(".x_label").selectAll("g")
        .data(app.mod96Plate.x_data).enter()
        .append("text")
        .text(function(d) {return d; })
        .style({"text-anchor": "middle", "font-size": 12, "fill": "#777"})
        .attr("y", app.mod96Plate.tick_width)
        .attr("x", function(d, i) { return (i + 1) * (app.mod96Plate.cell_stroke + app.mod96Plate.cell_radius * 2) + app.mod96Plate.tick_width * 0.8 + app.mod96Plate.cell_radius / 2; });

    plate = svg.select(".main").selectAll("g")
        .data(data).enter()
        .append("circle")
        .attr("cy", function(d) { return app.mod96Plate.fnGetCoordY(d.coord) + app.mod96Plate.tick_width; })
        .attr("cx", function(d) { return app.mod96Plate.fnGetCoordX(d.coord) + app.mod96Plate.tick_width; })
        .attr("r", app.mod96Plate.cell_radius)
        .attr("class", function(d) {
            if (d.label && d.label.indexOf("WT") == -1) {
                var temp = d.label.substring(5).split(';'), label = '';
                for (var i = 0; i < temp.length; i++) {
                    label += 'seqpos_' + temp[i].substring(1, temp[i].length - 1) + ' ';
                }
                return label;
            }
            return '';
        })
        .style("fill", function(d) { return app.mod96Plate.fnGetFillColor(d); })
        .style("stroke", function(d) { return app.mod96Plate.fnGetStrokeColor(d); })
        .style("stroke-width", app.mod96Plate.cell_stroke)
        .on("mouseover", function(d) {
            if (flag) {
                var cls = d3.select(this).attr("class").trim().split(' ')
                            .map(function(val) { return 'span.' + val; })
                            .reduce(function(prev_val, curr_val) { return prev_val + ', ' + curr_val; });
                d3.select(this).classed('active', true);

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

                        app.mod96Plate.tooltip.transition().duration(200)
                            .style("opacity", 0.9);
                        app.mod96Plate.tooltip.html('<table style="margin-top:5px;"><tbody><tr><td style="padding-right:20px;"><p><span class="label label-default">Well Position</span></p></td><td colspan="2"><p><span class="label label-primary">' + d.pos + '</span></p></td></tr><tr><td style="padding-right:20px;"><p><span class="label label-default">Name</span></p></td><td><p>' + lib + '</p></td><td><p>' + label[0] + '</p></td></tr>' + label_more + '<tr><td style="padding-right:20px;"><p><span class="label label-default">Sequence</span></p></td><td colspan="2" style="word-break:break-all"><code style="padding:0px; border-radius:0px;">' + d.sequence + '</code></td></tr></tbody></table>')
                            .style({"left": (pageX - 180) + "px", "top": (pageY + 20) + "px"});
                    }, 200);

                    clearTimeout(hover_timeout);
                    hover_timeout = setTimeout(function() { $(cls).addClass("active"); }, 50);
                }
            }
        })
        .on("mouseout", function(d) {
            if (flag) {
                d3.select(this).classed('active', false);

                if (d.label) {
                    app.mod96Plate.tooltip.transition().duration(200)
                        .style("opacity", 0);
                    clearTimeout(tooltip_timer);
                    clearTimeout(hover_timeout);
                    $("span[class^='seqpos_'].active").removeClass("active");
                }
            }
        });
};

app.mod96Plate.fnDrawResultPlates = function() {
    $.ajax({
        url: '/site_data/' + app.modPrimerize.job_type + 'd/result_' + app.modPrimerize.job_id + '.json',
        cache: false,
        dataType: "json",
        success: function(data) {
            var unit = parseInt($("[id^='svg_plt_']").first().width() / 30);
            app.mod96Plate.cell_radius = unit;
            app.mod96Plate.cell_stroke = unit / 5;
            app.mod96Plate.tick_width = unit * 3;

            for (var plt_key in data.plates) {
                for (var prm_key in data.plates[plt_key].primers) {
                    app.mod96Plate.fnDrawSinglePlate(d3.select("#svg_plt_" + plt_key + "_prm_" + prm_key), data.plates[plt_key].primers[prm_key], true);
                }
            }
        }
    });
}
