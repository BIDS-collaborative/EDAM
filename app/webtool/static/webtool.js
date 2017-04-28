/* Shows given <div> and hides all other divs */
function showPageElement(what) {
  hideAllElements();

  // shows element
  var obj = typeof what == 'object'
    ? what : document.getElementById(what);

  obj.style.display = 'block';
  return false;
}

/* hides all elements */
function hideAllElements() {
  var elements = new Array("rf", "lr");
  for (var i = elements.length - 1; i >= 0; i--) {
    hidePageElement(document.getElementById(elements[i]));
  }
}

/* hides a given div */
function hidePageElement(what)
{
  var obj = typeof what == 'object'
    ? what : document.getElementById(what);

  obj.style.display = 'none';
  return false;
}

// pulls form data from page and returns as string
function submit() {
  var elements = new Array("rf", "lr");
  var selected = false;
  var requestString = "?";
  for (var i = elements.length - 1; i >= 0; i--) {
    var obj =  document.getElementById(elements[i]);
    if (obj.style.display == 'block') {
      selected = true;
      requestString = requestString.concat("model=").concat(elements[i]);
      var hp = document.getElementById( elements[i].concat("In1") );
      requestString = requestString.concat("&hyperparameters=").concat(hp.value).concat(",");
      requestString = requestString.concat(document.getElementById( elements[i].concat("In2") ).value);
    }
  }
  if (selected == false) {
    alert("Please make a model and hyperparameter selection");
  }
  requestString = requestString.concat("&features=").concat($("#document_filename").text());
  requestString = requestString.concat("&labels=").concat($("#label_filename").text());
  return requestString;
}

function extractFileName(filename) {
  var fullPath = document.getElementById(filename).value;
  if (fullPath) {
    var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
    var filename = fullPath.substring(startIndex);
    if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
      filename = filename.substring(1);
    }
    return filename;
  }
  return "";
}

// gathers form data and passes it to model selection API
function restSubmit() {
  $('#overlay').show()
  
  $.ajax({url: '/webtool/model_selection/'.concat(submit()),
    dataType: 'json',
    success: function(data) {
      // alert(data);
      var x = 600, y = 500;
      createVerticalBarGraph(data['feature_importance'], x, y);
      var x = 400, y = 400;
      createMatrix(data['confusion_matrix'], x, y);
      var x = 600, y = 500;
      createScatterPlot(data['pca'], x, y);
      var x = 600, y = 400, z = 400;
      create3DScatterPlot(data['pca_3d'], x, y, z);
      showPageElement('model-results')
      $('#overlay').hide();
    }
  });
}
