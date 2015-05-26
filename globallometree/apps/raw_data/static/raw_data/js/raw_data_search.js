
// Add in keys and config unique to the allometric equation search 
window.app.searchManager.config.termFilterKeys = [
        'Forest_type'
		];

window.app.searchManager.config.rangeFilterKeys = [
		'H_tree_avg__gte',
        'H_tree_avg__lte',
        'Tree_ID__gte',
        'Tree_ID__lte',
        'Date_collection__gte',
        'Date_collection__lte',
        'DBH_cm__gte',
        'DBH_cm__lte',
        'H_m__gte',
        'H_m__lte',
        'CD_m__gte',
        'CD_m__lte',
        'F_Bole_kg__gte',
        'F_Bole_kg__lte',
        'F_Branch_kg__gte',
        'F_Branch_kg__lte',
        'F_Foliage_kg__gte',
        'F_Foliage_kg__lte',
        'F_Stump_kg__gte',
        'F_Stump_kg__lte',
        'F_Buttress_kg__gte',
        'F_Buttress_kg__lte',
        'F_Roots_kg__gte',
        'F_Roots_kg__lte',
        'Volume_bole_m3__gte',
        'Volume_bole_m3__lte',
        'WD_AVG_gcm3__gte',
        'WD_AVG_gcm3__lte',
        'DF_Bole_AVG__gte',
        'DF_Bole_AVG__lte',
        'DF_Branch_AVG__gte',
        'DF_Branch_AVG__lte',
        'DF_Foliage_AVG__gte',
        'DF_Foliage_AVG__lte',
        'DF_Stump_AVG__gte',
        'DF_Stump_AVG__lte',
        'DF_Buttress_AVG__gte',
        'DF_Buttress_AVG__lte',
        'DF_Roots_AVG__gte',
        'DF_Roots_AVG__lte',
        'D_Bole_kg__gte',
        'D_Bole_kg__lte',
        'D_Branch_kg__gte',
        'D_Branch_kg__lte',
        'D_Foliage_kg__gte',
        'D_Foliage_kg__lte',
        'D_Stump_kg__gte',
        'D_Stump_kg__lte',
        'D_Buttress_kg__gte',
        'D_Buttress_kg__lte',
        'D_Roots_kg__gte',
        'D_Roots_kg__lte',
        'ABG_kg__gte',
        'ABG_kg__lte',
        'BGB_kg__gte',
        'BGB_kg__lte',
        'Tot_Biomass_kg__gte',
        'Tot_Biomass_kg__lte',
        'BEF__gte',
        'BEF__lte'
	];

window.app.searchManager.config.indexName = 'rawdata';

window.app.listController.config.recordLinkPrefix = 'raw-data';
window.app.listController.config.recordReadableType = 'Raw Data';
window.app.listController.config.customListTemplate = '\
  <dt><small>Forest Type </small></dt>					   \
  <dd>{{ Forest_type }}</dd>';

window.app.listController.config.getRecordContext = function (data) {
	data['ID'] = data['Raw_data_ID'];
	return data;
}

window.app.mapController.config.renderCustomAggHTML = function (aggregation) {
	var html = '';
	return html;
}

window.app.mapController.config.recordReadableTypePlural = 'Raw Data';
window.app.mapController.config.customGeohashAggs = [];
