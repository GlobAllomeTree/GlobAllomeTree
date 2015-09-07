
// Add in keys and config unique to the allometric equation search 
window.app.searchManager.config.termFilterKeys = [
        'Input',
        'Output',
        'Interval_validity'
		];

window.app.searchManager.config.rangeFilterKeys = [
		'Growing_stock__gte',
        'Growing_stock__lte',
        'Aboveground_biomass__gte',
        'Aboveground_biomass__lte',
        'Net_annual_increment__gte',
        'Net_annual_increment__lte',
        'Stand_density__gte',
        'Stand_density__lte',
        'Age__gte',
        'Age__lte',
        'BEF__gte',
        'BEF__lte'
	];

window.app.searchManager.config.indexName = 'biomassexpansionfactor';

window.app.listController.config.recordLinkPrefix = 'biomass-expansion-factors';
window.app.searchManager.config.sortField = 'Biomass_ezpansion_factor_ID';
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
