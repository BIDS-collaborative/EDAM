

function searchINat(speciesname){

var cleaned=[];

var jqXHR=$.ajax({
	url: "http://inaturalist.org/observations.json?q="+speciesname+"&per_page=200&page=1"


}

	).done(function(data){
    var headers = jqXHR.getResponseHeader('X-Total-Entries');
    console.log(headers);
    //console.log(data);
	//console.log(data);
		for(b=0;b<data.length;b++){
			if(data[b]!=null){
				var better={'latitude': data[b].latitude , 'longitude': data[b].longitude};
				//console.log(better);
				cleaned.push(better);
				
			}
		}

		for(a=2;a<Math.floor(headers/200)+2;a++){


		
$.ajax({
	url: "http://inaturalist.org/observations.json?q="+speciesname+"&per_page=200&page="+a


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

		console.log(cleaned);
		

	/*	
		for(a=0;a<cleaned.length;a++){
	var lat=cleaned[a].latitude;
	var lon = cleaned[a].longitude;
	
	$.ajax({
		url: "https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+lon+"&sensor=false&key=AIzaSyBnPTDQG8hVlUwSdf6Fvwg4AQf7_IJunVE"


	}	

		).done(function(data){
  		
		
});


}

*/
});




		}
		
});

var existenceline={'species':speciesname,'exists':true}
alert(cleaned.length);
if (cleaned.length==0){
	existenceline['exists']=false;
}
return existenceline;
}

