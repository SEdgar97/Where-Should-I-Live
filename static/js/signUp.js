var myMap = L.map("map", {
  center: [37.09, -95.71],
  zoom: 4
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

var crimeVal = "";
var HCVal = "";
var pollutionVal = "";
var restaurantVal = "";

var crimeFilter = d3.select("#crimeFilter");
	var HCFilter = d3.select("#HCFilter");
	var pollutionFilter = d3.select("#pollutionFilter");
	var restaurantFilter = d3.select("#restFilter");

	crimeFilter.on("change",function(){
	    crimeVal = this.value;
	    console.log(crimeVal)
	});
	HCFilter.on("change",function(){
	    HCVal = this.value;
	});
	pollutionFilter.on("change",function(){
	    pollutionVal = this.value;
	});
	restaurantFilter.on("change",function(){
	    restaurantVal = this.value;
	});

var filters = {"Crime": crimeVal,"Healthcare": HCVal,"Pollution": pollutionVal,"Restaurant": restaurantVal};

var citiesLayer = L.layerGroup();

$(function(){
	$('.submit').click(function(){
        citiesLayer.clearLayers();
        $('#dataTable tr').detach();


		$.ajax({
			url: `/get_data/crime=${crimeVal}/healthcare=${HCVal}/pollution=${pollutionVal}/restaurant=${restaurantVal}`,
			data: filters,
			type: 'POST',
			success: function(response){
				response = JSON.parse(response)
				var size=0;
                for(let k in response.latitude) {
                console.log(k)
                  size++
                }
                console.log(size)

				for(var i = 0; i<size; i++){
				console.log(response.latitude[i])
				    L.marker([response.latitude[i],response.longitude[i]])
				    .bindPopup("<h3>" + response.city[i] + "</h3> <hr> <h6> (" + response.latitude[i] + ", " + response.longitude[i] + ")</h6>" )
				    .addTo(citiesLayer)

				};
				var tbody = d3.select('#dataTable');

        if (size > 0) {
        console.log('making a table')
            for(var j = 0; j<size; j++){
                var row = tbody.append('tr');
                console.log('row')
                var cell = row.append("td");
                console.log('cell')
                cell.text(response.city[j])
                cell = row.append("td");
                cell.text(response.crime_index[j])

                cell = row.append("td");
                cell.text(response.health_care_index[j])

                cell = row.append("td");
                cell.text(response.pollution_index[j])
                cell = row.append("td");
                cell.text(response.restaurant_price_index[j])


		    };

        };
			},
			error: function(error){
				console.log(error);
			}
		});
        citiesLayer.addTo(myMap);




	});
});