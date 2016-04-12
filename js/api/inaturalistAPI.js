
 //this function is used for keyword search.
function search_inat(query, api_dfd, results) {
var cleaned=[];

var jqXHR=$.ajax({
	url: "http://api.inaturalist.org/v1/observations?q="+query+"&per_page=500&order=desc&order_by=created_at"


}

	).done(function(data){
    
		if(data.results.length != 0) {
			var count = data.results[0].count;
			results['inaturalist'] = {'name': query, 'taxonomy': "not available", 'count': headers, 'database': 'iNaturalist'};
		}
		api_dfd.resolve();

	});
}



function search_inat_location(query, location, api_dfd, results) {
	api_dfd.resolve();
}

