//Module4 speciesplus parsingScheme developed by numfah
var config_speciesplus = {
	url:'http://api.speciesplus.net/api/v1/taxon_concepts.json?name=Puma concolor',
	responseType: 'json',
	method: "GET",
  	headers: {'X-Authentication-Token': 'WYjddmVCPlzeonLKsf39rwtt'}
};


app.factory('speciesplusAPI', ['$http', function($http) { 
  return $http(config_speciesplus)
            .success(function(data) { 
        		return data;
      		})
            .error(function(err) { 
              	return err; 
            }); 
}]);

var myurl;

pasringScheme_speciesplus = function(data) {
	var clean_data_speciesplus = {};
    var extract_results = [];
    // extract common names, higher taxa, and taxon ID
    var data_extract = {
        'common_names': data.taxon_concepts[0].common_names,
        'higher_taxa': data.taxon_concepts[0].higher_taxa,
    };
   
    extract_results.push(data_extract);
    var taxon_id = data.taxon_concepts[0].id;
    myurl = 'http://api.speciesplus.net/api/v1/taxon_concepts/'+taxon_id+'/distributions.json';

    // add cleaned results to object
    clean_data_speciesplus['results'] = extract_results;
    return clean_data_speciesplus;
    //console.log(clean_data_speciesplus); 

};
