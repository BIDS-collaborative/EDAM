app.controller('TableController', ['$scope', function($scope) { 

    $scope.API1 = 'http://api.gbif.org/v1/species/search?q=Puma concolor';
	$scope.pasringScheme1 = function(data) {
		// print all results from API
		var clean_data = {};
		console.log(data);
		var extract_results = []
  
		// extract canonicalName and species
		for (var i = 0; i < data.results.length; i++) {
		  var data_extract = {
			'name': data.results[i].canonicalName,
			'species': data.results[i].species
		  };
		  console.log(data_extract);
		  extract_results.push(data_extract);
		}
  
		// add cleaned results to object
		clean_data['results'] = extract_results;

		return clean_data;
  	};



  	$scope.API2 = "http://inaturalist.org/observations.json?q='Puma concolor'&per_page=200&page="
  	$scope.pasringScheme2 = function(data){
  		var cleaned=[];
		console.log(data);
		for(b=0;b<data.length;b++){
			if(data[b]!=null){
				var better={'latitude': data[b].latitude , 'longitude': data[b].longitude};
				console.log(better);
				cleaned.push(better);
			}
		}
		console.log(cleaned);
		return cleaned;
	};



    //a working method to return a json object
	$scope.getJson = function getJson(url) {
 		return JSON.parse($.ajax({
    		type: 'GET',
     		url: url,
    		dataType: 'json',
    		global: false,
    		async:false,
    		success: function(data) {
      		   	return data
    		}
 		}).responseText);
	};

	//call this to parse the url with a specific parsingScheme
	$scope.parse = function(url, iteration, pasringScheme) {
		return pasringScheme($scope.getJson(url));
	}
    
    //results are stored here
	$scope.dataResult = $scope.parse($scope.API1, 1, $scope.pasringScheme1);

}]);





