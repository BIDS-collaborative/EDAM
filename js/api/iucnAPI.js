function search_iucn(query, api_dfd, results) {
var cleaned=[];

var jqXHR=$.ajax({
	url: "http://apiv3.iucnredlist.org/api/v3/species/" + query + "?token=49a8a2b7e481a521cb4c4c5360044de9a81c5fac89bd5db1db80f733e93126db"


}

	).done(function(data){
    
   
		
		if(data.result.length>0) {
				var info = data.result[0];
		 		var taxon = [info.kingdom, info.phylum, info.order, info.family, info.genus];
				results['iucn'] = {'name': query, 'taxonomy': taxon, 'count': 1, 'database': 'IUCN'};
		
		}
	
	api_dfd.resolve();
	});

}


function search_iucn_location(query, location, api_dfd, results) {
	api_dfd.resolve();

}

