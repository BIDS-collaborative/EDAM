var app = angular.module('edamApp', []);

var databases = {
                'idigbio': {'basic': search_idigbio, 'location': search_idigbio_location},
                'gbif': {'basic': search_gbif, 'location': search_gbif_location},
                'iucn': {'basic': search_iucn, 'location': search_iucn_location},
                'inaturalist': {'basic': search_inat, 'location': search_inat_location},
                'nas': {'basic':search_nas, 'location': search_nas_location}
                };

searchDatabase = function(query, locationQuery, search_dfd, results, imgResult, commonNameResult) {

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

  // search for image
  var api_dfd = $.Deferred();
  all_dfd.push(api_dfd);
  search_img(query, api_dfd, imgResult);

  // search for common name
  var api_dfd = $.Deferred();
  all_dfd.push(api_dfd);
  getCommonNameTaxonomy_IUCN(query, api_dfd, commonNameResult);



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

    // image result
    var imgResult = {};
    // common name result
    var commonNameResult = {};

    $scope.name = query;

    $scope.searchResultTaxonomy = "";

    $scope.searchResultCommonName = "";



    // start database searches
    searchDatabase(query, locationQuery, search_dfd, results, imgResult, commonNameResult);

    // return when all searches are complete
    search_dfd.done(function() {
      // force update
      $scope.$apply(function() {
        $scope.searchResult = results;
        $scope.imageUrl = imgResult['img'];

        //console.log($scope.imageUrl);
        // combine taxonomy together
        $.each($scope.searchResult, function(db, result) {
          if (db === "iucn") {
            $scope.searchResultTaxonomy += result['taxonomy'] + ",\t";
          }
        });
        //console.log(results)

        console.log(commonNameResult);

        // combine commonname together
        $.each(commonNameResult, function(db, result) {
          if (result['common name'] != "no results") {
            $scope.searchResultCommonName += result['common name'] + ",\t";;
          }
        });
        if ($scope.searchResultCommonName.length === 0) {
          $scope.searchResultCommonName += 'no results';
        }
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
