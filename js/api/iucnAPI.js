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
		
		} else {
			results['iucn'] = {'name': query, 'taxonomy': 'no results', 'count': 'no results', 'database': 'IUCN'};
		}
	
	api_dfd.resolve();
	});

}



function search_iucn_location(query, location, api_dfd, results) {
	var jqXHR=$.ajax({
	url: "http://apiv3.iucnredlist.org/api/v3/species/countries/name/"+query+"?token=49a8a2b7e481a521cb4c4c5360044de9a81c5fac89bd5db1db80f733e93126db"


}
).done(function(data){
		if (data.result != 0) {
			var countries = data.result;
			var exist = false;
			$.each(countries, function(i, v) {
				if (v.country === location) {
					var taxon = [v.kingdom, v.phylum, v.order, v.family, v.genus];
					results['iucn'] = {'name':query, 'taxonomy': taxon, 'count' : 1, 'database': 'IUCN'};
					exist = true
				}
			});
			if (!exist) {
				results['iucn'] = {'name': query, 'taxonomy': 'no results', 'count': 'no results', 'database': 'IUCN'};
			}
		} else {
			results['iucn'] = {'name': query, 'taxonomy': 'no results', 'count': 'no results', 'database': 'IUCN'};
		}
		api_dfd.resolve();
});

}



function getCommonNameTaxonomy_IUCN(query, api_dfd, results) {
var cleaned=[];

var jqXHR=$.ajax({
	url: "http://apiv3.iucnredlist.org/api/v3/species/" + query + "?token=49a8a2b7e481a521cb4c4c5360044de9a81c5fac89bd5db1db80f733e93126db"


}

	).done(function(data){
    
   
		
		if(data.result.length>0) {
				var info = data.result[0];
		 		var taxon = [info.kingdom, info.phylum, info.order, info.family, info.genus];
				var common_name = info.main_common_name;
				results['iucn'] = {'name': query, 'taxonomy': taxon, 'common name': common_name, 'database': 'IUCN'};
		
		}
	
	api_dfd.resolve();
	});

}

