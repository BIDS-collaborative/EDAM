// sample bar chart in d3.js
$(document).ready(function(){

  // sample data
  var data = [4, 8, 15, 16, 23, 42];

  var width = 420,
    barHeight = 20;

  // calculate scale
  var x = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([0, width]);

    var tip = d3.tip()
      .attr("class", "d3-tip")
      .offset([-8, 0])
      .html(function(d) { return "Attribute Value: " + d; });

  // find chart and give it dimensions
  var chart = d3.select("#chart")
    .attr("width", width)
    .attr("height", barHeight * data.length);

  // add g for each data point
  var bar = chart.selectAll("g")
    .data(data)
  .enter().append("g")
    .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });
  bar.call(tip);


  // bar g is comprised of a rectangular bar and text label
  bar.append("rect")
    .attr("class", "d3rect")
    .attr("width", x)
    .attr("height", barHeight - 1)
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);

  bar.append("text")
    .attr("class", "graphtext")
    .attr("x", function(d) { return x(d) - 3; })
    .attr("y", barHeight / 2)
    .attr("dy", ".35em")
    .text(function(d) { return d; });



});

