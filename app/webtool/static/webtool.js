/* Shows given <div> and hides all other divs */ 
function showPageElement(what)  
{  
  hideAllElements();

  // shows element
  var obj = typeof what == 'object'  
    ? what : document.getElementById(what);

  obj.style.display = 'block';  
  return false;  
} 

/* hides a given div */
function hidePageElement(what)  
{  
  var obj = typeof what == 'object'  
    ? what : document.getElementById(what);  

  obj.style.display = 'none';  
  return false;  
}  

function hideAllElements() 
{
  var elements = new Array("random-forest", "logistic-regression", "clustering");
  for (var i = elements.length - 1; i >= 0; i--) {
      hidePageElement(document.getElementById(elements[i]));
    }
}

$( document ).ready(function() {
    /* make sure the javascript file doesn't do anything until the html is loaded */
});