(function() {
	//Only use safe Javascript
	"use strict";
	
	//Prevents older browsers from breaking if a console.log() function is left in the code.
	if(!window.console){ window.console = {log: function(){} }; } 
	
	var filters = [];
	var q = getURLParameter('q');
	var param;
	var markers;
	var dragTimer;
	var ES_THROTTLE_RATE = 500; //In ms
	
	// These are the default map bounds for the world
	// coordinates will fit the whole globe when accounting for the padding of 50
	var mapBounds = [
		[-40,-130], //Southwest
		[40,130] //Northeast
	];
	
	//List of all possible GET parameters and the type of value.  May be useful for other
	//functions other than generating term filters
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
	};
	
	//Lookup object for determining the Elastic Search GeoHash precision to use
	//at each map zoom level
	//Zoom level references can be found at http://wiki.openstreetmap.org/wiki/Zoom_levels
	//Geohash precision levels can be found at http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-aggregations-bucket-geohashgrid-aggregation.html
	var geoGridPrecision = {
		// zoom level : precision
		0 : 1, //156,412m/pixel : 5,009.4km x 4,992.6km
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
		11 : 8,
		12 : 8,
		13 : 8,
		14 : 8,
		15 : 8 //4.773m/pixel : 38.2m x 19m
	};
	
	//The map object
	var map = L.map('map', {
		minZoom: 2,
		maxZoom: 15,
		noWrap: true
	});
		
	//Modified from:
	//http://jsfiddle.net/sowelie/3JbNY/
	//Modifies the Leaflet Marker to have a native hover window
	//Ensures that hover continues even when moving mouse over symbol text
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
			while (parent !== null) {
				if (parent.className && L.DomUtil.hasClass(parent, className))
					return parent;
				parent = parent.parentNode;
			}
			return false;
		}
	});
	
	/**
	* Parses parameters from the URL, spliting by "?" or "&"
	* @param {string} Name of parameter
	*/
	function getURLParameter(name) {
		return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
	}

	/**
	* Generates an ElasticS earch aggregation query using the elastic.js library
	* @param {string} query to be passed to an ES String_Query.  Can be a null value
	* @param {array} An array of ejs.TermFilter objects. Can be a null value
	* @param {array} An array of coordinates to filter the results by.  In the order of [minx, miny, maxx, maxy]
	* @param {integer} A number specifiying the geoHash precision.  Values between 1-12 are acceptable
	* @return {json}
	*/
	function generateESQuery(q,termFilters,boundingBox,precision) {
		var query = ejs.Request();
		var filters;
		
		if (boundingBox) {
			//Elastic Search treats values of 180 and -180 as a width of 0 and 90, -90 as a height of 0
			//Makes sure to pass values that will actually return the required results.
			//Additionally, Leaflet will pan from world copy to world copy.  This can create values infinitly
			//far outside of allowed geographic coordinates.  This snaps requests back to the primary map
			//We can prevent leaflet from loading outside of the defined geographic coordinates for the globe
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
		
		//Builds the term filters for the ES search concatenating the term filters and bounding
		//box filters if both are set
		if (termFilters && boundingBox) {
			var geoFilter = ejs.GeoBboxFilter('Locations')
				.topLeft(ejs.GeoPoint([boundingBox[3], boundingBox[0]]))
				.bottomRight(ejs.GeoPoint([boundingBox[1], boundingBox[2]]));
			filters = $.extend([], termFilters, geoFilter);
		} else {
			filters = termFilters;
		}
		
		//Creaates a simple_string query if the q parameter is set
		//Defaults to only searching the "keywords" field using an "AND" operator
		//If the q parameter is set, term filters are ignored since ES won't accept both
		if (q) {
			query.query(
				ejs.FilteredQuery(
					ejs.QueryStringQuery({
						query : q, 
						fields: ["Keywords"],
						defaultOperator : "AND"})
				)
			);
		//Otherwise we just set the query to MatchAll and filter by term filters
		} else {
			query.query(
				ejs.FilteredQuery(
					ejs.MatchAllQuery(),
					ejs.AndFilter(filters)
					
				)
			);
		}

		//Build the aggreagations
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

	/**
	* Adds allometric aggregations to the map
	* @param {json} return object from an Elastic Search query 
	*/
	function addToMap (data) {
		markers = L.featureGroup();
		var i;
		var aggs = data.aggregations['Locations-Grid'].buckets;
		
		//Updates the map bounds object that contains all of the request points
		mapBounds = [
			[data.aggregations['Locations-Bounds']['min_lat'].value, data.aggregations['Locations-Bounds']['min_lon'].value],
			[data.aggregations['Locations-Bounds']['max_lat'].value, data.aggregations['Locations-Bounds']['max_lon'].value]
		];
		
		for (i=0;i<aggs.length;i++) {
			var html = "";
			var j;
			var totalLat = 0;
			var totalLon = 0;
			var totalLocations = 0;
			var iconSize;
			var sizeClass;
			
			//Generate text for html hover events
			for (j=0;j<aggs[i].species.buckets.length;j++){
				html += aggs[i].species.buckets[j].key + " (" + aggs[i].species.buckets[j]['doc_count']  + ")<br>";
			}
			
			//Here we loop through and get locations that are inside the geohash 
			//we are looking for. (since documents have many locations and only some
			//of them are inside the current geohash, this is required)
			//At the moment this is quite hard to do serverside
			for(j=0; j < aggs[i].geohashes.buckets.length; j++ ) {
				var geohashKey = aggs[i].geohashes.buckets[j].key;
				//if the parent aggregation key is at the start of the location geohash
				if (geohashKey.indexOf(aggs[i].key) === 0) {
					var geohashLatLon = decodeGeoHash(geohashKey);
					var geohashLocations = aggs[i].geohashes.buckets[j]['doc_count'];
					totalLocations += geohashLocations;
					totalLat += (geohashLatLon.latitude[2] * geohashLocations); //['lat'][2] is the middle of the geohash
					totalLon +=	(geohashLatLon.longitude[2] * geohashLocations); //['lon'][2] is the middle of the geohash
				}  
			}
			
			//Set the marker icon size based on the number of aggregations
			iconSize = aggs[i]['doc_count'] / 15 + 10;
			if(iconSize > 35) iconSize = 35;
			if (iconSize > 10 && iconSize < 11 ) {
				iconSize = 14;
				sizeClass = 'agg-icon-1';
			} else if (iconSize >= 11 && iconSize < 20 ) { 
				iconSize = 20;
				sizeClass = 'agg-icon-2';
			} else if (iconSize >= 20 && iconSize < 25 ) { 
				iconSize = 24;
				sizeClass = 'agg-icon-3';
			} else if (iconSize >= 25 && iconSize < 30 ) { 
				iconSize = 29;
				sizeClass = 'agg-icon-4';
			} else if (iconSize >= 30 && iconSize <= 35 ) { 
				iconSize = 35;
				sizeClass = 'agg-icon-5';
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
				});
				
				marker.bindPopup(html, {showOnMouseOver: true});
				markers.addLayer(marker);
			
			} else {
				//Todo: find out why there are some key / location mismatches
				console.log('mismatch!');
			}
		}
		map.addLayer(markers);
	}
	
	/**
	* Generates and elastic search query and retrieves the results from the server
	* drawing them on the map.  Query is limited to the extent of the map view (plus buffer)
	* to limit the number of features returned from the server and drawn on the map.  This
	* is particularly important when zoomed in as the number of features could be prohibitively
	* large
	*/
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
				map.removeLayer(markers);
				addToMap(e);
			}
		});
	}
	
	//Leaflet requires the div to be of a defined size before generating the map
	//When leaflet is called on a hidden div, the map is created with a size of 0
	//When we show the map, we need to reset the map so it draws at the correct dimensions
	//Hiding and reshowing the map tab will reset the map to the mapBounds.  If the map
	//should be reset to the last zoom and extent the user was viewing, then we need to 
	//update the map bounds with an "onmove" event listener
	$('a[href="#results-map"]').on('shown.bs.tab', function(){
		//confirm map zooms on invalidate size/fitbounds otherwise markers need to be added manually
		map.invalidateSize();
		map.fitBounds(mapBounds, {padding: [50, 50]});
	});
	
	// add an OpenStreetMap tile layer
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);

	//Build ES Query from URL Parameters
	for (param in urlParams) {
		if (urlParams.hasOwnProperty(param)) {
			if (urlParams[param] == 'term') {
				if (getURLParameter(param)) {
					filters.push(ejs.TermFilter(param, getURLParameter(param)));
				}
			}
		}
	}

	markers = L.featureGroup().addTo(map);
	map.on('zoomend', updateMarkers);

	dragTimer = null;
	map.on('drag', function() {
		if (dragTimer === null) {
			dragTimer = setTimeout(function(){
				updateMarkers(); 
				dragTimer = null;
			}, ES_THROTTLE_RATE);
		}
	});
}());