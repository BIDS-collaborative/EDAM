// Module 1 gbif parsing Scheme developed by Jonathan Wang
// Call this to asynchronously fetch the data 
app.factory('gbifAPI', ['$http', function($http) { 
  return $http.get('http://api.gbif.org/v1/occurrence/search?scientificName=Puma concolor&limit=300&offset=1') 
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
  
    for (var i = 0; i < data.results.length; i++) {
        var ref = data.results[i].datasetName;
        // only data from inaturalist has a field labeled datasetName
        if (typeof ref == "undefined") {
            var data_extract = {
              'kingdom': data.results[i].kingdom,
              'phylum': data.results[i].phylum,
              'order': data.results[i].order,
              'family': data.results[i].family,
              'genus': data.results[i].genus,
              'species': data.results[i].species,
              'country': data.results[i].country,
              'latitude': data.results[i].decimalLatitude,
              'longitude': data.results[i].decimalLongitude,
              'references': data.results[i].institutionCode
              };
          //console.log(data_extract);
            extract_results.push(data_extract);
        }
    }

    // add cleaned results to object
    clean_data['results'] = extract_results;
    console.log(clean_data);

	return clean_data;
};
