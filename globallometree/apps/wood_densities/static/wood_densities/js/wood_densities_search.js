
// Add in keys and config unique to the wood density search 
window.app.searchManager.config.termFilterKeys = [
        'Methodology',
        'Bark',
        'MC_Density',
        'Data_origin',
        'Data_type'
		];

window.app.searchManager.config.rangeFilterKeys = [
		'H_tree_avg__gte',
        'H_tree_avg__lte',
        'H_tree_min__gte',
        'H_tree_min__lte',
        'H_tree_max__gte',
        'H_tree_max__lte',
        'DBH_tree_avg__gte',
        'DBH_tree_avg__lte',
        'DBH_tree_max__gte',
        'DBH_tree_max__lte',
        'DBH_tree_min__gte',
        'DBH_tree_min__lte',
        'm_WD__gte',
        'm_WD__lte',
        'MC_m__gte',
        'MC_m__lte',
        'V_WD__gte',
        'V_WD__lte',
        'MC_V__gte',
        'MC_V__lte',
        'CR__gte',
        'CR__lte',
        'FSP__gte',
        'FSP__lte',
        'Density_g_cm3__gte',
        'Density_g_cm3__lte',
        'Samples_per_tree__gte',
        'Samples_per_tree__lte',
        'Number_of_trees__gte',
        'Number_of_trees__lte',
        'SD__gte',
        'SD__lte',
        'Min__gte',
        'Min__lte',
        'Max__gte',
        'Max__lte',
        'H_measure__gte',
        'H_measure__lte',
        'Bark_distance__gte',
        'Bark_distance__lte'
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
