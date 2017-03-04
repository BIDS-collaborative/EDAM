// sample bar chart in d3.js
$(document).ready(function(){
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
  var x = 960,
    y = 500;
createVerticalBarGraph(data, x, y);

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

  var x = 400,
    y = 400;
  var data = [
    [0.69, 0.02],
    [0.03, 0.70]
  ];

createMatrix(data, x, y);

});

