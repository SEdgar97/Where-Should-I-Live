var myMap = L.map("map", {
  center: [37.09, -95.71],
  zoom: 5
});

// Add a tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);






$(function(){
	$('button').click(function(){
		var user = $('#inputUsername').val();
		var pass = $('#inputPassword').val();

//		$.ajax({
//			url: '/signUpUser',
//			data: $('form').serialize(),
//			type: 'POST',
//			success: function(response){
//				console.log(response);
//			},
//			error: function(error){
//				console.log(error);
//			}
//		});

		$.ajax({
			url: '/get_data',
			data: "hello",
			type: 'POST',
			success: function(response){
				response = JSON.parse(response)
				var vals = Object.keys(response.city)

				for(var i = 0; i<vals.length; i++){
				    var key = vals[i]
				    console.log(response.city[key])
				    console.log("Latitude: " + response.latitude[key])
				    console.log("Longitude: " + response.longitude[key])
				    L.marker([response.latitude[key],response.longitude[key]])
				    .bindPopup("<h3>" + response.city[key] + "</h3> <hr> <h5> (" + response.latitude[key] + ", " + response.longitude[key] + ")")
				    .addTo(myMap)

				};

				for (var i = 0; i < cities.length; i++) {
                    var city = cities[i];
                    L.marker(city.location)
                    .bindPopup("<h1>" + city.name + "</h1> <hr> <h3>Population " + city.population + "</h3>")
                    .addTo(myMap);
                }




			},
			error: function(error){
				console.log(error);
			}
		});

	});
});