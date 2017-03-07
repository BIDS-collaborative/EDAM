$(document).ready(function(){
  /* VERTICAL BAR GRAPH */
  $.ajax({url: '/analysis/feature_importance',
    dataType: 'json',
    success: function(data) {
      var x = 800, y = 500;
      createVerticalBarGraph(data, x, y);
    }
  });

  /* CONFUSION MATRIX */
  $.ajax({url: '/analysis/confusion_matrix',
    dataType: 'json',
    success: function(data) {
      var x = 400, y = 400;
      createMatrix(data, x, y);
    }
  });


  // $.ajax({url: '/analysis/scatter_plot',
  //   dataType: 'json',
  //   success: function(data) {
  //     var x = 800, y = 500;
  //     createScatterPlot(data, x, y);
  //   }
  // });

var testData = {"feature1": [1, 2, 5, 7, 9], "feature2": [2, 4, 7, 8, 11], "species": ["cactus", "rose", "tulip", "weed", "daisy"]};
createScatterPlot(testData, 800, 500);

});

