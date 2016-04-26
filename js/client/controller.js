var app = angular.module('edamApp', []);

var databases = {
                'idigbio': {'basic': search_idigbio, 'location': search_idigbio_location},
                'gbif': {'basic': search_gbif, 'location': search_gbif_location},
                'iucn': {'basic': search_iucn, 'location': search_iucn_location},
                'inaturalist': {'basic': search_inat, 'location': search_inat_location},
                'nas': {'basic':search_nas, 'location': search_nas_location}
                };

searchDatabase = function(query, location, search_dfd, results, img_result, species_info) {
  var all_dfd = [];

  // search each database
  $.each(databases, function(db, func) {
    var api_dfd = $.Deferred()

    // add deferred to list of deferreds
    all_dfd.push(api_dfd);

    // run search to upate results
    if (location != null && location.length > 0) {
      func['location'](query, location, api_dfd, results);
    } else {
      func['basic'](query, api_dfd, results);
    }
  });

  // search for common name and taxonomy
  var api_dfd = $.Deferred()
  all_dfd.push(api_dfd);
  get_species_info(query, api_dfd, species_info);

  // search for image
  var api_dfd = $.Deferred()
  all_dfd.push(api_dfd);
  search_img(query, api_dfd, img_result);

  // return results after all searches complete
  $.when.apply(this, all_dfd).done(function() {
    if ($.isEmptyObject(results)) {
      results['null'] = {'count': 'no results', 'database': 'no results'};
    }
    search_dfd.resolve();
  });
};

app.controller('searchController', function($scope) {
  // data model for results table
  $scope.search_result = {};
  $scope.img = null;

  $scope.search = function(query, location){
    // all search complete notifier

    var search_dfd = $.Deferred();

    // container object to modify
    var results = {};
    var species_info = {};
    var img_result = {};

    $scope.query = query;
    $scope.taxonomy = 'Loading...';
    $scope.common_name = 'Loading...';
    $scope.img = '';
    $scope.search_result = {'loading': {'database': 'Loading...', 'count': 'Loading...'}};

    // start database searches
    searchDatabase(query, location, search_dfd, results, img_result, species_info);

    // return when all searches are complete
    search_dfd.done(function() {
      // force update
      $scope.$apply(function() {
        $scope.search_result = results;
        $scope.taxonomy = species_info['taxonomy'];
        $scope.common_name = species_info['common_name'];
        $scope.img = img_result['img'];
      });
    });
  }
});

