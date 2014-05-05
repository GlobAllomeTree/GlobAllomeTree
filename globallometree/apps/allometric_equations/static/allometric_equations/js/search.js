

//Declare a global namespace for our app
window.app = {};

window.app.config = {
	//address of elastic search
	elasticsearch :'http://localhost:9200/',
	index : 'globallometree',
	type : 'allometricequation'
}

//Add in functionality for searching
window.app.searchManager = function (){

	var searchDict;

	var search = function(dict) {
		//Save the search dictionary in the global context
		searchDict = dict;
	}

	//Get the type mapping for the current index
	var getMapping = function () {


	}


	var getSearchFields = function() {
		return {
			"Population": 'Mangroves',
		}
	}

	var getQuery = function (fields) {
		

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
		
		//Creates a simple_string query if the q parameter is set
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

	}

	return {
		getQuery : getQuery,
		search : search
	}

}();