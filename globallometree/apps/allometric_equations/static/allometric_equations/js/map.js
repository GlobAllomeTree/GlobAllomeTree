window.app.mapController = function() {
	//Only use safe Javascript
	"use strict";
	
	var ES_THROTTLE_RATE = 500; //In ms
	var el;	//dom element to show the map in, used by the init function
	var map; //reference to the leaflet map
	var geohash_markers, country_markers;
	var dragTimer;
	var initialized = false;
	var initialMapBoundsFit = false;
	
	
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
		1 : 2, 
		2 : 3,
		3 : 4,
		4 : 5,
		5 : 6,
		6 : 7,
		7 : 8,
		8 : 9,
		9 : 9,
		10 : 9,
		11 : 9,
		12 : 9,
		13 : 9,
		14 : 9,
		15 : 9 //4.773m/pixel : 38.2m x 19m
	};
	


	var initOrShowMap = function (params) {

		el = params['el'];

		if(initialized) {
			//confirm map zooms on invalidate size/fitbounds otherwise geohash_markers need to be added manually
			return
		}

		initialized = true;

		//The map object
		map = L.map(el, {
			minZoom: 2,
			maxZoom: 15
		});

		country_markers = L.featureGroup().addTo(map);
		geohash_markers = L.featureGroup().addTo(map);

		
		map.on('zoomend', updateGeohashMarkers);

		dragTimer = null;
		map.on('drag', function() {
			if (dragTimer === null) {
				dragTimer = setTimeout(function(){
					updateGeohashMarkers(); 
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


		//Since the country markers don't change on zoom,
		//we add them in once at the beginning
		loadCountryMarkers();


		//Bind the popups to load when they are opened
		//We have monkey patched a few properties onto the
		//marker to be able to show a summary
		map.on('popupopen', function(e) {
		  var marker = e.popup._source;
		  if(marker.aggType == 'country') {
		  	loadCountrySummaryToPopup(marker, e.popup);
		  } else if (marker.aggType == 'geohash') {
		  	loadGeoSummaryToPopup(marker, e.popup);
		  }
		});
	}
	

	
	/**
	* Adds allometric aggregations to the map with only a country specified for location
	* @param {data} return object from an Elastic Search query 
	*/
	function addCountryMarkersToMap(data) {
		var country_aggs = data.aggregations['country_3166_3'].buckets;

		country_markers = L.featureGroup();


		for (var i=0;i<country_aggs.length;i++) {
			var key = country_aggs[i]['key'];
			var totalDocs = country_aggs[i]['doc_count'];
			var centroid = window.app.country_centroids[key];
			var iconProps = getIconProps(totalDocs);
			var iconSize = iconProps['iconSize'];
			var sizeClass = iconProps['sizeClass'];
			var marker = new L.Marker([
			 	centroid.latitude,
			 	centroid.longitude
			], {
			    icon: L.divIcon({
			 		className: 'country-agg agg-icon ' + sizeClass,
			 		html: totalDocs,
			 		iconSize: [iconSize, iconSize]
			 	})
		    });

			marker.bindPopup('<p>loading...</p>');
			//We tag the geohash onto the marker for later use in the lookup
			//marker.geohash = geohash_aggs[i].key;
			//marker.geohashContentLoaded = false;
			marker.aggType = 'country';
			marker.country = centroid['common_name'];
			marker.aggregation = country_aggs[i];
			marker.docCount = totalDocs;
			marker.setZIndexOffset(500);
			country_markers.addLayer(marker);
		}

		map.addLayer(country_markers);

	}

	
	/**
	* Adds allometric aggregations to the map with precise latitude and longitude
	* @param {data} return object from an Elastic Search query 
	*/
	function addGeoHashMarkersToMap (data) {
		geohash_markers = L.featureGroup();
	
		var geohash_aggs = data.aggregations['Geohash-Grid'].buckets;
		for (var i=0;i<geohash_aggs.length;i++) {
			var html = "";
			var j;
			var totalLat = 0;
			var totalLon = 0;
			var centerLat, centerLon;
			var minLat, minLon, maxLat, maxLon;
			//var totalDocs = 0;
			
			//Some of the doc locations are in this geohash, while others are not
			//So here, we figure out which documents are in this geohash 
			//and average out the lats/lons from the geohashes terms agg
			var totalDocs = 0;
			var geohashKey = geohash_aggs[i].key;
			var geohashLatLon = decodeGeoHash(geohashKey);
			var minLat = geohashLatLon.latitude[0];
			var minLon = geohashLatLon.longitude[0];
			var maxLat = geohashLatLon.latitude[1];
			var maxLon = geohashLatLon.longitude[1];

			for(j=0; j < geohash_aggs[i].LatLon.buckets.length; j++ ) {
				// geohash_aggs[i].LatLon.buckets[j]
				// Object {key: "13.827800000,107.087500000", doc_count: 61}
				var docLatLon = geohash_aggs[i].LatLon.buckets[j].key.split(',');
				var docCount = geohash_aggs[i].LatLon.buckets[j].doc_count;				
				var docLat = 1 * docLatLon[0];
				var docLon = 1 * docLatLon[1];
				//if the parent aggregation key is at the start of the location geohash
				if ((docLat >= minLat) &&
					(docLat <= maxLat) &&
					(docLon >= minLon) &&
					(docLon <= maxLon)) {
				
					//Since these documents do belong to the geohash we are interested in, 
					//we add the documents to our total count
					totalDocs += docCount;
					totalLat += (docLat * docCount); 
					totalLon +=	(docLon * docCount); 
				}  
			}
			
			if(totalDocs) {
				//Actual center of records
				centerLat = totalLat / totalDocs;
				centerLon = totalLon / totalDocs;
			} else {
				centerLat = geohashLatLon.latitude[2];
				centerLon = geohashLatLon.longitude[2];
			}

			var iconProps = getGeoIconProps(geohash_aggs[i]['doc_count']);
			var iconSize = iconProps['iconSize'];
			var sizeClass = iconProps['sizeClass'];


			var marker = new L.Marker([
				centerLat,
				centerLon
			], {
				icon: L.divIcon({
					className: 'agg-icon ' + sizeClass,
					html: '', //geohash_aggs[i]['doc_count'],
					iconSize: [iconSize, iconSize]
				})
			});
			
			marker.bindPopup('<p>loading...</p>');
			//We tag the geohash onto the marker for later use in the lookup
			marker.geohash = geohash_aggs[i].key;
			marker.geohashContentLoaded = false;
			marker.aggType = 'geohash';
			marker.docCount = geohash_aggs[i]['doc_count'];
			//Keep track of the aggregation for later rendering
			marker.aggregation = geohash_aggs[i];
			geohash_markers.addLayer(marker);
			
		}
		map.addLayer(geohash_markers);
	}
	
	function getIconProps(totalDocs) {
		//Set the marker icon size based on the number of aggregations
		var sizeClass = 'agg-icon-1';
		var iconSize = totalDocs / 15 + 10;
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

		return {
			'sizeClass' : sizeClass,
			'iconSize' : iconSize
		}
	}

	function getGeoIconProps(totalDocs) {
		//Geographic icons without numbers
		var sizeClass = 'geo-agg-icon-1';
		var iconSize = totalDocs / 15 + 10;
		if(iconSize > 35) iconSize = 35;
		if (iconSize > 10 && iconSize < 11 ) {
			iconSize = 6;
			sizeClass = 'geo-agg-icon-1';
		} else if (iconSize >= 11 && iconSize < 20 ) { 
			iconSize = 8;
			sizeClass = 'geo-agg-icon-2';
		} else if (iconSize >= 20 && iconSize < 25 ) { 
			iconSize = 10;
			sizeClass = 'geo-agg-icon-3';
		} else if (iconSize >= 25 && iconSize < 30 ) { 
			iconSize = 12;
			sizeClass = 'geo-agg-icon-4';
		} else if (iconSize >= 30 && iconSize <= 35 ) { 
			iconSize = 14;
			sizeClass = 'geo-agg-icon-5';
		}

		return {
			'sizeClass' : sizeClass,
			'iconSize' : iconSize
		}
	}


	/**
	* Generates an elastic search query and retrieves the results from the server
	* drawing them on the map.  Query is limited to the extent of the map view (plus buffer)
	* to limit the number of features returned from the server and drawn on the map.  This
	* is particularly important when zoomed in as the number of features could be prohibitively
	* large
	*/
	function updateGeohashMarkers() {
		var bounds = map.getBounds();
		var zoom = map.getZoom();
		
		map.removeLayer(geohash_markers);

		if (zoom > 2) {

			//Add a 10% of the viewable map as a buffer
			var lngbuffer = Math.abs((bounds._northEast.lng - bounds._southWest.lng) * 0.1);
			var latbuffer = Math.abs((bounds._northEast.lat - bounds._southWest.lat) * 0.1);
			var maxx = bounds._northEast.lng + lngbuffer;
			var maxy = bounds._northEast.lat + latbuffer;
			var minx = bounds._southWest.lng - lngbuffer;
			var miny = bounds._southWest.lat - latbuffer;
			var precision = geoGridPrecision[map.getZoom()];

			var boundingBox = [minx, miny, maxx, maxy];

			var aggregations = [];
		
			aggregations.push(
				ejs.GeoHashGridAggregation('Geohash-Grid')
					.field('Geohash')
					.precision(precision)
					.aggregation(
						ejs.TermsAggregation('LatLon').field('LatLonString')
					)
					.aggregation(
						ejs.TermsAggregation('Species').field('Species')
					)
					.aggregation(
						ejs.TermsAggregation('Biome_FAO').field('Biome_FAO')
					)
					.aggregation(
						ejs.TermsAggregation('Output').field('Output')
					)
			);

			var geohash_query = window.app.searchManager.getQuery({
				aggregations : aggregations,
				boundingBox : boundingBox
			});

			window.app.searchManager.search({
				query : geohash_query,
				success: function (e) {
					addGeoHashMarkersToMap(e);
				}
			});
		} 
	}

	/**
	* Generates an elastic search query and retrieves the results from the server
	* drawing them on the map. 
	* This query only shows markers for records with only a country
	* specified and no exact lat/lon so they do not get updated on the zoom
	* like the geohash markers do 
	*/
	function loadCountryMarkers() {
		
		var aggregations = [];
		aggregations.push(
			ejs.TermsAggregation('country_3166_3')
					//'Country_3166_3' is the field in our index that we get value counts for
					.field('Country_3166_3')
					.size(1000)
			.aggregation(
				ejs.TermsAggregation('Species').field('Genus_Species')
			)
			.aggregation(
				ejs.TermsAggregation('Biome_FAO').field('Biome_FAO')
			)
			.aggregation(
					ejs.TermsAggregation('Output').field('Output')
			)	
		);

		var country_query = window.app.searchManager.getQuery({
			aggregations : aggregations
		});

		window.app.searchManager.search({
			query : country_query,
			success: function (e) {
				map.removeLayer(country_markers);
				addCountryMarkersToMap(e);
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

	//When someone clicks a geohash marker, it opens a popup
	//We fetch the summary and put it in the popup
	var loadGeoSummaryToPopup = function(marker, popup) {
		//Prevent double loading
		if(marker.contentLoaded) return;

		marker.contentLoaded = true;
		//Get our geohash bounds from the marker where we monkepathed them on
		var geohashBounds =  decodeGeoHash(marker.geohash);

		//Bounding box 
		//0 Min x (lon)
		//1 Min y (lat)
		//2 Max x (lon)
		//3 Max y (lat)
		var minx = geohashBounds['longitude'][0];
		var maxx = geohashBounds['longitude'][1];
		var miny = geohashBounds['latitude'][0];
		var maxy = geohashBounds['latitude'][1];
		var boundingBox = [minx, miny, maxx, maxy];
	
		var params = {'Min_Latitude'  : miny,
					  'Max_Latitude'  : maxy,
					  'Min_Longitude' : minx,
					  'Max_Longitude' : maxx,
			};

		var geohashedLink = window.app.searchManager.getLink(params);

		
		var html = getMarkerSummaryHTML(marker.aggregation);
		html += '<h5>Summary Area</h5>'
		html += '<p style="margin-top:0px;">Geohash: ' + marker.geohash + '<br>';
		html += 'Latitude: ' + geohashBounds['latitude'][0] + ' to ' + geohashBounds['latitude'][1] + '<br>';
		html += 'Longitude: ' + geohashBounds['longitude'][0] + ' to ' + geohashBounds['longitude'][1] + '<br>';
		html += '<a href="' + geohashedLink +'">Redo search to view just these records &gt;&gt;</a></p>';
		popup.setContent(html);
		
	}

	//When someone clicks a country marker, it opens a popup
	//We fetch the summary and put it in the popup
	var loadCountrySummaryToPopup = function(marker, popup) {
		//Prevent double loading
		if(marker.contentLoaded) return;
		marker.contentLoaded = true;
		//grab the country value that was patched onto the marker
		var country =  marker.country;
		var html = getMarkerSummaryHTML(marker.aggregation);
		html += '<h5>Summary Area</h5>';
		html += '<p style="margin-top:0px;"> Country summary for <strong>' + country + '</strong>.<br>';
		popup.setContent(html);
	}

	function getMarkerSummaryHTML(aggregation) {
		var html = "";
		html += '<h4>Equations: ' + aggregation.doc_count + '</h4>';
		if(aggregation['Species'].buckets.length) {
			html += '<h5>Species Represented</h5>'  
			html += '<p style="margin-top:0px;">' + getBucketsAsList(aggregation['Species'].buckets, ', ') + '</p>';
		}
		
		if(aggregation['Biome_FAO'].buckets.length){
			html += '<h5>FAO Biomes</h5>'  
			html += '<p style="margin-top:0px;">' + getBucketsAsList(aggregation['Biome_FAO'].buckets, ', ') + '</p>';
		}

		if(aggregation['Output'].buckets.length){
			html += '<h5>Output</h5>'  
			html += '<p style="margin-top:0px;">' + getBucketsAsList(aggregation['Output'].buckets, ', ') + '</p>';
		}
		
		return html;
	}


	//Public objects
	return {
		initOrShowMap : initOrShowMap,
		map : map
	}
}();