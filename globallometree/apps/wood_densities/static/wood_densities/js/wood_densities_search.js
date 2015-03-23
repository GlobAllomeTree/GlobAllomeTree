
// Add in keys and config unique to the wood density search 
window.app.searchManager.config.termFilterKeys = [
		];

window.app.searchManager.config.rangeFilterKeys = [
		
	];

window.app.searchManager.config.indexName = 'wooddensity';

window.app.listController.config.recordLinkPrefix = 'wood-densities';
window.app.listController.config.recordReadableType = 'Wood Density';
window.app.listController.config.customListTemplate = '\
  <dt><small>Density g/cm3 </small></dt>					   \
  <dd>{{ Density_g_cm3 }}</dd>';

window.app.listController.config.getRecordContext = function (data) {
	data['ID'] = data['Wood_density_ID'];
	return data;
}

window.app.mapController.config.renderCustomAggHTML = function (aggregation) {
	var html = '';
	return html;
}

window.app.mapController.config.recordReadableTypePlural = 'Wood Densities';
window.app.mapController.config.customGeohashAggs = [];
