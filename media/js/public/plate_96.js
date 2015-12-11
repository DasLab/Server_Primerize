var cell_radius = 7, cell_stroke = 1.4, tick_width = 20;
var tooltip_timer;


function get_coord_y(num) {
    var y = (num - 1) % 8 + 1;
    return y * (cell_stroke + cell_radius * 2);
}

function get_coord_x(num) {
    var x = Math.floor((num - 1) / 8) + 1;
    return x * (cell_stroke + cell_radius * 2);
}

function get_stroke_color(label) {
    if (label) {
        if (label.indexOf("WT") != -1) {
            return "#29be92";
        } else {
            return "#c28fdd";
        }
    } else {
        return "#333";
    }
}

function get_fill_color(label) {
    if (label) {
        if (label.indexOf("WT") != -1) {
            return "#beebde";
        } else {
            return "#ecddf4";
        }
    } else {
        return "#fff";
    }
}

function draw_96_plate(job_id) {
  $.ajax({
      url: '/site_data/2d/result_' + job_id + '.json',
      cache: false,
      dataType: "json",
      success: function(data) {
        var x_data = d3.range(1, 13), y_data = 'ABCDEFGH'.split('');
        var tooltip = d3.select("body").append("div")
                        .attr("class", "tooltip")
                        .style("opacity", 0);

        for (var plt_key in data.plates) {
            for (var prm_key in data.plates[plt_key].primers) {
                var svg = d3.select("#svg_plt_" + plt_key + "_prm_" + prm_key)
                    .append("svg")
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
                    .data(data.plates[plt_key].primers[prm_key]).enter()
                    .append("circle")
                    .attr("cy", function(d) { return get_coord_y(d.coord) + tick_width; })
                    .attr("cx", function(d) { return get_coord_x(d.coord) + tick_width; })
                    .attr("r", cell_radius)
                    .style("fill", function(d) { return get_fill_color(d.label); })
                    .style("stroke", function(d) { return get_stroke_color(d.label); })
                    .style("stroke-width", cell_stroke)
                    .on("mouseover", function(d) {
                        d3.select(this).transition().duration(200)
                            .style({"fill": "#ffd2ea", "stroke": "#ff69bc"});

                        if (d.label) {
                            var pageX = d3.event.pageX, pageY = d3.event.pageY;
                            tooltip_timer = setTimeout(function() {
                                var label = d.label;
                                if (label.indexOf("WT") == -1) {
                                    label = 'Lib <span class="label label-warning">' + label.substring(3, 4) + '</span> - <span class="label label-dark-blue">' + label.substring(5, 6) + '</span><span class="label label-teal">' + label.substring(6, label.length - 1) + '</span><span class="label label-dark-red">' + label.substring(label.length - 1) + '</span>';
                                } else {
                                    label = 'Lib <span class="label label-warning">' + label.substring(3, 4) + '</span> - <span class="label label-success">WT</span>';
                                }

                                tooltip.transition().duration(200)
                                    .style("opacity", .9);
                                tooltip.html('<table style="margin-top:5px;"><tbody><tr><td style="padding-right:20px;"><p><span class="label label-default">Well Position</span></p></td><td><p><span class="label label-primary">' + d.pos + '</span></p></td></tr><tr><td style="padding-right:20px;"><p><span class="label label-default">Name</span></p></td><td><p>' + label + '</p></td></tr><tr><td style="padding-right:20px;"><p><span class="label label-default">Sequence</span></p></td><td style="word-break:break-all"><code style="padding:0px; border-radius:0px;">' + d.sequence + '</code></td></tr></tbody></table>')
                                    .style({"left": pageX + "px", "top": (pageY - 28) + "px"});
                            }, 200);                                    
                        }
                    })
                    .on("mouseout", function(d) {
                        d3.select(this).transition().duration(200)
                            .style("fill", function(d) { return get_fill_color(d.label); })
                            .style("stroke", function(d) { return get_stroke_color(d.label); });

                        if (d.label) {
                            tooltip.transition().duration(200)
                                .style("opacity", 0);
                            clearTimeout(tooltip_timer);
                        }
                    });

            }
        }
      }
  });

}
