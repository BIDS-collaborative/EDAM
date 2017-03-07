$(document).ready(function(){
  var newData = {
    0.052292586431240476: 1,
    0.10713425866748247: 2,
    0.0693563829365081: 3,
    0.11078379234010838: 4,
    0.046718949326233265: 5,
    0.09660865890135116: 6,
    0.05291856239019112: 7,
    0.0032448594628799116: 8,
    0.05164358141039909: 9,
    0.01277467297704207: 10,
    0.04202756055149503: 11,
    0.06184134645873551: 12,
    0.05229293009728004: 13,
    0.018739288478561815: 14,
    0.022280519611825707: 15,
    0.04181676150348127: 16,
    0.08479743624028183: 17,
    0.07272785221490291: 18
}

  /* VERTICAL BAR GRAPH */
  $.ajax({url: '/analysis/feature_importance',
    dataType: 'json',
    success: function(data) {
      var x = 800, y = 500;
      createVerticalBarGraph(newData, x, y);
    }
  });
var newData2 = [[
    [
        0.86,
        0.14
    ],
    [
        0.67,
        0.33
    ]
], [1, 2, 3, 4]];
  /* CONFUSION MATRIX */
  $.ajax({url: '/analysis/confusion_matrix',
    dataType: 'json',
    success: function(data) {
      var x = 400, y = 400;
      createMatrix(newData2, x, y);
    }
  });
});

