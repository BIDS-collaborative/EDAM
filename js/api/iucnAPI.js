function search_iucn(query, api_dfd, results) {
  var cleaned = [];

  $.ajax({
    url: 'http://apiv3.iucnredlist.org/api/v3/species/' + query + '?token=49a8a2b7e481a521cb4c4c5360044de9a81c5fac89bd5db1db80f733e93126db'
  }).done(function(data) {
    if (data.result.length > 0) {
      // IUCN has no occurrences
      results['iucn'] = {'count': 1, 'database': 'IUCN'};
    } else {
      results['iucn'] = {'count': 'no results', 'database': 'IUCN'};
    }
    api_dfd.resolve();
  });
}

function search_iucn_location(query, location, api_dfd, results) {
  $.ajax({
    url: 'http://apiv3.iucnredlist.org/api/v3/species/countries/name/' + query + '?token=49a8a2b7e481a521cb4c4c5360044de9a81c5fac89bd5db1db80f733e93126db'
  }).done(function(data) {
    if (data.result != 0) {
      var countries = data.result;
      var exist = false;
      $.each(countries, function(i, v) {
        if (v.country === location) {
          results['iucn'] = {'count' : 1, 'database': 'IUCN'};
          exist = true
        }
      });
      if (!exist) {
        results['iucn'] = {'count': 'no results', 'database': 'IUCN'};
      }
    } else {
      results['iucn'] = {'count': 'no results', 'database': 'IUCN'};
    }
    api_dfd.resolve();
  });
}

function get_species_info(query, api_dfd, results) {
  var cleaned = [];

  $.ajax({
    url: 'http://apiv3.iucnredlist.org/api/v3/species/' + query + '?token=49a8a2b7e481a521cb4c4c5360044de9a81c5fac89bd5db1db80f733e93126db'
  }).done(function(data) {
    if (data.result.length>0) {
      var info = data.result[0];
      var taxon = [info.kingdom, info.phylum, info.class, info.order, info.family, info.scientific_name];
      var common_name = info.main_common_name;
      results['taxonomy'] = taxon.map(capitalize).join(' ');
      results['common_name'] = common_name;
    }
    api_dfd.resolve();
  });
}

