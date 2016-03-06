//Module3 iDigBio parsingScheme developed by Jong Ha Lee

var config_iDigBio = {
	url:'https://search.idigbio.org/v2/search/records/',
	responseType: 'json',
    contentType: 'application/json',
    method: "POST",
    data: JSON.stringify({limit:5000, rq:{scientificname:"puma concolor"}})
};

app.factory('iDigBioAPI', ['$http', function($http) { 
  return $http(config_iDigBio)
            .success(function(data) { 
              return data; 
            }) 
            .error(function(err) { 
              return err; 
            }); 
}]);



pasringScheme_iDigBio = function(data) {
  var clean_data = {}
  console.log(data);

  var extract_results = []; //to keep all extracted array of JSON object data

//Arrays for each attribute to get mode attribute
  var commonname = [];
  var scientificname = [];
  var country = [];

// extract relevant data for each individual observations:
  for (var i = 0; i < data.items.length; i++) { 
    var data_extract = {
      'common name': data.items[i].indexTerms.commonname,
      'scientific name': data.items[i].indexTerms.scientificname,
      'species': data.items[i].indexTerms.specificepithet,
      'genus': data.items[i].indexTerms.genus,
      'family': data.items[i].indexTerms.family,
      'order': data.items[i].indexTerms.order,
      'class': data.items[i].indexTerms.class,
      'phylum': data.items[i].indexTerms.phylum,
      'kingdom': data.items[i].indexTerms.kingdom,
      'higher taxonomy': data.items[i].indexTerms.highertaxon,
      //'location': data.items[i].indexTerms.geopoint,
      'country': data.items[i].indexTerms.country, 
      'sources': data.attribution
    };

    //aggregating attributes individually
    if(data_extract['common name'] != undefined)
      commonname.push(data_extract['common name']);
    if(data_extract['country'] != undefined)
      country.push(data_extract['country']);

    scientificname.push(data_extract['scientific name']);

    console.log(data_extract);
    extract_results.push(data_extract);
  }

//function to find mode for each observation attribute (pass in attribute arrays)
  function mode(array) {
    if(array.length == 0)
      return null;

    var modeMap = {};
    var maxEl = array[0], maxCount = 1;

    for(var i = 0; i < array.length; i++)
    {
      var el = array[i];
      if(el = "undefined")
        continue;
      if(modeMap[el] == null)
        modeMap[el] = 1;
      else
        modeMap[el]++;  
      if(modeMap[el] > maxCount)
      {
        maxEl = el;
        maxCount = modeMap[el];
      }
    }

    return maxEl;
  };

//Finding unique elements, specifically for country and commonname
  function find_unique(array) {
    var unique = [];
    var distinct = [];

    for(i = 0; i < array.length; i++){
      if(unique[array[i]]) continue;
      unique[array[i]] = true;
      distinct.push(array[i]);
    }

    return distinct;
  };

//General Data object
  var aggregate_gen_data = {
      'common name': find_unique(commonname),
      'scientific name': mode(scientificname),
      'species': data_extract.species,
      'genus': data_extract.genus,
      'family': data_extract.family,
      'order': data_extract.order,
      'class': data_extract.class,
      'phylum': data_extract.phylum,
      'kingdom': data_extract.kingdom,
      'higher taxonomy': data_extract['higher taxonomy'],
      'country': find_unique(country),
      'sources': data_extract.sources
  };

// add cleaned results to object
  clean_data['results'] = extract_results;
  clean_data['general_data'] = aggregate_gen_data;
  console.log(clean_data);
  return clean_data;
};