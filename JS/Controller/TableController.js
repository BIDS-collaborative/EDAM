// Module
var app = angular.module("myApp", []);

var databases = ["gbif", "iDigBio", "speciesplus", "inaturalist"];

var searchDatabase = function(keyWord) {
    results = {};
    for (database in databases):
        if (database === "gbif") {
            result[database] = search_gbif(keyWord);
        }
        if (database === "iDigBio") {
            result[database] = search_iDigBio(keyWord);
        }
        if (database === "speciesplus") {
            result[database] = search_speciesplus(keyWord);
        }
        if (database === "inaturalist") {  
            result[database] = search_inaturalist(keyWord);
        }
    return results;
}

app.controller('TableController', ['$scope', 'gbifAPI', 'iDigBioAPI','speciesplusAPI', 'inaturalistAPI', 
	function($scope, gbifAPI, iDigBioAPI, speciesplusAPI, inaturalistAPI) {

	gbifAPI.success(function(data) {
		//$scope.dataResult_gbif = pasringScheme_gbif(data);
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

    $scope.searchResponse = searchResult;

}]);







































