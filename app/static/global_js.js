function createVerticalBarGraph(data, x, y) {
  var dimensions = margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = x - margin.left - margin.right,
    height = y - margin.top - margin.bottom;
  var svg = d3.select('#feature_importance')
    .attr('width', x)
    .attr('height', y);

  var barWidth = width/data.length;
  var y = d3.scaleLinear().domain([0, d3.max(data)]).range([height, 0]);
  var x = d3.scaleBand().domain(d3.range(0, data.length)).rangeRound([0, width]).padding(0.02);

  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-8, 0])
    .html(function(d) { return 'Attribute Value: ' + d; });

  var g = svg.append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
  g.append('g')
    .attr('class', 'axis axis--x')
    .attr('transform', 'translate(0,' + height + ')')
    .call(d3.axisBottom(x));
  g.append('g')
    .attr('class', 'axis axis--y')
    .call(d3.axisLeft(y))

  var bar = g.selectAll('.bar')
    .data(data)
    .enter().append('g');
  bar.call(tip);

  bar.append('rect')
    .attr('class', 'd3rect')
    .attr('y', function(d) { return y(d); })
    .attr('x', function(d, i) { return i * barWidth; })
    .attr('width', x.bandwidth())
    .attr('height', function(d) { return height - y(d); })
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);
}

function createMatrix(data, x, y) {
  var labels = ['Invasive', 'Noninvasive'];
  Matrix({
    margins   : {top: 10, right: 10, bottom: 50, left: 100},
    container : '#confusion_matrix',
    data      : data,
    labels    : labels,
    width     : x,
    height    : y
  });
}
