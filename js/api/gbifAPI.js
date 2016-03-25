function search_gbif(query, api_dfd, results) {
  // call gbif service
  $.ajax({
    // currently gets 5 results
    url: 'http://api.gbif.org/v1/occurrence/search?scientificName=' + query + '&limit=5&offset=0',
  }).done(function(data) {
    // check if there are results
    if (data.results.length != 0) {
      // extract taxonomy from first entry
      var resultObject = data.results[0];
      var taxon = [resultObject.kingdom, resultObject.phylum, resultObject.order, resultObject.family, resultObject.genus];
      
      // update results object
      results['gbif'] = {'name': query, 'taxonomy': taxon.join(), 'database': 'gbif'};
    }

    // notify search complete
    api_dfd.resolve();
  });
}
