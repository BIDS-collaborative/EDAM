function search_idigbio(query, api_dfd, results) {
  // call idigbio service
  $.ajax({
    url: 'https://search.idigbio.org/v2/search/records/',
    dataType: 'json',
    contentType: 'application/json',
    type: 'POST',
    // update search limit
    data: JSON.stringify({ limit: 5, rq: {scientificname: query} })
  }).done(function(data) {
    // process resulting data
    var count = data.itemCount;

    // check if there are any results
    if (data.items.length !=  0) {
      results['idigbio'] = {'count': count, database: 'iDigBio'};
    } else {
      results['idigbio'] = {'count': 'no results', database: 'iDigBio'};
    }
    
    // notify done to controller
    api_dfd.resolve();
  });
}

function search_idigbio_location(query, location, api_dfd, results) {
  // call idigbio service
  $.ajax({
    url: 'https://search.idigbio.org/v2/search/records/',
    dataType: 'json',
    contentType: 'application/json',
    type: 'POST',
    // update search limit
    data: JSON.stringify({ limit: 5, rq: {scientificname: query, country: location} })
  }).done(function(data) {
    // process resulting data
    var count = data.itemCount;

    // check if there are any results
    if (data.items.length !=  0) {
      results['idigbio'] = {'count': count, database: 'iDigBio'};
    } else {
      results['idigbio'] = {'count': 'no results', database: 'iDigBio'};
    }
    
    // notify done to controller
    api_dfd.resolve();
  });
}


