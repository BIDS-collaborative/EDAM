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
  var elements = new Array("rf", "lr", "clustering");
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

function submit() {
  var elements = new Array("rf", "lr", "clustering");
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
      alert(requestString);
    }
  }
  if (selected == false) {
    alert("Please make a model and hyperparameter selection");
  }
  return false;
}

$( document ).ready(function() {
  /* make sure the javascript file doesn't do anything until the html is loaded */
  alert("hi");
});