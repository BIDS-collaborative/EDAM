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
});

