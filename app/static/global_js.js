function createVerticalBarGraph(data, x, y) {
  var dimensions = margin = {top: 50, right: 20, bottom: 80, left: 65},
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

  svg.append("text")
    .attr("x", ((width+margin.left + margin.right)/2))
    .attr("y", height/10)
    .attr("text-anchor", "middle")
    .style("font-size", "22px")
    .style("text-decoration", "underline")
    .text("Relative Importance of each Feature");
  svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0)
    .attr("x",0 - ((height+margin.top + margin.bottom) / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .style("font-size", "16px")
    .text("Feature Importance");
  svg.append("text")
    .attr("x", ((width+margin.left + margin.right)/2))
    .attr("y", height + margin.top + 38 )
    .style("text-anchor", "middle")
    .style("font-size", "16px")
    .text("Feature Index");
  svg.append("text")
    .attr("x", ((width+margin.left + margin.right)/2))
    .attr("y", height + margin.top + 56 )
    .style("text-anchor", "middle")
    .style("font-size", "12px")
    .style("font-style", "italic")
    .text("The bar graph illustrates the relative contribution of each feature to the model");

}

function createMatrix(data, x, y) {
  // data is a dictionary of the form {data: [], tips: [], labels: []}
  // where data is shown in the cells, tips are hover tooltips and labels are x/y axis labels
  Matrix({
    margins   : {top: 50, right: 20, bottom: 80, left: 130},
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

  var margin = {top: 50, right: 20, bottom: 80, left: 65},
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

  svg.append("text")
    .attr("x", ((width+margin.left + margin.right)/2))
    .attr("y", height/10)
    .attr("text-anchor", "middle")
    .style("font-size", "22px")
    .style("text-decoration", "underline")
    .text("Feature Scatter Plot");
  svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0)
    .attr("x",0 - ((height+margin.top + margin.bottom) / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .style("font-size", "16px")
    .text("PCA 2");
  svg.append("text")
    .attr("x", ((width+margin.left + margin.right)/2))
    .attr("y", height + margin.top + 38 )
    .style("text-anchor", "middle")
    .style("font-size", "16px")
    .text("PCA 1");
  svg.append("text")
    .attr("x", ((width+margin.left + margin.right)/2))
    .attr("y", height + margin.top + 56 )
    .style("text-anchor", "middle")
    .style("font-size", "12px")
    .style("font-style", "italic")
    .text("Plot of the first 2 principal components of the feature set");
}

function create3DScatterPlot(data, x, y, z){
  var feature1 = data['feature1'],
  feature2 = data['feature2'],
  feature3 = data['feature3'],
  invasive = data['label'],
  invasive_points = [],
  noninvasive_points = [];
  for (i = 0; i < feature1.length; i++){
    if (invasive[i] == 1){
      invasive_points.push([feature1[i], feature2[i], feature3[i]]);
    } else {
      noninvasive_points.push([feature1[i], feature2[i], feature3[i]]);
    }
  }

  // Set up the chart
  var chart = new Highcharts.Chart('3d_scatter_plot', {
    chart: {
        renderTo: 'scatterplot',
        width: x,
        height: y,
        margin: 100,
        type: 'scatter',
        options3d: {
            enabled: true,
            alpha: 10,
            beta: 30,
            depth: z,
            viewDistance: 5,
            fitToPlot: false,
            frame: {
                bottom: { size: 1, color: 'rgba(0,0,0,0.02)' },
                back: { size: 1, color: 'rgba(0,0,0,0.04)' },
                side: { size: 1, color: 'rgba(0,0,0,0.06)' }
            }
        }
    },
    title: {
        text: 'Feature Scatter Plot 3D'
    },
    subtitle: {
        text: 'Click and drag the plot area to rotate in space'
    },
    plotOptions: {
        scatter: {
            width: 10,
            height: 10,
            depth: 10
        }
    },
    yAxis: {
        min: 1.5*Math.max(Math.min(...feature2)),
        max: 1.5*Math.max(Math.max(...feature2)),
        title: {
          text:"PCA 2"
        }
    },
    xAxis: {
        min: 1.5*Math.max(Math.min(...feature1)),
        max: 1.5*Math.max(Math.max(...feature1)),
        gridLineWidth: 1,
        title: {
          text:"PCA 1"
        }
    },
    zAxis: {
        min: 1.5*Math.max(Math.min(...feature3)),
        max: 1.5*Math.max(Math.max(...feature3)),
        showFirstLabel: false,
        title: {
          text:"PCA 3"
        }
    },
    legend: {
        enabled: false
    },
    series: [{
        name: 'Invasive',
        color: '#ED0D08',
        data: invasive_points
    }, {
        name: 'Noninvasive',
        color: '#4682b4',
        data: noninvasive_points,
        marker: {
            symbol: 'circle'
        }
    }]
  });


  // Add mouse events for rotation
  $(chart.container).on('mousedown.hc touchstart.hc', function (eStart) {
      eStart = chart.pointer.normalize(eStart);

      var posX = eStart.pageX,
          posY = eStart.pageY,
          alpha = chart.options.chart.options3d.alpha,
          beta = chart.options.chart.options3d.beta,
          newAlpha,
          newBeta,
          sensitivity = 5; // lower is more sensitive

      $(document).on({
          'mousemove.hc touchdrag.hc': function (e) {
              // Run beta
              newBeta = beta + (posX - e.pageX) / sensitivity;
              chart.options.chart.options3d.beta = newBeta;

              // Run alpha
              newAlpha = alpha + (e.pageY - posY) / sensitivity;
              chart.options.chart.options3d.alpha = newAlpha;

              chart.redraw(false);
          },
          'mouseup touchend': function () {
              $(document).off('.hc');
          }
      });
  });
}
