
for(a=0;a<100;a++){


$.ajax({
	url: "http://inaturalist.org/observations.json?q='Puma concolor'&per_page=200&page="+a


}

	).done(function(data){
		console.log(data);
});


}

