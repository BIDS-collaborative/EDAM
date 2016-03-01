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