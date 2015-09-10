
//Add in functionality for searching
window.app.listController = function () {

	//Only use safe Javascript
	"use strict";
	var $el, $resultsInfo, $resultsList;
	var currentPage = 0;
	var resultsPerPage = 50;
	var totalResults;
	var showingUntil = 0;

	var config = {
			recordLinkPrefix : '',
			recordReadableType : '',
			customListTemplate : '',
			getRecordContext : function (data) { return {}}
		}
	
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

	var getResultTemplate = function () {
		var template =   '<div class="panel panel-default"">						\
							<div class="panel-heading">								\
								<a href="/data/{{ recordLinkPrefix }}/{{ID}}/"		\
								   class="btn btn-default pull-right btn-xs"> 		\
									Detailed information 							\
									<span class="glyphicon glyphicon-chevron-right"></span> \
								</a>												\
								{{#showDatasetLink}}								\
								<a href="{{ datasetLink }}"							\
								style="margin-right:15px"							\
								   class="btn btn-success pull-right btn-xs"> 		\
									Request Access to Dataset						\
								</a>												\
								{{/showDatasetLink}}								\
								<h3 class="panel-title">							\
									<a href="/data/{{ recordLinkPrefix }}/{{ID}}/">	\
										{{recordReadableType }} {{ID}}				\
									</a>											\
								</h3>												\
							</div>													\
							<div class="panel-body">								\
								<dl class="dl-horizontal">' + config['customListTemplate'] + '\
								  													\
								  <dt><small>Reference</small></dt>					\
								  <dd><small>{{{Reference}}}&nbsp;</small></dd>	    \
										  								 			\
								  <dt><small>Reference Year</small></dt>			\
								  <dd><small>{{{Year}}}&nbsp;</small></dd>	        \
										  								 			\
								  <dt><small>FAO Biomes</small></dt>				\
								  <dd><small>{{{Zone_FAO}}}&nbsp;</small></dd>   	\
								 													\
								  <dt><small>Species</small></dt>					\
								  <dd><small>{{{Species}}}&nbsp;</small></dd>		\
																					\
								  <dt><small>Locations</small></dt>					\
								  <dd><small>{{{Locations}}}&nbsp;</small></dd>		\
								  													\
								</dl>												\
							</div>													\
					   </div>';
		return template;
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
		var searchDict = window.app.searchManager.getCurrentSearchDict();
		for (var i = 0; i < hits.length; i++) {
			//Use the elasticsearch document source
			var data = hits[i]['_source'];
			var context = config.getRecordContext(data);

			try {
				var speciesList = [];
				for (var j=0; j < data['Species_group']['Group'].length; j++ ) {
					var species_record = data['Species_group']['Group'][j];
					var speciesHTML = species_record['Family'];
					speciesHTML += ' ' + species_record['Genus'];
					speciesHTML += ' ' + species_record['Species'];
					speciesList.push(speciesHTML);
				}
				context['Species'] = speciesList.join(', ');

			} catch (e) {
				context['Species'] = '';
			}


			try {
				var ZoneFAOList = [];
				var countryList = [];
				var locationList = [];
				for (var j=0; j < data['Location_group']['Group'].length; j++ ) {
					var location_record = data['Location_group']['Group'][j];
					if (!_.contains(ZoneFAOList,location_record['Zone_FAO'])) {
						ZoneFAOList.push(location_record['Zone_FAO'])
					}

					if (!_.contains(countryList,location_record['Country'])) {
						countryList.push(location_record['Country'])
					}
					var locationHTML = '';
					if (location_record['Name']) {
						locationHTML += location_record['Name'] + ', ';
					}
					if (location_record['Country']) {
						locationHTML += ' ' + location_record['Country'];
					}

					if (location_record['Latitude']) {

						var latLonText = ' (lat ' + location_record['Latitude'] +  ', lon ' + location_record['Longitude'] + ')';	
						
						if (searchDict['Max_Latitude'] 
						&& searchDict['Min_Latitude'] 
						&& searchDict['Min_Longitude'] 
						&& searchDict['Max_Longitude'] 
						&& location_record['Latitude'] <= searchDict['Max_Latitude'] 
						&& location_record['Latitude'] >= searchDict['Min_Latitude'] 
						&& location_record['Longitude'] >= searchDict['Min_Longitude'] 
						&& location_record['Longitude'] <= searchDict['Max_Longitude']) {
							latLonText = '<strong>' + latLonText + '</strong>';
						} else {
							latLonText = '<span style="color:#888">' + latLonText + '</span>';
						}
		
						locationHTML += latLonText;
					}

					locationList.push(locationHTML);
				}
				context['Zone_FAO'] = ZoneFAOList.join('<br>');
				context['Country'] = countryList.join('<br>');
				context['Locations'] = locationList.join('<br> ');

			} catch (e) {
				context['Zone_FAO'] = '';
				context['Country'] = '';
				context['Locations'] = '';
			}

			try {
				context['Reference'] = data['Source']['Reference'];
				context['Year'] = data['Source']['Reference_year'];
			} catch (e) {
				context['Reference'] = '';
				context['Year'] = '';
			}

			context['recordLinkPrefix'] = config['recordLinkPrefix'];
			context['recordReadableType'] = config['recordReadableType'];

			try {
				context['showDatasetLink'] = ! data['Dataset']['User_has_access']; 
				context['datasetLink'] = data['Dataset']['Dataset_url'];
			} catch (e) {
				context['showDatasetLink'] = false; 
				context['datasetLink'] = '';
			}

			$resultsList.append(Mustache.render(getResultTemplate(), context));	
		}
	}

	//Public functions
	return {
		init : init,
		config : config
	}

}();