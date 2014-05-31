

//Add in functionality for searching
window.app.searchManager = function (){
	
	//Only use safe Javascript
	"use strict";

	var searchDict;
	var termFilterKeys = [  'Ecosystem', 
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
							'Year'];

		//Components
		// B : 'term',
		// Bd : 'term',
		// Bg : 'term',
		// Bt : 'term',
		// L : 'term',
		// Rb : 'term',
		// Rf : 'term',
		// Rm : 'term',
		// S : 'term',
		// T : 'term',
		// F : 'term',
		// //Input/Output
		// U : 'term',
		// V : 'term',
		// W : 'term',
		// X : 'term',
		// Z : 'term',
		// Unit_U : 'term',
		// Unit_V : 'term',
		// Unit_W : 'term',
		// Unit_X : 'term',
		// Unit_Y : 'term',
		// Unit_Z : 'term',
		// Min_X__gte : 'term',
		// Max_X__gte : 'term',
		// Min_Z__gte : 'term',
		// Max_Z__gte : 'term',
		// Output : 'term',
		// Min_X__lte : 'term',
		// Max_X__lte : 'term',
		// Min_Z__lte : 'term',
		// Max_Z__lte : 'term',
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
		
		if (!params) { params = {};}
			
		//Set the query and filters
		var dict = searchDict;
		var filters = [];

		if (searchDict['q']) {
			var keywordQuery = ejs.MatchQuery("Keywords", searchDict['q']).type('phrase');
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

		//Simple term filters
		for (var key in searchDict) {
			if($.inArray(key, termFilterKeys)) {
				var searchValue = searchDict[key];
				filters.push(ejs.TermFilter(key, searchValue));
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