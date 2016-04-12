
 //this function is used for keyword search.
function search_inat(query, api_dfd, results) {
var cleaned=[];
var count = 0;

var jqXHR=$.ajax({
	url: "http://api.inaturalist.org/v1/observations?q="+query+"&per_page=500&order=desc&order_by=created_at"

	}).done(function(data){
		var count_dfd = $.Deferred();
    	var jqXHR=$.ajax({
			url: "http://api.inaturalist.org/v1/observations/species_counts?q="+query
		}).done(function(data){
   			if (data.results.length != 0) {
    			count = data.results[0].count;
    		}
    		count_dfd.resolve();
    	});
		count_dfd.done(function() {
			if(data.results.length != 0) {
				results['inaturalist'] = {'name': query, 'taxonomy': "not available", 'count': count, 'database': 'iNaturalist'};
			} else {
				results['inaturalist'] = {'name': query, 'taxonomy': "no results", 'count': 'no results', 'database': 'iNaturalist'};
			}
			api_dfd.resolve();
		});

	});
}



function search_inat_location(query, location, api_dfd, results) {
	api_dfd.resolve();
}

