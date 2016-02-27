
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



// Module2 inaturalist parsingScheme developed by calvin

app.factory('inaturalistAPI', ['$http', function($http) { 
  return $http.get("http://inaturalist.org/observations.json?q='Puma concolor'&per_page=200&page=1") 
            .success(function(data) { 
              return data; 
            }) 
            .error(function(err) { 
              return err; 
            }); 
}]);


pasringScheme_inaturalistAPI = function(data){
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



//Module4 speciesplus parsingScheme developed by numfah
var config_speciesplus = {
	url:'http://api.speciesplus.net/api/v1/taxon_concepts.json?name=Puma concolor',
	responseType: 'json',
	method: "POST",
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


























