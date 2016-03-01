// Module 1 gbif parsing Scheme developed by Jonathan Wang
// Call this to asynchronously fetch the data 
app.factory('gbifAPI', ['$http', function($http) { 
  return $http.get('http://api.gbif.org/v1/species/search?q=Puma concolor') 
            .success(function(data) { 
              return data; 
            }) 
            .error(function(err) { 
              return err; 
            }); 
}]);

pasringScheme_gbif = function(data) {
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
