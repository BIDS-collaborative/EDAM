// find mode of array
function mode(array) {
  if (array.length == 0) {
    return null;
  }
  var modeMap = {};
  var maxEl = array[0];
  var maxCount = 1;

  $.each(array, function(index, value) {
    if (value != 'undefined') {
      if (!modeMap[value]) {
        modeMap[value] = 1;
      } else {
        modeMap[value]++;  
      }
      if(modeMap[value] > maxCount) {
        maxEl = value;
        maxCount = modeMap[value];
      }
    }
  });
  return maxEl;
}

function search_idigbio(query, api_dfd, results) {
  // call idigbio service
  $.ajax({
    url: 'https://search.idigbio.org/v2/search/records/',
    dataType: 'json',
    contentType: 'application/json',
    type: 'POST',
    // update search limit
    data: JSON.stringify({ limit:5, rq:{scientificname: query} })
  }).done(function(data) {
    // process resulting data
    var taxon = [];
    var count = data.itemCount;
    $.each(data.items, function(index, value) {
      var resultObject = value.indexTerms;
      if (resultObject.highertaxon) {
        taxon.push(resultObject.highertaxon);
      }
    });

    // check if there are any results
    if (data.items.length !=  0) {
      results['idigbio'] = {'name': query, 'taxonomy': mode(taxon), 'count': count, database: 'idigbio'};
    }
    
    // notify done to controller
    api_dfd.resolve();
  });
}