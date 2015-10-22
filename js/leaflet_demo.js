$(document).ready(function() {
  var map_all = L.map('map_all').setView([22.0833, -129.5000], 3);

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
  maxZoom: 18,
  id: 'koalaboy808.kf3oj9o7',
  accessToken: 'pk.eyJ1Ijoia29hbGFib3k4MDgiLCJhIjoiQlkzb3l0USJ9.o-SHU46rak_miT5dRXIhaw'
  }).addTo(map_all);

  var map = L.map('map').setView([22.0833, -159.5000], 9);

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
  maxZoom: 18,
  id: 'koalaboy808.kf3oj9o7',
  accessToken: 'pk.eyJ1Ijoia29hbGFib3k4MDgiLCJhIjoiQlkzb3l0USJ9.o-SHU46rak_miT5dRXIhaw'
  }).addTo(map);

  var map1 = L.map('map1').setView([-17.5333, -149.8333], 9);

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
  maxZoom: 18,
  id: 'koalaboy808.kf3oj9o7',
  accessToken: 'pk.eyJ1Ijoia29hbGFib3k4MDgiLCJhIjoiQlkzb3l0USJ9.o-SHU46rak_miT5dRXIhaw'
  }).addTo(map1);

  var map2 = L.map('map2').setView([48.5353, -123.0311], 9);

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
  maxZoom: 18,
  id: 'koalaboy808.kf3oj9o7',
  accessToken: 'pk.eyJ1Ijoia29hbGFib3k4MDgiLCJhIjoiQlkzb3l0USJ9.o-SHU46rak_miT5dRXIhaw'
  }).addTo(map2);

  var map3 = L.map('map3').setView([-0.6667, -90.5500], 9);

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
  maxZoom: 18,
  id: 'koalaboy808.kf3oj9o7',
  accessToken: 'pk.eyJ1Ijoia29hbGFib3k4MDgiLCJhIjoiQlkzb3l0USJ9.o-SHU46rak_miT5dRXIhaw'
  }).addTo(map3);
  // L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  //     attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  // }).addTo(map);

  // var areaSelect = L.areaSelect({width:200, height:200});
  // areaSelect.on("change", function() {
  //     var bounds = this.getBounds();
  //     $("#result .sw").val(bounds.getSouthWest().lat + ", " + bounds.getSouthWest().lng);
  //     $("#result .ne").val(bounds.getNorthEast().lat + ", " + bounds.getNorthEast().lng);
  // });
  // areaSelect.addTo(map);

  var greenIcon = L.icon({
      iconUrl: '../resources/leaf_green.png',
      shadowUrl: '../resources/leaf_shadow.png',

      iconSize:     [38, 95], // size of the icon
      shadowSize:   [50, 64], // size of the shadow
      iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
      shadowAnchor: [4, 62],  // the same for the shadow
      popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
  });

  L.marker([22.0833, -159.5000], {icon: greenIcon}).addTo(map_all, map).bindPopup("Kauai");
  L.marker([-17.5333, -149.8333], {icon: greenIcon}).addTo(map_all).bindPopup("Moorea");
  L.marker([48.5353, -123.0311], {icon: greenIcon}).addTo(map_all).bindPopup("Friday Harbor");
  L.marker([-0.6667, -90.5500], {icon: greenIcon}).addTo(map_all).bindPopup("Galapagos Islands");
});