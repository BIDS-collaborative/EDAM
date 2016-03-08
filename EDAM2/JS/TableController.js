// Module
var app = angular.module("myApp", []);

var databases = ["gbif", "iDigBio", "speciesplus", "inaturalist"];

searchDatabase = function(keyWord) {
    var results = {};
    for (i = 0; i < databases.length; i++)  {
        database = databases[i];
        console.log(database);
        if (database === "gbif") {
            results[database] = search_gbif(keyWord);
        }
        if (database === "iDigBio") {
            results[database] = search_idigbio(keyWord);
        }
        if (database === "speciesplus") {
            results[database] = search_speciesplus(keyWord);
        }
        if (database === "inaturalist") {  
            results[database] = search_inaturalist(keyWord);
        }
    }
    return results;
};








































