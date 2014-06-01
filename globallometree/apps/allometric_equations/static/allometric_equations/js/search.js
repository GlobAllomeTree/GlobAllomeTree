

//Add in functionality for searching
window.app.searchManager = function (){
	
	//Only use safe Javascript
	"use strict";

	var searchDict;

	//Simple term filters which can be string or boolean mapping types
	//When boolean 0,f alse, off, no and and empty string are false 
	var termFilterKeys = [  
		'Ecosystem', 
		'Population',
		'Genus',
		'Species',
		'Country',
		'Biome_HOLDRIDGE',
		'Biome_UDVARDY',
		'Biome_FAO',
		'Biome_WWF',
		'Division_BAILEY',
		'Author',
		'Reference',
		'Year',
		'B',
		'Bd',
		'Bg',
		'Bt',
		'L',
		'Rb',
		'Rf',
		'Rm',
		'S',
		'T',
		'F',
		'U',
		'V',
		'W',
		'X',
		'Z',
		'Unit_U', 
		'Unit_V',
		'Unit_W',
		'Unit_X',
		'Unit_Y',
		'Unit_Z',
		'Output'
	];

	//range filters
	var rangeFilterKeys = [
		'Min_X__gte',
		'Max_X__gte',
		'Min_Z__gte',
		'Max_Z__gte',
		'Min_X__lte',
		'Max_X__lte',
		'Min_Z__lte',
		'Max_Z__lte'
	]

		// //Allometry
		// Equation : 'term',
		

	var setSearchDict = function(dict) {
		//Save the search dictionary in the function context
		searchDict = dict;
	}

	var search = function(params) {
		
		$.ajax({
			type: "POST",
			url: window.app.config.search_url + '/globallometree/allometricequation/_search',
			data: JSON.stringify(params['query'].toJSON()),
			success: params['success']
		});
		
	}
	
	var getQuery = function (params) {
		//This base getQuery function is called by both the map and 
		//list views
		//The map view sometimes needs to pass a more restrictive bounding box
		if (!params) { params = {};}
			
		//Set the query and filters
		var dict = searchDict;
		var filters = [];

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
		if (searchDict['point_distance']) {
			filters.push(ejs.GeoDistanceFilter('Locations')
						.distance(searchDict['point_distance'])
						.unit('km') //km or mi
						.normalize(true)
						.point(ejs.GeoPoint([searchDict['point_latitude'],
										     searchDict['point_longitude']]))
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
			if($.inArray(key, rangeFilterKeys) != -1) {
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


		//Allow a custom bounding box to be passed in from the map
		//to further limit results
		if (params['boundingBox']) {
			var boundingBox = _constrainBoundingBox(params['boundingBox']);
			var geoFilter = ejs.GeoBboxFilter('Locations')
		 		.topLeft(ejs.GeoPoint([boundingBox[3], boundingBox[0]]))
		 		.bottomRight(ejs.GeoPoint([boundingBox[1], boundingBox[2]]));
		 	filters.push(geoFilter);
		}

		var query = ejs.Request();
		query.query(
			ejs.FilteredQuery(
				keywordQuery,
				ejs.AndFilter(filters)	
			)
		);

		if (params['aggregations']) {
			for(var i = 0; i < params['aggregations'].length; i++) {
				query.aggregation(params['aggregations'][i]);
			}
		}

		return query;
	}

	var _constrainBoundingBox = function(boundingBox) {

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
		return boundingBox;
	}


	return {
		setSearchDict : setSearchDict,
		getQuery : getQuery,
		search : search
	}

}();