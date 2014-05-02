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
				ejs.TermsAggregation('geohashes')
					.script("doc['Locations'].value.geohash")
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

//Modified from:
//http://jsfiddle.net/sowelie/3JbNY/
var CustomMarker = L.Marker.extend({
	bindPopup: function(htmlContent, options) {
		if (options && options.showOnMouseOver) {
			//call the super method
			L.Marker.prototype.bindPopup.apply(this, [htmlContent, options]);
			
			//Default behavior shows popup on click
			//Turn that off so that we only popup on hover.
			this.off("click", this.openPopup, this);
			
			// bind to mouse over
			this.on("mouseover", function(e) {
				
				// get the element that the mouse hovered onto
				var target = e.originalEvent.fromElement || e.originalEvent.relatedTarget;
				var parent = this._getParent(target, "leaflet-popup");

				// check to see if the element is a popup, and if it is this marker's popup
				if (parent == this._popup._container)
					return true;
				
				// show the popup
				this.openPopup();
				
			}, this);
			
			// and mouse out
			this.on("mouseout", function(e) {
				
				// get the element that the mouse hovered onto
				var target = e.originalEvent.toElement || e.originalEvent.relatedTarget;
				
				// check to see if the element is a popup
				if (this._getParent(target, "leaflet-popup")) {

					L.DomEvent.on(this._popup._container, "mouseout", this._popupMouseOut, this);
					return true;

				}
				
				// hide the popup
				this.closePopup();
				
			}, this);
		}
	},
	
	_popupMouseOut: function(e) {
	    
		// detach the event
		L.DomEvent.off(this._popup, "mouseout", this._popupMouseOut, this);
 
		// get the element that the mouse hovered onto
		var target = e.toElement || e.relatedTarget;
		
		// check to see if the element is a popup
		if (this._getParent(target, "leaflet-popup"))
			return true;
		
		// check to see if the marker was hovered back onto
		if (target == this._icon)
			return true;
		
		// hide the popup
		this.closePopup();
		
	},
	
	_getParent: function(element, className) {
		
		var parent = element.parentNode;
		
		while (parent != null) {
			
			if (parent.className && L.DomUtil.hasClass(parent, className))
				return parent;
			
			parent = parent.parentNode;
			
		}
		
		return false;
		
	}
 
});


function addToMap (data) {
	markers = L.featureGroup();
	
	var aggIcon = L.divIcon({className: 'agg-icon'});
	var aggs = data.aggregations['Locations-Grid'].buckets;
	

	mapBounds = [
		[data.aggregations['Locations-Bounds']['min_lat'].value, data.aggregations['Locations-Bounds']['min_lon'].value],
		[data.aggregations['Locations-Bounds']['max_lat'].value, data.aggregations['Locations-Bounds']['max_lon'].value]
	]
	
	for (var i=0;i<aggs.length;i++) {
		
		var html = "";
		for (var j=0;j<aggs[i].species.buckets.length;j++){
			html += aggs[i].species.buckets[j].key + " (" + aggs[i].species.buckets[j]['doc_count']  + ")<br>"
		}
		
		var totalDocs = 0;
		var totalLat = 0;
		var totalLon =0
		var totalLocations = 0;

		//Here we loop through and get locations that are inside the geohash 
		//we are looking for. (since documents have many locations and only some
		//of them are inside the current geohash, this is required)
		//At the moment this is quite hard to do serverside
		for(var j =0; j < aggs[i]['geohashes']['buckets'].length; j++ ) {
			var geohashKey = aggs[i]['geohashes']['buckets'][j]['key'];
			//if the parent aggregation key is at the start of the location geohash
			if (geohashKey.indexOf(aggs[i]['key']) == 0) {
				var geohashLatLon = decodeGeoHash(geohashKey);
				var geohashLocations = aggs[i]['geohashes']['buckets'][j]['doc_count'];
				totalLocations += geohashLocations;
				totalLat += (geohashLatLon['latitude'][2] * geohashLocations); //['lat'][2] is the middle of the geohash
				totalLon +=	(geohashLatLon['longitude'][2] * geohashLocations); //['lon'][2] is the middle of the geohash
			}  
		}
		
		iconSize = aggs[i]['doc_count'] / 15 + 10;
		if(iconSize > 35) iconSize = 35;
		if (iconSize > 10 && iconSize < 11 ) {
			iconSize = 14;
			var sizeClass = 'agg-icon-1' 
		} else if (iconSize >= 11 && iconSize < 20 ) { 
			iconSize = 20;
			var sizeClass = 'agg-icon-2' 
		} else if (iconSize >= 20 && iconSize < 25 ) { 
			iconSize = 24;
			var sizeClass = 'agg-icon-3' 
		} else if (iconSize >= 25 && iconSize < 30 ) { 
			iconSize = 29;
			var sizeClass = 'agg-icon-4' 
		} else if (iconSize >= 30 && iconSize <= 35 ) { 
			iconSize = 35;
			var sizeClass = 'agg-icon-5' 
		}

		if(totalLocations) {
			var avgLat = totalLat / totalLocations;
			var avgLon = totalLon / totalLocations;
			var marker = new CustomMarker([
				avgLat,
				avgLon
			], {
				icon: L.divIcon({
					className: 'agg-icon ' + sizeClass,
					html: aggs[i]['doc_count'],
					iconSize: [iconSize, iconSize]
				})
			})
			
			marker.bindPopup(html, {showOnMouseOver: true});
			markers.addLayer(marker);
		
		} else {
			//Todo: find out why there are some key / location mismatches
			console.log('mismatch!')
		}
	}
	map.addLayer(markers);
}

// Set bounds to extent of data.
$('a[href="#results-map"]').on('shown.bs.tab', function(e){
	//confirm map zooms on invalidatesize/fitbounds otherwise markers need to be added manually
	map.invalidateSize();
	map.fitBounds(mapBounds, {padding: [50, 50]});
})

function updateMarkers() {
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
}

var markers = L.featureGroup().addTo(map);
map.on('zoomend', updateMarkers)

var dragTimer = null;
map.on('drag', function() {
	if (dragTimer === null) {
		dragTimer = setTimeout(function(){
			updateMarkers(); 
			dragTimer = null;
		}, 500);
	}
})

//}

