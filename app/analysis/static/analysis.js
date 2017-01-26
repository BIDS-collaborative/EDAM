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

  // find chart and give it dimensions
  var chart = d3.select(".chart")
    .attr("width", width)
    .attr("height", barHeight * data.length);

  // add g for each data point
  var bar = chart.selectAll("g")
    .data(data)
  .enter().append("g")
    .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

  // bar g is comprised of a rectangular bar and text label
  bar.append("rect")
    .attr("width", x)
    .attr("height", barHeight - 1);

  bar.append("text")
    .attr("x", function(d) { return x(d) - 3; })
    .attr("y", barHeight / 2)
    .attr("dy", ".35em")
    .text(function(d) { return d; });
});