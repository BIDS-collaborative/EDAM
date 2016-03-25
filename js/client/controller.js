var app = angular.module('edamApp', []);

var databases = {'idigbio': search_idigbio, 'gbif': search_gbif};

searchDatabase = function(query, search_dfd, results) {
  var all_dfd = [];

  // search each database
  $.each(databases, function(db, func) {
    // search complete notifier
    var api_dfd = $.Deferred();

    // add deferred to list of deferreds
    all_dfd.push(api_dfd);
    
    // run search to upate results
    func(query, api_dfd, results);
  });

  // return results after all searches complete
  $.when.apply(this, all_dfd).done(function() {
    if ($.isEmptyObject(results)) {
      results['null'] = {'name': 'no results', 'taxonomy': 'no results', 'database': 'no results'};
    }
    search_dfd.resolve();
  });
};

app.controller('searchController', function($scope) {
  // data model for results table
  $scope.searchResult = {};

  $scope.search = function(query){
    // all search complete notifier
    var search_dfd = $.Deferred();

    // container object to modify
    var results = {};

    // start database searches
    searchDatabase(query, search_dfd, results);

    // return when all searches are complete
    search_dfd.done(function() {
      // force update
      $scope.$apply(function() {
        $scope.searchResult = results;
      });
    });
  }
});


