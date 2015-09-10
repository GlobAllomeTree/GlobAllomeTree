

//Add in functionality for searching
window.app.searchManager = function (){
	
	//Only use safe Javascript
	"use strict";

	var searchDict;

	var baseTermFilterKeys = [
			'Family',
			'Genus',
			'Species',
			'Country',
			'Zone_Holdridge',
			'Ecoregion_Udvardy',
			'Zone_FAO',
			'Ecoregion_WWF',
			'Division_Bailey',
			'Reference_author',
			'Reference',
			'Reference_year',
			'Tree_type',
			'Population_type'];

	// Simple term filters which can be string or boolean mapping types
	// When boolean 0,f alse, off, no and and empty string are false 
	// Declare an object propery which later gets modified by individual config files
	var config = {};

	var setSearchDict = function(dict) {
		//Save the search dictionary in the function context
		searchDict = dict;
	}

	var search = function(params) {
		$.ajax({
			type: "POST",
			url: window.app.config.search_url + '/globallometree/' + config.indexName + '/_search',
			data: JSON.stringify(params['query'].toJSON()),
			success: params['success']
		});
	}

	var isPreciseLocationSearch = function() {
		var preciseSearchKeys = ['Min_Latitude', 'Max_Latitude', 'Min_Longitude', 'Max_Longitude'];
		for (var i in preciseSearchKeys) {
			if (preciseSearchKeys[i] in searchDict) {
				return true;
			}
		}
		return false;
	}
	
	var getQuery = function (params) {

		var termFilterKeys = _.union(baseTermFilterKeys, config.termFilterKeys);

		//This base getQuery function is called by both the map and 
		//list views
		//The map view sometimes needs to pass a more restrictive bounding box
		if (!params) { params = {};}
			
		//Set the query and filters
		var filters = [];
		var boundingBox;

		//If there is a keyword search, we match _all
		//which is a special field in elastic search that has
		//text indexed from all of the other fields and is available by default
		if (searchDict['q']) {
			var keywordQuery = ejs.MatchQuery("_all", searchDict['q']);
		} else {
			var keywordQuery = ejs.MatchAllQuery();
		}

		//If this search is trying to limit with a certain distance from a
		//point then we use a Geo
		if (searchDict['Point_Latitude']) {
			filters.push(ejs.GeoDistanceFilter('Geohash')
						.distance(1*searchDict['Point_Distance'])
						.unit('km') //km or mi
						.normalize(true)
						.point(ejs.GeoPoint([1*searchDict['Point_Latitude'],
										     1*searchDict['Point_Longitude']]))
			)
		}	

		if (searchDict['Equation']) {
			filters.push(ejs.RegexpFilter('Equation', searchDict['Equation']))
		}

		for (var key in searchDict) {
			var searchValue = searchDict[key];
			//Simple term filters
			if($.inArray(key, termFilterKeys) != -1) {		
				filters.push(ejs.TermFilter(key, searchValue));
			}
			//Range filters
			if($.inArray(key, config.rangeFilterKeys) != -1) {
				//Key is assumed to look like fieldname__gte
				var parts = key.split('__')
				var field = parts[0];
				var filterTypeName = parts[1];
				if (filterTypeName == 'gte') {
					filters.push(ejs.RangeFilter(field).gte(searchValue))
				} else if (filterTypeName == 'lte') {
					filters.push(ejs.RangeFilter(field).lte(searchValue))
				}
			}

		}

		if(params['boundingBox'] || isPreciseLocationSearch()) {
			//Allow a custom bounding box to be passed in from the map
			//to further limit results
			//Bounding box 
			//0 Min x (lon)
			//1 Min y (lat)
			//2 Max x (lon)
			//3 Max y (lat)
			if(params['boundingBox']) {
				boundingBox = params['boundingBox'];
			} else {
				boundingBox = [-179.9999, -89.9999, 179.9999, 89.9999];
			}
			boundingBox = _constrainBoundingBox(boundingBox);

			var geoFilter = ejs.GeoBboxFilter('Geohash')
		 		.topLeft(ejs.GeoPoint([boundingBox[3], boundingBox[0]]))
		 		.bottomRight(ejs.GeoPoint([boundingBox[1], boundingBox[2]]));
		 	filters.push(geoFilter);
		}
		
		if (params['filters']) {
			for(var i = 0; i < params['filters'].length; i++) {
				filters.push(params['filters'][i]);
			}
		}

		var query = ejs.Request();
		query.query(
			ejs.FilteredQuery(
				keywordQuery,
				ejs.AndFilter(filters)	
			)
		);

		query.sort(config.sortField);

		if (params['aggregations']) {
			for(var i = 0; i < params['aggregations'].length; i++) {
				query.aggregation(params['aggregations'][i]);
			}
		}

		return query;
	}

	/*
	* Get a link and replace out some params in the url
	* Simplistic function that allows replacing the current search with a new one
	* If this current url is ?q=Acacia
	* window.app.searchManager.getLink({'foo' : 'bar'});
	* "?q=Acacia&foo=bar"
	* window.app.searchManager.getLink({'q' : 'bar'});
	* "?q=bar"
	*/
	var getLink = function(params) {
		var parts = [];

		//create a local copy of the search dict to not edit the global one
		var dict = {};
		for (var key in searchDict) {
			dict[key] = searchDict[key];
		}
		//override dict with params
		for(var key in params) {
			dict[key] = params[key];
		}
		for(var key in dict) {
			parts.push(key + '=' + dict[key]); 
		}
		return '?' + parts.join('&');
	}

	// Currently done on the server side
	// //Decodes the url to get the current params
	// //returns a dictionary
	// var getCurrentSearchDict = function() {
	// 	var query = window.location.search.substring(1);
	// 	var vars = query.split('&');
	// 	var dict = {};
	// 	for(var i = 0; i < vars.length; i ++) {
	// 		var parts = vars[i].split('=');
	// 		if (parts[1] !== '') {
	// 			dict[parts[0]] = parts[1];
	// 		}
	// 	}
	// 	return dict;
	// }

	var _constrainBoundingBox = function(boundingBox) {

		//Elastic Search treats values of 180 and -180 as a width of 0 and 90, -90 as a height of 0
		//Makes sure to pass values that will actually return the required results.
		//Additionally, Leaflet will pan from world copy to world copy.  This can create values infinitly
		//far outside of allowed geographic coordinates.  This snaps requests back to the primary map
		//We can prevent leaflet from loading outside of the defined geographic coordinates for the globe
		
		//This also takes into account the min/max latitude/longitude from the

		var Min_Latitude = -89.99999;
		var Max_Latitude = 89.99999;
		var Min_Longitude = -179.99999;
		var Max_Longitude = 179.99999;


		if('Min_Latitude' in searchDict) {
			Min_Latitude = 1 * searchDict['Min_Latitude'];
		}

		if('Max_Latitude' in searchDict) {
			Max_Latitude = 1 * searchDict['Max_Latitude'];
		}

		if('Min_Longitude' in searchDict) {
			Min_Longitude = 1 * searchDict['Min_Longitude'];
		}

		if('Max_Longitude' in searchDict) {
			Max_Longitude = 1 * searchDict['Max_Longitude'];
		}
		
		//0 Min x (lon)
		//1 Min y (lat)
		//2 Max x (lon)
		//3 Max y (lat)

		if (boundingBox[0] < Min_Longitude) {
			boundingBox[0] = Min_Longitude;
		}
		if (boundingBox[1] < Min_Latitude) {
			boundingBox[1] = Min_Latitude;
		}
		if (boundingBox[2] > Max_Longitude) {
			boundingBox[2] = Max_Longitude;
		}
		if (boundingBox[3] > Max_Latitude) {
			boundingBox[3] = Max_Latitude;
		}
		return boundingBox;
	}

	var getCurrentSearchDict = function() {
		return searchDict;
	}

	return {
		setSearchDict : setSearchDict,
		getQuery : getQuery,
		search : search,
		getLink : getLink,
		getCurrentSearchDict : getCurrentSearchDict,
		config : config
	}

}();