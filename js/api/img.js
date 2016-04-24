function search_img(query, api_dfd, imgResult) {
  $.ajax({
    
    type: "POST",
    dataType: 'jsonp',
    
    url: 'https://www.googleapis.com/customsearch/v1?q='+query+'&key=AIzaSyB9GKaKX2TRnMH8M28bVD8BfG-rR7H7RJs&cx=006284769470110551168:rbgx9geslba',
  }).done(function(data) {
    // check if there are results
    if (data.length != 0) {
      console.log(data);
      //console.log(data.items[0].pagemap.cse_image[0].src); // this is the image
      imgResult['img'] = data.items[0].pagemap.cse_image[0].src;
    } else {
      imgResult['img'] = null;
    }

    // notify search complete
    api_dfd.resolve();
   
  });
}