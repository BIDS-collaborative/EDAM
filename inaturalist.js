var cleaned=[];


var jqXHR=$.ajax({
	url: "http://inaturalist.org/observations.json?q='Puma concolor'&per_page=200&page=1"


}

	).done(function(data){
    var headers = jqXHR.getAllResponseHeaders();
    console.log(headers);
    console.log(data);
	//console.log(data);
		for(b=0;b<data.length;b++){
			if(data[b]!=null){
				var better={'latitude': data[b].latitude , 'longitude': data[b].longitude};
				//console.log(better);
				cleaned.push(better);
				
			}
		}
		//console.log(cleaned);
});



$.ajax({
	url: "http://inaturalist.org/observations.json?q='Puma concolor'&per_page=200&page=2"


}

	).done(function(data,request){
    
    
	//console.log(data);
		for(b=0;b<data.length;b++){
			if(data[b]!=null){
				var better={'latitude': data[b].latitude , 'longitude': data[b].longitude};
				//console.log(better);
				cleaned.push(better);
				
			}
		}
		//console.log(cleaned);
});


