function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}

function generateESQuery(q,termFilters,boundingBox,precision) {
	var query = ejs.Request();
	var filters;
	
	if (boundingBox) {
		
		if (boundingBox[0] < -179.99999) {
			boundingBox[0] = -179.99999;
		}
		if (boundingBox[1] < -89.99999) {
			boundingBox[1] = -89.99999;
		}
		if (boundingBox[2] > 179.99999) {
			boundingBox[2] = 179.99999;
		}
		if (boundingBox[3] > 89.99999) {
			boundingBox[3] = 89.99999;
		}
		
	}
		
	if (termFilters && boundingBox) {
		var geoFilter = ejs.GeoBboxFilter('Locations')
			.topLeft(ejs.GeoPoint([boundingBox[3], boundingBox[0]]))
			.bottomRight(ejs.GeoPoint([boundingBox[1], boundingBox[2]]))
		filters = $.extend([], termFilters, geoFilter);
	} else {
		filters = termFilters;
	}
	

	if (q) {
		query.query(
			ejs.FilteredQuery(
				ejs.QueryStringQuery({
					query : q, 
					fields: ["Keywords"],
					defaultOperator : "AND"})
			)
		)	
	} else {
		query.query(
			ejs.FilteredQuery(
				ejs.MatchAllQuery(),
				ejs.AndFilter(filters)
				
			)
		)
	}

	query.aggregation(
		ejs.GeoHashGridAggregation('Locations-Grid')
			.field('Locations')
			.precision(precision)
			.aggregation(
				ejs.TermsAggregation('species')
					.field('Species')
			)
			.aggregation(
				ejs.AvgAggregation('avg_lat')
					.script("doc['Locations'].value.lat")
			)
			.aggregation(
				ejs.AvgAggregation('avg_lon')
					.script("doc['Locations'].value.lon")
			)
	)
	.aggregation(
		ejs.FilterAggregation('Locations-Bounds')
			.filter(
				ejs.ExistsFilter('Locations')
			)
			.aggregation(
				ejs.MinAggregation('min_lat')
					.script("doc['Locations'].value.lat")
			)
			.aggregation(
				ejs.MaxAggregation('max_lat')
					.script("doc['Locations'].value.lat")
			)
			.aggregation(
				ejs.MinAggregation('min_lon')
					.script("doc['Locations'].value.lon")
			)
			.aggregation(
				ejs.MaxAggregation('max_lon')
					.script("doc['Locations'].value.lon")
			)
	);
	return query;
}

var mapBounds = [
	// These coordinates will fit the whole globe when accounting for the padding of 50
	[-40,-130], //Southwest
	[40,130] //Northeast
];

var urlParams = {
	//Keyword
	q : 'query',
	//Identification
	Ecosystem : 'term',
	Population : 'term',
	//Taxonomy
	Genus : 'term',
	Species : 'term',
	//Location
	Country : 'term',
	Biome_HOLDRIDGE : 'term',
	Biome_UDVARDY : 'term',
	Biome_FAO : 'term',
	Biome_WWF : 'term',
	Division_BAILEY : 'term',
	//Components
	B : 'term',
	Bd : 'term',
	Bg : 'term',
	Bt : 'term',
	L : 'term',
	Rb : 'term',
	Rf : 'term',
	Rm : 'term',
	S : 'term',
	T : 'term',
	F : 'term',
	//Input/Output
	U : 'term',
	V : 'term',
	W : 'term',
	X : 'term',
	Z : 'term',
	Unit_U : 'term',
	Unit_V : 'term',
	Unit_W : 'term',
	Unit_X : 'term',
	Unit_Y : 'term',
	Unit_Z : 'term',
	Min_X__gte : 'term',
	Max_X__gte : 'term',
	Min_Z__gte : 'term',
	Max_Z__gte : 'term',
	Output : 'term',
	Min_X__lte : 'term',
	Max_X__lte : 'term',
	Min_Z__lte : 'term',
	Max_Z__lte : 'term',
	//Allometry
	Equation : 'term',
	//Reference
	Author : 'term',
	Reference : 'term',
	Year : 'term',
	//Pagination Properties
	order_by : 'ignore',
	page : 'ignore'
}

var geoGridPrecision = {
	/*zoom level: precision*/
	0 : 1,
	1 : 1,
	2 : 2,
	3 : 2,
	4 : 3,
	5 : 3,
	6 : 4,
	7 : 5,
	8 : 6,
	9 : 7,
	10 : 8,
	11 : 9,
	12 : 10,
	13 : 10,
	14 : 10,
	15 : 10
	
}

//if (document.getElementById('map')) {
var map = L.map('map', {
	minZoom: 2,
	maxZoom: 15,
	noWrap: true
});

// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

//Build ES Query from URL Parameters

var filters = [];
var q = getURLParameter('q');

for (param in urlParams) {
	if (urlParams.hasOwnProperty(param)) {
		if (urlParams[param] == 'term') {
			if (getURLParameter(param)) {
				filters.push(ejs.TermFilter(param, getURLParameter(param)))
			}
		}
	}
}



function addToMap (data) {
	markers = L.featureGroup();
	
	var aggIcon = L.divIcon({className: 'agg-icon'});
	var aggs = data.aggregations['Locations-Grid'].buckets;

	mapBounds = [
		[data.aggregations['Locations-Bounds']['min_lat'].value, data.aggregations['Locations-Bounds']['min_lon'].value],
		[data.aggregations['Locations-Bounds']['max_lat'].value, data.aggregations['Locations-Bounds']['max_lon'].value]
	]
	
	for (var i=0;i<aggs.length;i++) {
		var marker = L.marker([
			aggs[i]['avg_lat'].value,
			aggs[i]['avg_lon'].value
		], {
			icon: L.divIcon({
				className: 'agg-icon',
				html: aggs[i]['doc_count'],
				iconSize: [35, 35]
			})
		})
		markers.addLayer(marker);
	}
	map.addLayer(markers);
}

// Set bounds to extent of data.
$('a[href="#results-map"]').on('shown.bs.tab', function(e){
	//confirm map zooms on invalidatesize/fitbounds otherwise markers need to be added manually
	map.invalidateSize();
	map.fitBounds(mapBounds, {padding: [50, 50]});
})

var markers = L.featureGroup().addTo(map);
map.on('zoomend', function() {
	var bounds = map.getBounds();
	var maxx = bounds._northEast.lng;
	var maxy = bounds._northEast.lat;
	var minx = bounds._southWest.lng;
	var miny = bounds._southWest.lat;
	var precision = geoGridPrecision[map.getZoom()];
	var query = generateESQuery(q, filters, [minx, miny, maxx, maxy], precision);
	
	$.ajax({
		type: "POST",
		url: 'http://localhost:9200/globallometree/allometricequation/_search',
		data: JSON.stringify(query.toJSON()),
		success: function (e) {
			map.removeLayer(markers)
			addToMap(e);
		}
})

})

//}

