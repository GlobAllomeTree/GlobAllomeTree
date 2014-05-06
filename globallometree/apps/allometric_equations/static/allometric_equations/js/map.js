window.app.mapController = function() {
	//Only use safe Javascript
	"use strict";
	
	var ES_THROTTLE_RATE = 500; //In ms
	var el;
	var map;
	var param;
	var markers;
	var dragTimer;
	var initialized = false;
	
	
	// These are the default map bounds for the world
	// coordinates will fit the whole globe when accounting for the padding of 50
	var mapBounds = [
		[-40,-130], //Southwest
		[40,130] //Northeast
	];
	
	
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
		12 : 9,
		13 : 9,
		14 : 9,
		15 : 9 //4.773m/pixel : 38.2m x 19m
	};
	
	//Elastic Search queries are filtered by the bounding box of the map view.  To facilitate smoother
	//panning by loading in advance points slightly outside of the map view we can apply a buffer to
	//the elastic search request.  This is done by adding padding to the coordinates passed to ES.
	//Since we are using Latitude/Longitude, the length of a decimal degree will vary based on latitude
	//All values here are calculated at the equator.  To calculate the decimal degree buffer by number of
	//pixels (we are using 300 here) multiply the resolution of a pixel at the current zoom level (in meters/pixel)
	//by the number of pixels you wish to buffer.  Then divide by the size of a decimal degree at the equator, 111,320m.
	var zoomExtentBuffer = {
		0 : 0,
		1 : 0, 
		2 : 3.512666188, //Minimum zoom for our map, shows almost entire world so 10 pixel buffer
		3 : 8.781440891, //Still shows most of the world so 50 pixel buffer
		4 : 26.05192239, //This and all subsequent zoom levels have 300 pixel buffer (half the map width)
		5 : 13.17283507,
		6 : 6.586417535,
		7 : 3.293208768,
		8 : 1.64390945,
		9 : 0.821954725,
		10 : 0.409629896,
		11 : 0.204814948,
		12 : 0.102407474,
		13 : 0.0512037370,
		14 : 0.025601868,
		15 : 0.013474668
	}
	


	var initOrShowMap = function (params) {

		el = params['el'];

		if(initialized) {
			//confirm map zooms on invalidate size/fitbounds otherwise markers need to be added manually
			return
		}

		initialized = true;

		//The map object
		map = L.map(el, {
			minZoom: 2,
			maxZoom: 15,
			maxBounds : [[90, -180], [-90, 180]]
		});

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

		// add an OpenStreetMap tile layer
		L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
			attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
		}).addTo(map);

		//Leaflet requires the div to be of a defined size before generating the map
		//When leaflet is called on a hidden div, the map is created with a size of 0
		//When we show the map, we need to reset the map so it draws at the correct dimensions
		//Hiding and reshowing the map tab will reset the map to the mapBounds.  If the map
		//should be reset to the last zoom and extent the user was viewing, then we need to 
		//update the map bounds with an "onmove" event listener
		map.invalidateSize();
		map.fitBounds(mapBounds, {padding: [50, 50]});


		//Bind the popups to load when they are opened
		map.on('popupopen', function(e) {
		  var marker = e.popup._source;
		  loadSummaryToPopup(marker, e.popup);
		});

	}
	
	

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
	

	function getGeoAggregations(precision) {
		
		var aggregations = [];
		
		aggregations.push(
			ejs.GeoHashGridAggregation('Locations-Grid')
				.field('Locations')
				.precision(precision)
				.aggregation(
					ejs.TermsAggregation('geohashes')
						.script("doc['Locations'].value.geohash")
				)
		);

		aggregations.push(
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

		return aggregations;
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
			var totalDocs = 0;
			var iconSize;
			var sizeClass;
			
		
			// Here we loop through and get locations that are inside the geohash 
			// so that we can average out the matching locations and find the best
			// place to put the marker.
			// Each document has several locations, some are inside this geohash and
			// some are outside the geohash. 
			// In the loop, we look to see if the location geohash has the prefix of the 
			// bucket geohash.
			// For example if the bucket geohash is c1, we would use the the location if 
			// it's geohash begins with c1 (c1klj9, c178ds,...) 
			//
			// Additionally, we get a total doc count using the location geohashes
			// This is done because the geohash grid bucket doc count is counting total locations, not total documents
			// Taking the below result as an example it is easier to see why this is required
			// geohas_grid agg bucket: key: "dn" - doc_count: 538
			// geohashes terms agg: 
			// buckets: 
			// doc_count: 112
			// key: "dnhjv2bwdk4u"
			//
			// doc_count: 100
			// key: "djugne6qsphb"
			//
			// doc_count: 95
			// key: "djjzj71gg3mp"
			//
			// u'doc_count': 3,
			// u'key': u'dhqrfbh'}
			// 
			// While the geohash grid count is 538, that is the count of all locations 
			// in all matched documents even if those locations fall outside the parent buckets geohash
			// What we really want is just the count of all matched documents 
			// So in the case here, we want key: "dnhjv2bwdk4u" with doc_count: 112

			for(j=0; j < aggs[i].geohashes.buckets.length; j++ ) {
				var geohashKey = aggs[i].geohashes.buckets[j].key;
				//if the parent aggregation key is at the start of the location geohash
				if (geohashKey.indexOf(aggs[i].key) === 0) {
					var geohashLatLon = decodeGeoHash(geohashKey);
					var geohashDocs = aggs[i].geohashes.buckets[j]['doc_count'];
					
					//Since these documents do belong to the geohash we are interested in, 
					//we add the documents to our total count
					totalDocs += geohashDocs;
					totalLat += (geohashLatLon.latitude[2] * geohashDocs); //['lat'][2] is the middle of the geohash
					totalLon +=	(geohashLatLon.longitude[2] * geohashDocs); //['lon'][2] is the middle of the geohash
				}  

				var aggDocCount = aggs[i]['doc_count'];
				var currentAgg = aggs[i];
				// if (geohashDocs < aggDocCount) {
				// 	debugger;
				// }
			}
			
		
			//Set the marker icon size based on the number of aggregations
			iconSize = totalDocs / 15 + 10;
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


			//In some cases (very few) the totalDocs will be empty 
			//since the only docs in the aggregation are actually in another geohash
			//It does not seem to be an issue though since there are other aggregations
			//that correctly include and display these docs - most likely it is a bug
			//in the new aggregatio
			if(totalDocs) {

				//Actual center of records
				var avgLat = totalLat / totalDocs;
				var avgLon = totalLon / totalDocs;

				//Center of aggregation geohash
				//Decode the geohash key for the bucket
				//var aggLatLon = decodeGeoHash(aggs[i].key);
				//var aggLat = aggLatLon.latitude[2]; //center of bucket
				//var aggLon = aggLatLon.longitude[2]; //center of bucket 

				var marker = new CustomMarker([
					avgLat,
					avgLon
				], {
					icon: L.divIcon({
						className: 'agg-icon ' + sizeClass,
						html: totalDocs,
						iconSize: [iconSize, iconSize]
					})
				});
				
				marker.bindPopup('<p>loading...</p>', {showOnMouseOver: true});
				//We tag the geohash onto the marker for later use in the lookup
				marker.geohash = aggs[i].key;
				marker.geohashContentLoaded = false;
				marker.docCount = totalDocs;
				markers.addLayer(marker);
			}
		}
		map.addLayer(markers);
	}
	
	/**
	* Generates an elastic search query and retrieves the results from the server
	* drawing them on the map.  Query is limited to the extent of the map view (plus buffer)
	* to limit the number of features returned from the server and drawn on the map.  This
	* is particularly important when zoomed in as the number of features could be prohibitively
	* large
	*/
	function updateMarkers() {
		var bounds = map.getBounds();
		var zoom = map.getZoom();
		var maxx = bounds._northEast.lng + zoomExtentBuffer[zoom];
		var maxy = bounds._northEast.lat + zoomExtentBuffer[zoom];
		var minx = bounds._southWest.lng - zoomExtentBuffer[zoom];
		var miny = bounds._southWest.lat - zoomExtentBuffer[zoom];
		var precision = geoGridPrecision[map.getZoom()];
		var boundingBox = [minx, miny, maxx, maxy];
		
		var query = window.app.searchManager.getQuery({
			aggregations : getGeoAggregations(precision),
			boundingBox : boundingBox
		});

		window.app.searchManager.search({
			query : query,
			success: function (e) {
				map.removeLayer(markers);
				addToMap(e);
			}
		});
	}

	var getBucketsAsList = function(buckets, separator) {
		var items = [];
		//Generate text for html hover events
		for (j=0;j<buckets.length;j++){
			items.push(buckets[j].key + " (" + buckets[j]['doc_count']  + ")");
		}
		return items.join(separator);
	}

	//When someone opens a popup, we get the summary
	var loadSummaryToPopup = function(marker, popup) {
		//Prevent double loading
		if(marker.geohashContentLoaded) return;
		marker.geohashContentLoaded = true;
		//Get our geohash bounds from the marker where we monkepathed them on
		var geohashBounds =  decodeGeoHash(marker.geohash);

		var minx = geohashBounds['longitude'][0];
		var maxx = geohashBounds['longitude'][1];
		var miny = geohashBounds['latitude'][0];
		var maxy = geohashBounds['latitude'][1];
		var boundingBox = [minx, miny, maxx, maxy];
	
		var query = window.app.searchManager.getQuery({
			aggregations : [
				ejs.TermsAggregation('Species').field('Genus_Species'),
				ejs.TermsAggregation('Biome_FAO').field('Biome_FAO'),
				ejs.TermsAggregation('Reference').field('Reference'),		
			],
			boundingBox : boundingBox
		});

		window.app.searchManager.search({
			query : query,
			success: function (data) {
				var html = "<br>";
				//marker.docCount was also monkey patched
				html += '<h4>Equations: ' + marker.docCount + '</h4>';

				if(data.aggregations['Species'].buckets.length) {
					html += '<h5>Species Represented</h5>'  
					html += '<p style="margin-top:0px;">' + getBucketsAsList(data.aggregations['Species'].buckets, ', ') + '</p>';
				}
				
				if(data.aggregations['Biome_FAO'].buckets.length){
					html += '<h5>FAO Biomes</h5>'  
					html += '<p style="margin-top:0px;">' + getBucketsAsList(data.aggregations['Biome_FAO'].buckets, ', ') + '</p>';
				}
				
				html += '<h5>Summary Area</h5>'
				html += '<p style="margin-top:0px;"> Latitude: ' + geohashBounds['latitude'][0] + ' to ' + geohashBounds['latitude'][1] + '<br>';
				html += 'Longitude: ' + geohashBounds['longitude'][0] + ' to ' + geohashBounds['longitude'][1] + '</p>';

				popup.setContent(html);
			}
		});
	}


	//Public objects
	return {
		initOrShowMap : initOrShowMap,
		map : map
	}
}();