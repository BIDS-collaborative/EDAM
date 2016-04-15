function search_nas(query, api_dfd, results) {
var cleaned=[];
var space = query.indexOf(" ");
var genus = "";
var species = "";
if (space > 0) {
	genus = query.substring(0,space);
	species = query.substring(space + 1);
}else {
	//alert("invalid");//fix me
	results['NAS'] = {'name': query, 'taxonomy': 'no results', 'count': 'no results', 'database': 'Nonindigenous Aquatic Species'};
	api_dfd.resolve();

}
var jqXHR=$.ajax({
	url: "http://nas.er.usgs.gov/api/v1/occurrence/search?genus="+genus+"&species="+species+"&api_key=7F0F12B9-BFF1-4266-A0B5-77C4115CA7B8",
	dataType: 'jsonp'
}

	).done(function(data){
    
   
		
		if(data.results.length>0) {
			var count = data.count;
			var info = data.results[0];
		 	var taxon = [info.group, info.family, info.genus, info.species];
			results['NAS'] = {'name': query, 'taxonomy': taxon.join(), 'count': count, 'database': 'Nonindigenous Aquatic Species'};
		
		} else {
			results['NAS'] = {'name': query, 'taxonomy': 'no results', 'count': 'no results', 'database': 'Nonindigenous Aquatic Species'};
		}
	
	api_dfd.resolve();
	});

}


function search_nas_location(query, location, api_dfd, results) {
	var space = query.indexOf(" ");
	var genus = "";
	var species = "";
	if (space > 0) {
		genus = query.substring(0,space);
		species = query.substring(space + 1);
	} else {
		//alert("invalid"); //fix me
		results['NAS'] = {'name': query, 'taxonomy': 'no results', 'count': 'no results', 'database': 'Nonindigenous Aquatic Species'};
		api_dfd.resolve();
	}
	if (location === "USA" || location === "United States") {
	var jqXHR=$.ajax({
		url: "http://nas.er.usgs.gov/api/v1/occurrence/search?genus="+genus+"&species="+species+"&api_key=7F0F12B9-BFF1-4266-A0B5-77C4115CA7B8",
		dataType: 'jsonp'

	}

	).done(function(data){
    
    
		var count = data.count;
		var info = data.results[0];
		 var taxon = [info.group, info.family, info.genus, info.species];
		if (count > 0) {
			results['NAS'] = {'name': query, 'taxonomy': taxon.join(), 'count': count, 'database': 'Nonindigenous Aquatic Species'};
		
		}
		else {
			results['NAS'] = {'name': query, 'taxonomy': 'no results', 'count': 'no results', 'database': 'Nonindigenous Aquatic Species'};
		}
		api_dfd.resolve();
	});


	}
	else {
		results['NAS'] = {'name': query, 'taxonomy': 'no results', 'count': 'no results', 'database': 'Nonindigenous Aquatic Species'};
		api_dfd.resolve();
	}
}
