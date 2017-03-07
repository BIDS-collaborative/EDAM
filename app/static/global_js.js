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
