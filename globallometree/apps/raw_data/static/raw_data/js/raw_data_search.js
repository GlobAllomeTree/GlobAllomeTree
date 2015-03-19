
// Add in keys and config unique to the allometric equation search 
window.app.searchManager.config.termFilterKeys = [
		];

window.app.searchManager.config.rangeFilterKeys = [
		
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
