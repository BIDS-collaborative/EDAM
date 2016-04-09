var app = angular.module('edamApp', []);

var databases = {
                'idigbio': {'basic': search_idigbio, 'location': search_idigbio_location},
                'gbif': {'basic': search_gbif, 'location': search_gbif_location},
                'iucn': {'basic': search_iucn, 'location': search_iucn_location},
                'inaturalist': {'basic': search_inat, 'location': search_inat_location}
                };

searchDatabase = function(query, locationQuery, search_dfd, results) {

  var all_dfd = [];

  // search each database
  $.each(databases, function(db, func) {
    // search complete notifier
    var api_dfd = $.Deferred();

    // add deferred to list of deferreds
    all_dfd.push(api_dfd);

    // run search to upate results
    if (locationQuery != null && locationQuery.length > 0) {
      func['location'](query, locationQuery, api_dfd, results);
    } else {
      func['basic'](query, api_dfd, results);
    }
  });

  // return results after all searches complete
  $.when.apply(this, all_dfd).done(function() {
    if ($.isEmptyObject(results)) {
      results['null'] = {'name': 'no results', 'taxonomy': 'no results', 'count': 'no results', 'database': 'no results'};
    }
    search_dfd.resolve();
  });
};

app.controller('searchController', function($scope) {
  // data model for results table
  $scope.searchResult = {};

  $scope.search = function(query, locationQuery){
    // all search complete notifier
    var search_dfd = $.Deferred();

    // container object to modify
    var results = {};


    // start database searches
    searchDatabase(query, locationQuery, search_dfd, results);

    // return when all searches are complete
    search_dfd.done(function() {
      // force update
      $scope.$apply(function() {
        $scope.searchResult = results;
        console.log(results)
      });
    });
  }
});

$(function() {
    var availableTags = [
      "ActionScript",
      "AppleScript",
      "Asp",
      "BASIC",
      "C",
      "C++",
      "Clojure",
      "COBOL",
      "ColdFusion",
      "Erlang",
      "Fortran",
      "Groovy",
      "Haskell",
      "Java",
      "JavaScript",
      "Lisp",
      "Perl",
      "PHP",
      "Python",
      "Ruby",
      "Scala",
      "Scheme",
      "puma",
      "puma concolor"
    ];
    $( ".form-control" ).autocomplete({
      source: availableTags
    });
  });
