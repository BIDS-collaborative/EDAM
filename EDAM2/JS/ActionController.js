// Input Handler
var keyWord = "Default"
var searchResult;

$(document).ready(function(){
    $("#button").click(function(){
        keyWord = $('input[name=KeyWord]').val();
        results = searchDatabase(keyWord);
        console.log(results)
        $(".outPut").append("<table><thead><tr><th colspan=3 class = 'title'>" + keyWord + "</th> </tr>");
        $(".outPut").append("<tr><th> Source Database </th><th> Name </th> <th> Taxonomy </th></tr> </thead>");
        $(".outPut").append("<tbody>");
        for (database in results) {
            result = results[database];
            $(".outPut").append("<tr><td>" + database + "</td> <td>" + result[0] + "</td> <td>" + result[1] + "</td> </tr>");
        }
        $(".outPut").append("</tbody> </table>");        
    });
    $("form").keypress(function(e) {
        keyWord = $('input[name=KeyWord]').val();
        results = searchDatabase(keyWord);
        $(".outPut").append("<table><thead><tr><th colspan=3 class = 'title'>" + keyWord + "</th> </tr>");
        $(".outPut").append("<tr><th> Source Database </th><th> Name </th> <th> Taxonomy </th></tr> </thead>");
        $(".outPut").append("<tbody>");
        for (database in results) {
            result = results[database];
            $(".outPut").append("<tr><td>" + database + "</td> <td>" + result[0] + "</td> <td>" + result[1] + "</td> </tr>");
        }
        $(".outPut").append("</tbody> </table>");
    });
    $("#button").mouseenter(function(){
        $("#button").fadeTo('fast',1);
    });
    $("#button").mouseleave(function(){
        $("#button").fadeTo('fast',0.2);
    });
    
});
