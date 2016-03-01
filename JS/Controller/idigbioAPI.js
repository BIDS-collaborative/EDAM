//Module3 iDigBio parsingScheme developed by Jong Ha Lee

var config_iDigBio = {
	url:'https://search.idigbio.org/v2/search/records/',
	responseType: 'json',
    contentType: 'application/json',
    method: "POST",
    data: JSON.stringify({limit:5000, rq:{scientificname:"puma concolor"}})
};

app.factory('iDigBioAPI', ['$http', function($http) { 
  return $http(config_iDigBio)
            .success(function(data) { 
              return data; 
            }) 
            .error(function(err) { 
              return err; 
            }); 
}]);



pasringScheme_iDigBio = function(data) {
	var clean_data = {};
	console.log(data);

	var extract_results = []

	// extract relevant data:
	for (var i = 0; i < data.items.length; i++) { 
    	var data_extract = {
      	'common name': data.items[i].indexTerms.commonname,
      	'scientific name': data.items[i].indexTerms.scientificname,
      	'species': data.items[i].indexTerms.specificepithet,
      	'genus': data.items[i].indexTerms.genus,
      	'family': data.items[i].indexTerms.family,
      	'order': data.items[i].indexTerms.order,
      	'class': data.items[i].indexTerms.class,
      	'phylum': data.items[i].indexTerms.phylum,
      	'kingdom': data.items[i].indexTerms.kingdom,
      	'location': data.items[i].indexTerms.geopoint,
      	'location name': data.items[i].indexTerms.verbatimlocality,
      	'taxonomy': data.items[i].indexTerms.highertaxon,
      	//'sources': data.items[i].data.dcterms:bibliographicCitation// NOTE: Couldn't use :
    	};
    	console.log(data_extract);
    	extract_results.push(data_extract);
  	}

  	// add cleaned results to object
  	clean_data['results'] = extract_results;
  	console.log(clean_data);
  	return clean_data
};