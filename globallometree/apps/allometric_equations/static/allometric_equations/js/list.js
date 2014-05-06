
//Add in functionality for searching
window.app.listController = function () {

	//Only use safe Javascript
	"use strict";
	var $el, $resultsInfo, $resultsList;
	var page = 0;
	var resultsPerPage = 20;
	var totalResults;
	var showingUntil = 0;

	var resultTemplate = '';
	resultTemplate  = '<div class="panel panel-default"">							\
							<div class="panel-heading">								\
								<h3 class="panel-title">Equation ID {{ID}}</h3>		\
							</div>													\
							<div class="panel-body">								\
								<dl class="dl-horizontal">							\
								  <dt><small>Equation</small></dt>					\
								  <dd><code>{{Equation}}</code></dd>				\
								 													\
								  <dt><small>FAO Biomes</small></dt>				\
								  <dd><small>{{Biome_FAO}}</small></dd>   			\
								 													\
								  <dt><small>Species</small></dt>					\
								  <dd><small>{{Species}}</small></dd>				\
								  								 					\
								  <dt><small>Countries</small></dt>					\
								  <dd><small>{{Country}}</small></dd>				\
								  													\
								  <dt><small>Year</small></dt>						\
								  <dd><small>{{Year}}</small></dd>					\
								</dl>												\
							</div>													\
					   </div>';

	var init = function (params) {
		//Get the element where we will render the list results
		$el = $('#' + params['el']);	
		$el.append('<div class="results-info"></div><div id="results-list"></div><div class="results-info"></div>');
		$resultsInfo = $('.results-info', $el);
		$resultsList = $('#results-list', $el);
		loadPage();
	}

	var loadPage = function() {
		var sm = window.app.searchManager;   
        sm.search({
            query : sm.getQuery(),
            success : handleResponse
        });
	}

	var updateResultsInfo = function () {
		//Not totally clean, but update the search summary 
		//which is outside this view
		$('#summary-results-total').html(totalResults);
		$resultsInfo.html('Showing results 1 to ' +  15 + ' out of ' + totalResults); 
	}

	var handleResponse = function(response) {
		totalResults = response['hits']['total'];
		updateResultsInfo();
		appendResults(response['hits']['hits']);
	}

	var appendResults = function (hits) {
		for (var i = 0; i < hits.length; i++) {
			//Use the elasticsearch document source
			var data = hits[i]['_source'];
			var context = {};

			context['ID'] = data['ID'];
			context['Equation'] = data['Equation'];
			if(data['Genus_Species']) {
				context['Species'] = data['Genus_Species'].join(', ');
			}
			if(data['Country']) {
				context['Country'] = data['Country'].join(', ');
			}
			if(data['Biome_FAO']) {
				context['Biome_FAO'] = data['Biome_FAO'].join(', ');
			}
			if(data['Year']) {
				context['Year'] = data['Year'].join(', ');
			}
			$resultsList.append(Mustache.render(resultTemplate, context));	
		}
	}

	
	//Public functions
	return {
		init : init
	}

}();