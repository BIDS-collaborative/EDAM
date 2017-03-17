function createVerticalBarGraph(data, x, y) {
  var dimensions = margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = x - margin.left - margin.right,
    height = y - margin.top - margin.bottom;
  var features = data['features'],
  importance = data['importance'];
  var svg = d3.select('#feature_importance')
    .attr('width', x)
    .attr('height', y);
  var pairs = [];

  for (i = 0; i < features.length; i++){
    pairs.push([Math.round(importance[i]*1000)/1000, features[i]]);
  }
  var barWidth = width/importance.length;
  var y = d3.scaleLinear().domain([0, d3.max(importance)]).range([height, 0]);
  var x = d3.scaleBand().domain(d3.range(0, importance.length)).rangeRound([0, width]);

  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-8, 0])
    .html(function(d) { return "Importance: " + d[0] + "<br/>" + "Feature: " + d[1]; });

  var g = svg.append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
  g.append('g')
    .attr('class', 'axis axis--x')
    .attr('transform', 'translate(0,' + height + ')')
    .call(d3.axisBottom(x));
  var yAxis = d3.axisLeft(y);
  yAxis.ticks(10);
  yAxis.tickSizeOuter(0);
  yAxis.tickPadding(3);
  g.append('g')
    .attr('class', 'axis axis--y')
    .call(yAxis);

  var bar = g.selectAll('.bar')
    .data(pairs)
    .enter().append('g');
  bar.call(tip);

  bar.append('rect')
    .attr('class', 'd3rect')
    .attr('y', function(d) { return y(d[0]); })
    .attr('x', function(d, i) { return i * barWidth + 1; })
    .attr('width', x.bandwidth()-1)
    .attr('height', function(d) { return height - y(d[0]);})
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);

}

function createMatrix(data, x, y) {
  // data is a dictionary of the form {data: [], tips: [], labels: []}
  // where data is shown in the cells, tips are hover tooltips and labels are x/y axis labels
  Matrix({
    margins   : {top: 10, right: 10, bottom: 50, left: 100},
    container : '#confusion_matrix',
    data      : data['matrix'],
    tips      : data['tips'],
    labels    : data['labels'],
    width     : x,
    height    : y
  });
}

function createScatterPlot(data, x, y) {
  var feature1 = data['feature1'],
  feature2 = data['feature2'],
  invasive = data['invasive'],
  species = data['species'];
  invasive = data['label'];
  var pairs = [];

  for (i = 0; i < feature1.length; i++){
    pairs.push([feature1[i], feature2[i], species[i], invasive[i]]);
  }

  var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = x - margin.left - margin.right,
    height = y - margin.top - margin.bottom;

  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-8, 0])
    .html(function(d) { return d[2]});

  // set the ranges
  var x = d3.scaleLinear().domain([(d3.min(feature1) - 0.25), (d3.max(feature1) + 0.25)]).range([0, width]);
  var y = d3.scaleLinear().domain([(d3.min(feature2) - 0.25), (d3.max(feature2) + 0.25)]).range([height, 0]);

  // append the svg obgect to the body of the page
  // appends a 'group' element to 'svg'
  // moves the 'group' element to the top left margin
  var svg = d3.select("#scatter_plot")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)

  var g = svg.append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');


  g.append('g')
    .attr('class', 'axis axis--x')
    .attr('transform', 'translate(0,' + height + ')')
    .call(d3.axisBottom(x));
  var yAxis = d3.axisLeft(y);
  yAxis.ticks(10);
  yAxis.tickSizeOuter(0);
  yAxis.tickPadding(3);
  g.append('g')
    .attr('class', 'axis axis--y')
    .call(yAxis);

  // Add the scatterplot
  svg.selectAll("dot")
    .data(pairs)
    .enter().append("circle")
    .attr('class', 'circ')
    .call(tip)
    .attr("r", 4)
    .attr("cx", function(d) { return x(d[0]) + margin.left;})
    .attr("cy", function(d) { return y(d[1]) + margin.top;})
    .style("fill", function(d) {if (d[3] == 0) {return "blue"}; return "red";})
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);
}
