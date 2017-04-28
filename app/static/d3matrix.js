function Matrix(options) {

  var margin = options.margins,
      width = options.width,
      height = options.height,
      data = options.data,
      samples = options.tips,
      container = options.container,
      labelsData = options.labels,
      numrows,
      numcols;

  if(!data){
      throw new Error('No data passed.');
  }

  if(!Array.isArray(data) || !data.length || !Array.isArray(data[0])){
      throw new Error('Data type should be two-dimensional Array.');
  }
  var total = []
  total.push(data[0][0])
  total.push(data[0][1])
  total.push(data[1][0])
  total.push(data[1][1])
  var indexDict = {};
  for (i = 0 ; i < 4; i++) {
    indexDict[total[i]] = samples[i];
  }

  numrows = data.length;
  numcols = data[0].length;

  var svg = d3.select(container).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var tip = d3.tip()
      .attr("class", "d3-tip")
      .offset([-8, 0])
      .html(function(d) { return "Number of Samples: " + indexDict[d]; });

  var background = svg.append("rect")
      .style("stroke", "black")
      .style("stroke-width", "2px")
      .attr("width", width)
      .attr("height", height)
      .call(tip);


  var x = d3.scaleBand()
      .domain(d3.range(numcols))
      .range([0, width]);

  var y = d3.scaleBand()
      .domain(d3.range(numrows))
      .range([0, height]);

  var colorMap = d3.scaleLinear()
      .domain([0, 1])
      .range(["white", "black"]);

  var row = svg.selectAll(".row")
      .data(data)
      .enter().append("g")
      .attr("class", "row")
      .attr("transform", function(d, i) { return "translate(0," + y(i) + ")"; });


  var cell = row.selectAll(".cell")
      .data(function(d) { return d; })
          .enter().append("g")
      .attr("class", "cell")
      .attr("transform", function(d, i) { return "translate(" + x(i) + ", 0)"; });


  cell.append('rect')
      .attr("width", x.bandwidth())
      .attr("height", y.bandwidth())
      .style("stroke-width", 0)
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide);

  cell.append("text")
      .attr("dy", ".32em")
      .attr("x", x.bandwidth() / 2)
      .attr("y", y.bandwidth() / 2)
      .attr("text-anchor", "middle")
      .style("fill", function(d, i) { return d >= 0.5 ? 'white' : 'black'; })
      .text(function(d, i) { return d; });

  row.selectAll(".cell")
      .data(function(d, i) { return data[i]; })
      .style("fill", colorMap);

  var labels = svg.append('g')
      .attr('class', "labels");

  var columnLabels = labels.selectAll(".column-label")
      .data(labelsData)
    .enter().append("g")
      .attr("class", "column-label")
      .attr("transform", function(d, i) { return "translate(" + x(i) + "," + height + ")"; });

  columnLabels.append("line")
      .style("stroke", "black")
      .style("stroke-width", "1px")
      .attr("x1", x.bandwidth() / 2)
      .attr("x2", x.bandwidth() / 2)
      .attr("y1", 0)
      .attr("y2", 5);

  columnLabels.append("text")
      .attr("x", x.bandwidth() / 2)
      .attr("y", y.bandwidth() / 8)
      .attr("dy", ".32em")
      .attr("text-anchor", "middle")
      //.attr("transform", "rotate(-60)") MAKES TEXTLABELS WEIRD
      .text(function(d, i) { return d; });

  var rowLabels = labels.selectAll(".row-label")
      .data(labelsData)
    .enter().append("g")
      .attr("class", "row-label")
      .attr("transform", function(d, i) { return "translate(" + 0 + "," + y(i) + ")"; });

  rowLabels.append("line")
      .style("stroke", "black")
      .style("stroke-width", "1px")
      .attr("x1", 0)
      .attr("x2", -5)
      .attr("y1", y.bandwidth() / 2)
      .attr("y2", y.bandwidth() / 2);

  rowLabels.append("text")
      .attr("x", -10)
      .attr("y", y.bandwidth() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "end")
      .text(function(d, i) { return d; });
  svg.append("text")
    .attr("x", 200)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .style("font-size", "22px")
    .style("text-decoration", "underline")
    .text("Model Prediction Confusion Matrix");
  svg.append("text")

    .attr("x", -100)
    .attr("y", 180)
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .style("font-size", "16px")
    .text("Actual");
  svg.append("text")
    .attr("x", 200)
    .attr("y", 450)
    .style("text-anchor", "middle")
    .style("font-size", "16px")
    .text("Predicted");
  svg.append("text")
    .attr("x", 200)
    .attr("y", 470)
    .style("text-anchor", "middle")
    .style("font-size", "12px")
    .style("font-style", "italic")
    .text("The confusion matrix shows the prediction accuracy of the model");

}
