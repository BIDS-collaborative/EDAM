// probably can be optimized more
function searchINaturalist(species){
  var api_data = [];
  var dfd_list = [];
  var dfd = $.Deferred();

  // initial request to get total entries
  $.ajax({
    url: "http://inaturalist.org/observations.json?q=" + species + "&per_page=200&page=1"
  }).done(function(data, textStatus, jqXHR){
    // read header to get total entries
    var headers = jqXHR.getResponseHeader('X-Total-Entries');
    for(i = 0; i < data.length; i++){
      if(data[i] != null){
        var cleaned_data = {'latitude': data[i].latitude , 'longitude': data[i].longitude};
        api_data.push(cleaned_data);
      }
    }

    // read all pages
    for(p = 2; p < Math.floor(headers/200)+2; p++){
      // add a deferred for each ajax request
      dfd_list.push($.Deferred());
      $.ajax({
        url: "http://inaturalist.org/observations.json?q=" + species + "&per_page=200&page=" + p
      }).done(function(data,request){  
        for(i = 0; i < data.length; i++){
          if(data[i] != null){
            var cleaned_data = {'latitude': data[i].latitude , 'longitude': data[i].longitude};
            api_data.push(cleaned_data);
          }
        }
        // resolve each deferred in list
        dfd_list.pop().resolve();
      });
    }   
    // resolve initial deferred once deferred list is filled
    dfd.resolve();
  });

  // wait for page header to return
  dfd.done(function() {
    // wait for all data to load
    $.when.apply(this, dfd_list).done(function() {
      var result = {'species': species, 'taxonomy': null}
      if(api_data.length == 0){
        return null
      }
      return result;
    });
  });
}
