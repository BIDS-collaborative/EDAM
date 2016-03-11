// Input Handler

var searchResult;

$(document).ready(function(){
    $("#button").click(function(){
        var keyWord = $('input[name=KeyWord]').val();
        results = searchDatabase(keyWord);
        console.log(results)
        $("#searchResponse").append("<table class='table table-striped'><thead><tr><th>" + keyWord + "</th> </tr>");
        $("#searchResponse").append("<tr><th> Source Database </th><th> Name </th> <th> Taxonomy </th></tr> </thead>");
        $("#searchResponse").append("<tbody>");
        for (database in results) {
            result = results[database];
            $("#searchResponse").append("<tr><td>" + database + "</td> <td>" + result[0] + "</td> <td>" + result[1] + "</td> </tr>");
        }
        $("#searchResponse").append("</tbody> </table>");        
    });
    
    $("form").keypress(function(e) {
        if(e.which == 13) {
            var keyWord = $('input[name=KeyWord]').val();
            results = searchDatabase(keyWord);
            $("#searchResponse").append("<table class='table table-striped'><thead><tr><th>" + keyWord + "</th> </tr>");
            $("#searchResponse").append("<tr><th> Source Database </th><th> Name </th> <th> Taxonomy </th></tr> </thead>");
            $("#searchResponse").append("<tbody>");
            for (database in results) {
                result = results[database];
                $("#searchResponse").append("<tr><td>" + database + "</td> <td>" + result[0] + "</td> <td>" + result[1] + "</td> </tr>");
            }
            $("#searchResponse").append("</tbody> </table>");
        }
    });

    $("#button").mouseenter(function(){
        $("#button").fadeTo('fast',1);
    });
    $("#button").mouseleave(function(){
        $("#button").fadeTo('fast',0.2);
    });
    
});
