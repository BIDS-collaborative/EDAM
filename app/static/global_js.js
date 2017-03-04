$(document).ready(function(){
  // Add smooth scrolling to all links in navbar + footer link
  $(".navbar a, footer a[href='#myPage']").on('click', function(event) {

   // Make sure this.hash has a value before overriding default behavior
  if (this.hash !== "") {

    // Prevent default anchor click behavior
    event.preventDefault();

    // Store hash
    var hash = this.hash;

    // Using jQuery's animate() method to add smooth page scroll
    // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
    $('html, body').animate({
      scrollTop: $(hash).offset().top
    }, 900, function(){

      // Add hash (#) to URL when done scrolling (default click behavior)
      window.location.hash = hash;
      });
    } // End if
  });
});
function createVerticalBarGraph(data, x, y){
  var dimensions = margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = x - margin.left - margin.right,
    height = y - margin.top - margin.bottom;
  var svg = d3.select("svg")
    .attr("width", x)
    .attr("height", y);


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
  }

  function createMatrix(data, x, y){
    var labels = ['Invasive', 'Noninvasive'];
    Matrix({
      container : '#container',
      data      : data,
      labels    : labels,
      width     : x,
      height    : y
    });
  }
