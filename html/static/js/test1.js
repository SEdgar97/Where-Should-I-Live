var button =document.getElementById("button");
button.addEventListener('click',() => {add()});

function add(){
	var result=[
	{
	city_name:"Honolulu",
	restaurant_price_index:81.491,
	health_care_index:72.418,
	crime_index:43.914,
	pollution_index:36.664
	}
]
	var html="<tr><th>City</th><th>Crime Index</th><th>Health Care Index</th><th>Pollution Index</th><th>Restaurant Price Index</th></tr>";
	
	for (var element of result){
		html += "<tr>";
		for (var property in element){
			html += `<td>${element[property]}</td>`;		
		}
		html += "</tr>";
	}
	
	document.getElementById("table").innerHTML= html;
	
}