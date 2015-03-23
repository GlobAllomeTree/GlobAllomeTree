
// Add in keys and config unique to the allometric equation search 
window.app.searchManager.config.termFilterKeys = [
		];

window.app.searchManager.config.rangeFilterKeys = [
		
	];

window.app.searchManager.config.indexName = 'biomassexpansionfactor';

window.app.listController.config.recordLinkPrefix = 'biomass-expansion-factors';
window.app.listController.config.recordReadableType = 'Biomass Expansion Factor';
window.app.listController.config.customListTemplate = '\
  <dt><small>Biomass Expansion Factor </small></dt>					   \
  <dd>{{ BEF }}</dd>';

window.app.listController.config.getRecordContext = function (data) {
	data['ID'] = data['ID_BEF'];
	return data;
}

window.app.mapController.config.renderCustomAggHTML = function (aggregation) {
	var html = '';
	return html;
}

window.app.mapController.config.recordReadableTypePlural = 'Biomass Expansion Factors';
window.app.mapController.config.customGeohashAggs = [];
