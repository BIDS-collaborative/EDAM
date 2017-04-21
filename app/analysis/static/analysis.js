$(document).ready(function(){
  /* VERTICAL BAR GRAPH */
  $.ajax({url: '/analysis/feature_importance',
    dataType: 'json',
    success: function(data) {
      var x = 600, y = 400;
      createVerticalBarGraph(data, x, y);
    }
  });

  /* CONFUSION MATRIX */
  $.ajax({url: '/analysis/confusion_matrix',
    dataType: 'json',
    success: function(data) {
      var x = 300, y = 300;
      createMatrix(data, x, y);
    }
  });


  $.ajax({url: '/analysis/pca_scatter',
    dataType: 'json',
    success: function(data) {
      var x = 600, y = 400;
      createScatterPlot(data, x, y);
    }
  });

  $.ajax({url: '/analysis/pca_3d',
    dataType: 'json',
    success: function(data) {
      var x = 600, y = 400, z = 400;
      create3DScatterPlot(data, x, y, z);
    }
  });

});

