$.ajax({
  url: 'http://api.gbif.org/v1/species/search?q=Puma',
}).done(function(data) {
  console.log(data);
});