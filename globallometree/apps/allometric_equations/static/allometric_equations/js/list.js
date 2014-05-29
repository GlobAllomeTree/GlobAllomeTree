
//Add in functionality for searching
window.app.listController = function () {

	//Only use safe Javascript
	"use strict";
	var $el, $resultsInfo, $resultsList;
	var currentPage = 0;
	var resultsPerPage = 50;
	var totalResults;
	var showingUntil = 0;

	var resultTemplate  = '<div class="panel panel-default"">						\
							<div class="panel-heading">								\
								<a href="/allometric-equations/{{ID}}/"				\
								   class="btn btn-default pull-right btn-xs"> 		\
									Detailed information 							\
									<span class="glyphicon glyphicon-chevron-right"></span> \
								</a>												\
								<h3 class="panel-title">							\
									<a href="/allometric-equations/{{ID}}/">		\
										Equation ID {{ID}}							\
									</a>											\
								</h3>												\
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
		$el.append('<div class="results-info"></div>		\
					<div id="results-list"></div>			\
					<div id="results-info-bottom" class="results-info"></div>');
		$resultsInfo = $('.results-info', $el);
		$resultsList = $('#results-list', $el);
		loadPage();
	}

	var loadPage = function() {
		var sm = window.app.searchManager;   

		var from = currentPage * resultsPerPage;
        sm.search({
        	//Get the current query and paginate it
            query : sm.getQuery().from(from).size(resultsPerPage),
            success : handleResponse
        });

        currentPage += 1;
	}

	var updateResultsInfo = function () {
		$resultsInfo.css('visibility', 'visible').html('');
		//Not totally clean, but update the search summary 
		//which is outside this view
		$('#summary-results-total').html(totalResults);

		if(totalResults < 5) {
			$('#results-info-bottom').hide();
		}
		if(totalResults == 0) {
			$resultsInfo.append('<p class="pull-left">No results were found for your query</p>');
			return;
		}
		

		var resultsShownCount = currentPage * resultsPerPage;
		if(resultsShownCount > totalResults) {
			resultsShownCount = totalResults;
		}

		if(resultsShownCount < totalResults) {
			var numToLoad = resultsPerPage;
			if (resultsShownCount > (totalResults - resultsPerPage)) {
				numToLoad = totalResults - resultsShownCount;
			}			
			$resultsInfo.append(' <button type="button" class="load-more-button btn btn-info btn-xs pull-right">Load next '+ numToLoad + '</span>  </button>')
		
			$('.load-more-button').click(function() {
				var anchorName = 'results-'+ (resultsShownCount + 1);
				$resultsList.append('<div id="'+ anchorName +'" class="alert alert-info">Results ' + (resultsShownCount + 1) + ' to ' +  (resultsShownCount + numToLoad) + '</div>');
				loadPage();
				$resultsInfo.css('visibility', 'hidden');
				$("html, body").animate({ scrollTop: $('#' + anchorName).offset().top - 20 }, 500);
			});
		}
		$resultsInfo.append('<p class="result-count pull-right">Showing results 1 to ' +  resultsShownCount + ' out of ' + totalResults + "</p>"); 

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