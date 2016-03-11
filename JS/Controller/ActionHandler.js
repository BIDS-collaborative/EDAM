// Input Handler
var keyWord = "Default"
var searchResult;

$(document).ready(function(){
    $("#button").click(function($scope){
        keyWord = $('input[name=KeyWord]').val();
        results = searchDatabase(keyWord);
        
    });
    $("form").keypress(function(e) {
        keyWord = $('input[name=KeyWord]').val();
        results = searchDatabase(keyWord);

    });
    $("#button").mouseenter(function(){
        $("#button").fadeTo('fast',1);
    });
    $("#button").mouseleave(function(){
        $("#button").fadeTo('fast',0.2);
    });
    
});
