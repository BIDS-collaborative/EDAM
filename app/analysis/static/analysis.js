// sample bar chart in d3.js
$(document).ready(function(){
// /* Horizontal Bar Graph */

//   // sample data
//   var data = [4, 8, 15, 16, 23, 42];

//   var width = 420,
//     barHeight = 20;

//   // calculate scale
//   var x = d3.scaleLinear()
//     .domain([0, d3.max(data)])
//     .range([0, width]);

//     var tip = d3.tip()
//       .attr("class", "d3-tip")
//       .offset([-8, 0])
//       .html(function(d) { return "Attribute Value: " + d; });

//   // find chart and give it dimensions
//   var chart = d3.select("#chart")
//     .attr("width", width)
//     .attr("height", barHeight * data.length);

//   // add g for each data point
//   var bar = chart.selectAll("g")
//     .data(data)
//   .enter().append("g")
//     .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });
//   bar.call(tip);


//   // bar g is comprised of a rectangular bar and text label
//   bar.append("rect")
//     .attr("class", "d3rect")
//     .attr("width", x)
//     .attr("height", barHeight - 1)
//     .on('mouseover', tip.show)
//     .on('mouseout', tip.hide);

//   bar.append("text")
//     .attr("class", "graphtext")
//     .attr("x", function(d) { return x(d) - 3; })
//     .attr("y", barHeight / 2)
//     .attr("dy", ".35em")
//     .text(function(d) { return d; });

/* VERTICAL BAR GRAPH*/
$.ajax({url: "links to web results",
       dataType: "json",
       success: function(data) {
        var storeData = null;
        $.each(data, function(key, val) {
          if (key == "featureResults"){
            storeData = val;
          }
        });
      }
  });
// placeholder data
  var data = [4, 8, 15, 16, 23, 42, 46, 21, 12];
  // var height = 500,

  //   width = 960;

  var svg = d3.select("svg"),
    margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;
  // calculate scale
  // var y = d3.scaleLinear()
  //   .domain([0, d3.max(data)])
  //   .range([height, 0]);
  var barWidth = width/data.length;
  var y = d3.scaleLinear().domain([0, d3.max(data)]).range([height, 0]);
  var x = d3.scaleBand().domain(d3.range(0, data.length)).rangeRound([0, width]).padding(0.02);

  var tip = d3.tip()
    .attr("class", "d3-tip")
    .offset([-8, 0])
    .html(function(d) { return "Attribute Value: " + d; });
  // find chart and give it dimensions

  var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  g.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));
  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y))

  // var chart = d3.select("#verticalgraph")
  //   .attr("height", height)
  //   .attr("width", barWidth * data.length);

  // add g for each data point

  var bar = g.selectAll(".bar")
    .data(data)
    .enter().append("g");
  bar.call(tip);

  bar.append("rect")
    .attr("class", "d3rect")
    .attr("class", "d3rect")
    .attr("y", function(d) { return y(d); })
    .attr("x", function(d, i) { return i * barWidth; })
    .attr("width", x.bandwidth())
    .attr("height", function(d) { return height - y(d); })
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);
  // var bar = chart.selectAll("g")
  //   .data(data)
  //   .enter().append("g")
  //   .attr("transform", function(d, i) { return "translate(" + i * barWidth + ",0)"; });
  //   bar.call(tip);
  //test


  // // bar g is comprised of a rectangular bar and text label
  // bar.append("rect")
  //   .attr("class", "d3rect")
  //   .attr("y", function(d) { return y(d); })
  //   .attr("height", function(d) { return height - y(d); })
  //   .attr("width", barWidth - 1)
  //   .on('mouseover', tip.show)
  //   .on('mouseout', tip.hide);


/*CONFUSION MATRIX */
$.ajax({url: "links to web results",
       dataType: "json",
       success: function(data) {
        var storeData = null;
        $.each(data, function(key, val) {
          if (key == "matrices"){
            storeData = val;
          }
        });
       }
  });
  var confusionMatrix = [
    [0.69, 0.02],
    [0.03, 0.70]
  ];
  var labels = ['Invasive', 'Noninvasive'];

  Matrix({
    container : '#container',
    data      : confusionMatrix,
    labels    : labels
  });
});

