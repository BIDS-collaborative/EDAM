var app = angular.module('myApp', []);
var clean_data = {};

$.ajax({
  // search taxonomy
  url: 'http://api.gbif.org/v1/species/search?q=Puma concolor',
}).done(function(data) {
  // print all results from API
  console.log(data);
  var extract_results = []

  // extract canonicalName and species
  for (var i = 0; i < data.results.length; i++) {
    var data_extract = {
      'name': data.results[i].canonicalName,
      'species': data.results[i].species
    };
    console.log(data_extract);
    extract_results.push(data_extract);
  }

  // add cleaned results to object
  clean_data['results'] = extract_results;
  console.log(clean_data);
});


app.controller('customersCtrl', function($scope) {
    $scope.names = [
      { "Name" : "Max Joe", "City" : "Lulea", "Country" : "Sweden" },
      { "Name" : "Manish", "City" : "Delhi", "Country" : "India" },
      { "Name" : "Koniglich", "City" : "Barcelona", "Country" : "Spain" },
      { "Name" : "Wolski", "City" : "Arhus", "Country" : "Denmark" }
    ];
});
