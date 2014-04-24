var map = L.map('map');
					
// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Set bounds to extent of data.
$('a[href="#results-map"]').on('shown.bs.tab', function(e){
	map.invalidateSize();
	map.fitBounds([
		[-20.879343,-75.805664], //Southwest
		[-56.944974,-52.866211] //Northeast
	]);
	
})


