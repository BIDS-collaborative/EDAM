
// Input Handler
var keyWord

$(document).ready(function(){
    $("#button").click(function(){
        keyWord = $('input[name=KeyWord]').val();    
        	if (keyWord.toLowerCase() === "gbif") {
       			window.location = "./gbifTable.html";
        	} else if (keyWord.toLowerCase() === "idigbio") {
				window.location = "./idigbioTable.html";
        	} else if (keyWord.toLowerCase() === "inaturalist") {
				window.location = "./inaturalistTable.html";
        	} else {
        		window.location = "./PageSkeleton.html";
        	}
    });
    $("form").keypress(function(e) {
    	if(e.which == 13) {
        	keyWord = $('input[name=KeyWord]').val();    
        	if (keyWord.toLowerCase() === "gbif") {
       			window.location = "./gbifTable.html";
        	} else if (keyWord.toLowerCase() === "idigbio") {
				window.location = "./idigbioTable.html";
        	} else if (keyWord.toLowerCase() === "inaturalist") {
				window.location = "./inaturalistTable.html";
        	} else {
        		window.location = "./PageSkeleton.html";
        	}
    	}
    });
    $("#button").mouseenter(function(){
        $("#button").fadeTo('fast',1);
    });
    $("#button").mouseleave(function(){
        $("#button").fadeTo('fast',0.2);
    });
    
});






// Module
var app = angular.module("myApp", []);


app.controller('TableController', ['$scope', 'gbifAPI', 'iDigBioAPI','speciesplusAPI', 'inaturalistAPI', 
	function($scope, gbifAPI, iDigBioAPI, speciesplusAPI, inaturalistAPI) { 


	gbifAPI.success(function(data) {
		$scope.dataResult_gbif = pasringScheme_gbif(data);
	});

	iDigBioAPI.success(function(data) {
		$scope.dataResult_iDigBio = pasringScheme_iDigBio(data);
	});

	speciesplusAPI.success(function(data) {
		$scope.dataResult_speciesplus = pasringScheme_speciesplus(data);
	});


	inaturalistAPI.success(function(data) {
		$scope.dataResult_inaturalistAPI = pasringScheme_inaturalistAPI(data);
	});



}]);







































