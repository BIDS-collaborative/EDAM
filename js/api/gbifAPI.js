function search_gbif(query, api_dfd, results) {
  // call gbif service
  $.ajax({
    // currently gets 5 results
    url: 'http://api.gbif.org/v1/occurrence/search?scientificName=' + query + '&limit=5&offset=0',
  }).done(function(data) {
    // check if there are results
    if (data.results.length != 0) {
      var count = data.count;
      
      // update results object
      results['gbif'] = {'count': count, 'database': 'GBIF'};
    } else {
      results['gbif'] = {'count': 'no results', 'database': 'GBIF'};
    }

    // notify search complete
    api_dfd.resolve();
  });
}

function search_gbif_location(query, location, api_dfd, results) {
  // call gbif service
  $.ajax({
    // currently gets 5 results
    url: 'http://api.gbif.org/v1/occurrence/search?scientificName=' + query + '&limit=5&offset=0',
  }).done(function(data) {
    // check if there are results
    if (data.results.length != 0) {
      // extract taxonKey from first entry
      var taxonKey = data.results[0].taxonKey;
    }

    // get 2 letter country code
    countryCode = getCountryCode(location);

    // if country code found, search by location
    if (countryCode != location) {
      $.ajax({
        url: 'http://api.gbif.org/v1/occurrence/count?taxonKey=' + taxonKey + '&country=' + countryCode,
      }).done(function(count) {
        // data is the count
        results['gbif'] = {'count' : count, 'database': 'GBIF'};
      });
    } else {
      results['gbif'] = {'count': 'no results', 'database': 'GBIF'};
    }

    // notify search complete
    api_dfd.resolve();
  });
}

