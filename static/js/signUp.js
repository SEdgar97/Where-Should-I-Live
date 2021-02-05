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

/*

// Creating the initial size of the svg
var svgWidth = 960;
var svgHeight = 500;

// Add a margin
var margin = {
  top: 20,
  right: 40,
  bottom: 80,
  left: 100
};
// Create the sizes for the chart
var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an svg inside the chart object
var svg = d3
  .select(".chart")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

// Creating the object that all our elements go into
var chartGroup = svg.append("g")
.attr("transform", `translate(${margin.left}, ${margin.top})`);


// Create global variables for initial values
var chosenXAxis = "xhealth_care_index";
var chosenYAxis = "ypollution_index";
var currentX = "xhealth_care_index";
var currentY = 'ypollution_index';
var axisXVal = "Healthcare Index";
var axisYVal = "Pollution Index";

// Create the initial value of the title
var chartTitle = d3.select('.chart-title').text('Healthcare Index v. Pollution Index')

// Update the y scale based upon given values, called when an axis is clicked
function yScale(cityData, chosenYAxis) {

    // Creating a scaled y axis from the values given
  var yLinearScale = d3.scaleLinear()
    .domain([d3.min(cityData, d => d[chosenYAxis]) * 0.8,
      d3.max(cityData, d => d[chosenYAxis]) * 1.2
    ])
    .range([height,0]);

  return yLinearScale;
}

// Same as the y axis but for the x
function xScale(cityData, chosenXAxis) {
  // create scales
  var xLinearScale = d3.scaleLinear()
    .domain([d3.min(ctyData, d => d[chosenXAxis]) * 0.8,
      d3.max(cityData, d => d[chosenXAxis]) * 1.2
    ])
    .range([0, width]);

  return xLinearScale;
}


// Rendering the axes based upon the given x and y axes passed
// This is intended for when a new axis is called so that the axis transition happens properly
function renderAxes(newXScale,newYScale, xAxis,yAxis) {

  var bottomAxis = d3.axisBottom(newXScale);
  var leftAxis = d3.axisLeft(newYScale)

  xAxis.transition()
    .duration(1000)
    .call(bottomAxis);

    yAxis.transition()
    .duration(1000)
    .call(leftAxis)

    // Returns both changed axes
  return xAxis,yAxis;
}

// Move the circles based upon the changed axis values
function renderCircles(circlesGroup, newXScale, newYScale, chosenYAxis, chosenXAxis) {

    // This function for some reason can only accomdate one of these functions at one time. So an if statement separates them
    // depending upon if the x or y axis is changed.
    // This one updates the X values for the circles and their text
    if (chosenXAxis != currentX){

    circlesGroup.selectAll('circle').transition()
    .duration(1000)
    .attr("cx", d => newXScale(d[chosenXAxis]));
    circlesGroup.selectAll('text').transition()
    .duration(1000)
    .attr("x", d => newXScale(d[chosenXAxis])-6);

    currentX = chosenXAxis;
    }

    // Updates the circle and text with the proper y values
    if (chosenYAxis != currentY) {
    circlesGroup.selectAll('circle').transition()
    .duration(1000)
    .attr("cy", d => newYScale(d[chosenYAxis]));
    circlesGroup.selectAll('text').transition()
    .duration(1000)
    .attr("y", d => newYScale(d[chosenYAxis])-6);

    currentY = chosenYAxis;
    }


  return circlesGroup;
}

// This changes the tool tip based upon the axes selected
function updateToolTip(chosenXAxis,chosenYAxis, circlesGroup) {

  var xlabel;
  var ylabel;

  if (chosenXAxis === "xhealth_care_index") {
    xlabel = "HC index: ";
  }
  else if (chosenXAxis === "xpollution_index") {
  xlabel = "Pollution index: ";

  }
  else if(chosenXAxis === "xcrime_index") {
  xlabel = "Crime index: "
  }
  else {
    xlabel = "Restaurant Price index: ";
  }


  if (chosenYAxis === "yhealth_care_index") {
    ylabel = "HC index: ";
  }
  else if (chosenYAxis === "ypollution_index") {
  ylabel = "Pollution index: ";

  }
  else if(chosenYAxis === "ycrime_index") {
  ylabel = "Crime index: "
  }
  else {
    ylabel = "Restaurant Price index: ";
  }


    // This creates the tooltip structure and hands it over to css for the formatting
  var toolTip = d3.tip()
    .attr("class", "tooltip")
    .offset([80, -60])
    .html(function(d) {
      return (`<br>${xlabel} ${d[chosenXAxis]}<br> ${ylabel} ${d[chosenYAxis]}`);
    });
// Actually add the tooltip
  circlesGroup.call(toolTip);

// Add the events listener that renders and hides the tooltip object
  circlesGroup.on("mouseover", function(data) {
    toolTip.show(data,this);
  })
    .on("mouseout", function(data, index) {
      toolTip.hide(data,this);
    });

  return circlesGroup;
}


// Read through the data and make some of the columns numeric
d3.csv("assets/data/data.csv").then(function(cityData) {
//  censusData.forEach(function(data) {
//    data.obesity = +data.obesity;
//    data.healthcare = +data.healthcare;
//    data.income = +data.income;
//    data.age = +data.age
//  });

  // Create the linear scale for each axis
  var xLinearScale = xScale(response, chosenXAxis);
  var yLinearScale = yScale(response, chosenYAxis);


  // Create the axis objects
  var bottomAxis = d3.axisBottom(xLinearScale);
  var leftAxis = d3.axisLeft(yLinearScale);

  // Add the x axis
  var xAxis = chartGroup.append("g")
    .classed("x-axis", true)
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);


  // Add the y axis
  var yAxis = chartGroup.append("g")
  .classed('y-axis',true)
  .attr("transform", `translate(0,0)`)
   .call(leftAxis);

  // Create the circle objects and the text objects
  // Circle objects don't render text in d3 so we add text objects and place them on top of the circles
  var circlesGroup = chartGroup.selectAll("circle")
    .data(response)
    .enter()
    .append('g')

    circlesGroup.append("circle")
    .attr("cx", d => xLinearScale(d[chosenXAxis]))
    .attr("cy", d => yLinearScale(d[chosenYAxis]))
    .attr("r", 15)
    .attr("fill", "green")
    .attr("opacity", ".5")

//    circlesGroup.append('text').text(d=>d.abbr)
//    .attr('x',d => xLinearScale(d[chosenXAxis]) -6)
//    .attr('y',d => yLinearScale(d[chosenYAxis])+4)
//    .attr('stroke','white')
//    .attr("font-size", "8px");


  // Create the group for all 4 different axes
  var labelsGroup = chartGroup.append("g")
    .attr("transform", `translate(${width / 2}, ${height + 20})`);

    // Create all 4 of the label objects
    // These are all created in the same way because they're called the same way as one another
  var xHCLabel = labelsGroup.append("text")
    .attr("x", 0)
    .attr("y", 20)
    .attr("value", "xhealth_care_index") // value to grab for event listener
    .classed("active", true)
    .text("Healthcare Index");

  var xCrimeLabel = labelsGroup.append("text")
    .attr("x", 0)
    .attr("y", 40)
    .attr("value", "xcrime_index") // value to grab for event listener
    .classed("inactive", true)
    .text("Crime Index");

    var xPollutionLabel = labelsGroup.append("text")
    .attr("x", 0)
    .attr("y", 60)
    .attr("value", "xpollution_index") // value to grab for event listener
    .classed("inactive", true)
    .text("Pollution Index");

    var xRestaurantLabel = labelsGroup.append("text")
    .attr("x", 0)
    .attr("y", 80)
    .attr("value", "xrestaurant_price_index") // value to grab for event listener
    .classed("inactive", true)
    .text("Restaurant Index");




    var yHCLabel = labelsGroup.append("text")
    .attr("transform", "rotate(90)")
    .attr("x", 0 - (height / 2) -50)
    .attr("y", width/2 + 40)
    .attr("value", "yhealth_care_index") // value to grab for event listener
    .classed("active", true)
    .text("Healthcare Index");

    var yCrimeLabel = labelsGroup.append("text")
    .attr("transform", "rotate(90)")
    .attr("x", 0 - (height / 2) -50)
    .attr("y", width/2 + 60)
    .attr("value", "ycrime_index") // value to grab for event listener
    .classed("inactive", true)
    .text("Crime Index");

    var yPollutionLabel = labelsGroup.append("text")
    .attr("transform", "rotate(90)")
    .attr("x", 0 - (height / 2) -50)
    .attr("y", width/2 + 80)
    .attr("value", "ypollution_index") // value to grab for event listener
    .classed("inactive", true)
    .text("Pollution Index");

    var yRestaurantLabel = labelsGroup.append("text")
    .attr("transform", "rotate(90)")
    .attr("x", 0 - (height / 2) -50)
    .attr("y", width/2 + 100)
    .attr("value", "yrestaurant_price_index") // value to grab for event listener
    .classed("inactive", true)
    .text("Restaurant Index");


  // Add the tooltips
  var circlesGroup = updateToolTip(chosenXAxis, chosenYAxis, circlesGroup);

  // Event listener for all axis clicks
  labelsGroup.selectAll("text")
    .on("click", function() {
      // Get value of selection
      var value = d3.select(this).attr("value");

    // Grab the current value and store it in either the changed X or Y
      if (value == 'xhealth_care_index') {
        chosenXAxis = 'xhealth_care_index';
        }

        else if (value == 'xcrime_index') {
        chosenXAxis = 'xcrime_index';
        }

        else if (value == 'xpollution_index') {
        chosenXAxis = 'xpollution_index';
        }

        else {
        chosenXAxis = 'xrestaurant_price_index'
        }




        if (value == 'yhealth_care_index') {
        chosenYAxis = 'yhealth_care_index';
        }

        else if (value == 'ycrime_index') {
        chosenYAxis = 'ycrime_index';
        }

        else if (value == 'ypollution_index') {
        chosenYAxis = 'ypollution_index';
        }

        else {
        chosenXAxis = 'yrestaurant_price_index'
        }

        // Create the X and Y scale based upon the selected axes
        xLinearScale = xScale(response, chosenXAxis);
        yLinearScale = yScale(response,chosenYAxis);

        // Render the axis transitions
        xAxis,yAxis = renderAxes(xLinearScale,yLinearScale, xAxis,yAxis);


        // Update the circles with their new positions
        circlesGroup = renderCircles(circlesGroup, xLinearScale, yLinearScale, chosenYAxis, chosenXAxis);

        // Update tooltips with new info
        circlesGroup = updateToolTip(chosenXAxis, chosenYAxis, circlesGroup);

        // Changes the appearance of the axis labels
        if (chosenXAxis === "xhealth_care_index") {
            axisXVal = "Healthcare Index";

          xHCLabel
            .classed("active", true)
            .classed("inactive", false);
          xCrimeLabel
            .classed("active", false)
            .classed("inactive", true);
          xPollutionLabel
            .classed("active", false)
            .classed("inactive", true);
          xRestaurantLabel
            .classed("active", false)
            .classed("inactive", true);

        }
        else if (chosenXAxis === "xcrime_index"){
            axisXVal = "Crime Index";

            xHCLabel
                .classed("active", false)
                .classed("inactive", true);
            xCrimeLabel
                .classed("active", true)
                .classed("inactive", false);
          xPollutionLabel
                .classed("active", false)
                .classed("inactive", true);
          xRestaurantLabel
                .classed("active", false)
                .classed("inactive", true);

        }
        else if (chosenXAxis === "xpollution_index"){
            axisXVal = "Pollution Index";
            xHCLabel
                .classed("active", false)
                .classed("inactive", true);
            xCrimeLabel
                .classed("active", false)
                .classed("inactive", true);
          xPollutionLabel
                .classed("active", true)
                .classed("inactive", false);
          xRestaurantLabel
                .classed("active", false)
                .classed("inactive", true);
        }

        else {
            axisXVal = "Restaurant Index";
          xHCLabel
                .classed("active", false)
                .classed("inactive", true);
            xCrimeLabel
                .classed("active", false)
                .classed("inactive", true);
          xPollutionLabel
                .classed("active", false)
                .classed("inactive", true);
          xRestaurantLabel
                .classed("active", true)
                .classed("inactive", false);
        }







        if (chosenYAxis === "yhealth_care_index") {
            axisYVal = "Healthcare Index";

          yHCLabel
            .classed("active", true)
            .classed("inactive", false);
          yCrimeLabel
            .classed("active", false)
            .classed("inactive", true);
          yPollutionLabel
            .classed("active", false)
            .classed("inactive", true);
          yRestaurantLabel
            .classed("active", false)
            .classed("inactive", true);

        }
        else if (chosenYAxis === "ycrime_index"){
            axisYVal = "Crime Index";

            yHCLabel
                .classed("active", false)
                .classed("inactive", true);
            yCrimeLabel
                .classed("active", true)
                .classed("inactive", false);
          yPollutionLabel
                .classed("active", false)
                .classed("inactive", true);
          yRestaurantLabel
                .classed("active", false)
                .classed("inactive", true);

        }
        else if (chosenYAxis === "ypollution_index"){
            axisYVal = "Pollution Index";
            yHCLabel
                .classed("active", false)
                .classed("inactive", true);
            yCrimeLabel
                .classed("active", false)
                .classed("inactive", true);
          yPollutionLabel
                .classed("active", true)
                .classed("inactive", false);
          yRestaurantLabel
                .classed("active", false)
                .classed("inactive", true);
        }

        else {
            axisYVal = "Restaurant Index";
          yHCLabel
                .classed("active", false)
                .classed("inactive", true);
            yCrimeLabel
                .classed("active", false)
                .classed("inactive", true);
          yPollutionLabel
                .classed("active", false)
                .classed("inactive", true);
          yRestaurantLabel
                .classed("active", true)
                .classed("inactive", false);
        }

        // Change the chart title if a new axis is selected
        chartTitle = d3.select('.chart-title').text(`${axisXVal} v. ${axisYVal}`)

    });

})

*/