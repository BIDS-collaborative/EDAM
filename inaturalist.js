var cleaned=[];
for(a=0;a<100;a++){


$.ajax({
	url: "http://inaturalist.org/observations.json?q='Puma concolor'&per_page=200&page="+a


}

	).done(function(data){
		console.log(data);
		for(b=0;b<data.length;b++){
			if(data[b]!=null){
				var better={'latitude': data[b].latitude , 'longitude': data[b].longitude};
				console.log(better);
				cleaned.push(better);
				
			}
		}
		console.log(cleaned);
});


}

