function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
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

//if (document.getElementById('map')) {
var map = L.map('map');

// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

//Build ES Query from URL Parameters

var andFilter = [];
/*ejs.GeoBboxFilter('Locations')
				.topLeft(ejs.GeoPoint([-20.879343,-75.805664]))
				.bottomRight(ejs.GeoPoint([-56.944974,-52.866211])),*/

for (param in urlParams) {
	if (urlParams.hasOwnProperty(param)) {
		if (urlParams[param] == 'term') {
			if (getURLParameter(param)) {
				andFilter.push(ejs.TermFilter(param, getURLParameter(param)))
			}
		}
	}
}

var query = ejs.Request();

if (getURLParameter('q')) {
	query.query(
		ejs.FilteredQuery(
			ejs.QueryStringQuery({"query" : getURLParameter('q'),"fields": ["Keywords"],"defaultOperator" : "AND"})
		)
	)	
} else {
	query.query(
		ejs.FilteredQuery(
			queryString = ejs.MatchAllQuery(),
			ejs.AndFilter(andFilter)
		)
	)
}

query.aggregation(
	ejs.GeoHashGridAggregation('Locations-Grid')
		.field('Locations')
		.precision(2)
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
)
.toJSON()

$.ajax({
	type: "POST",
	url: 'http://localhost:9200/globallometree/allometricequation/_search',
	data: JSON.stringify(query),
	success: addToMap
})

function addToMap (data) {
	var aggIcon = L.divIcon({className: 'agg-icon'});
	var aggs = data.aggregations['Locations-Grid'].buckets;
	
	mapBounds = [
		[data.aggregations['Locations-Bounds']['min_lat'].value, data.aggregations['Locations-Bounds']['min_lon'].value],
		[data.aggregations['Locations-Bounds']['max_lat'].value, data.aggregations['Locations-Bounds']['max_lon'].value]
	]
	
	for (var i=0;i<aggs.length;i++) {
		L.marker([
			aggs[i]['avg_lat'].value,
			aggs[i]['avg_lon'].value
		], {
			icon: L.divIcon({
				className: 'agg-icon',
				html: aggs[i]['doc_count'],
				iconSize: [35, 35]
			})
		}).addTo(map);
	}
}

// Set bounds to extent of data.
$('a[href="#results-map"]').on('shown.bs.tab', function(e){
	map.invalidateSize();
	map.fitBounds(mapBounds, {padding: [50, 50]});
	
})
//}

