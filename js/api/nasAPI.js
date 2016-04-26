function search_nas(query, api_dfd, results) {
  var cleaned = [];
  var space = query.indexOf(' ');
  var genus = '';
  var species = '';
  if (space > 0) {
    genus = query.substring(0, space);
    species = query.substring(space + 1);
  } else {
    results['nas'] = {'count': 'no results', 'database': 'NAS'};
    api_dfd.resolve();
  }
  $.ajax({
    url: 'http://nas.er.usgs.gov/api/v1/occurrence/search?genus=' + genus+'&species=' + species + '&api_key=7F0F12B9-BFF1-4266-A0B5-77C4115CA7B8',
    dataType: 'jsonp'
  }).done(function(data) {
    if (data.results.length>0) {
      var count = data.count;
      results['nas'] = {'count': count, 'database': 'NAS'};
    } else {
      results['nas'] = {'count': 'no results', 'database': 'NAS'};
    }
    api_dfd.resolve();
  });
}

function search_nas_location(query, location, api_dfd, results) {
  var space = query.indexOf(' ');
  var genus = '';
  var species = '';
  if (space > 0) {
    genus = query.substring(0,space);
    species = query.substring(space + 1);
  } else {
    results['nas'] = {'count': 'no results', 'database': 'NAS'};
    api_dfd.resolve();
  }
  // only has US data
  if (location === 'USA' || location === 'United States') {
    $.ajax({
      url: 'http://nas.er.usgs.gov/api/v1/occurrence/search?genus=' + genus + '&species=' + species + '&api_key=7F0F12B9-BFF1-4266-A0B5-77C4115CA7B8',
      dataType: 'jsonp'
    }).done(function(data) {
      var count = data.count;
      if (count > 0) {
        results['nas'] = {'count': count, 'database': 'NAS'};
      } else {
        results['nas'] = {'count': 'no results', 'database': 'NAS'};
      }
      api_dfd.resolve();
    });
  }
  else {
    results['nas'] = {'count': 'no results', 'database': 'NAS'};
    api_dfd.resolve();
  }
}
