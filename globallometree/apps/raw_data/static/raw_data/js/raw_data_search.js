
// Add in keys and config unique to the allometric equation search 
window.app.searchManager.config.termFilterKeys = [
		];

window.app.searchManager.config.rangeFilterKeys = [
        'DBH_cm__gte',
        'DBH_cm__lte',
        'H_m__gte',
        'H_m__lte',
        'CD_m__gte',
        'CD_m__lte',
	];

window.app.searchManager.config.indexName = 'rawdata';
window.app.searchManager.config.sortField = 'ID_RD';

window.app.listController.config.recordLinkPrefix = 'raw-data';
window.app.listController.config.recordReadableType = 'Raw Data';

window.app.listController.config.customListTemplate = '\
  <dt><small>Tree Height (H_m) </small></dt>					   \
  <dd>{{ H_m }}</dd>     \
  <dt><small>Tree Diameter (DBH_cm) </small></dt>                    \
  <dd>{{ DBH_cm }}</dd>     \
  <dt><small>Total Volume (Volume_m3) </small></dt>                    \
  <dd>{{ Volume_m3 }}</dd>     \
  ';

window.app.listController.config.getRecordContext = function (data) {
	data['ID'] = data['ID_RD'];
	return data;
}

window.app.mapController.config.renderCustomAggHTML = function (aggregation) {
	var html = '';
	return html;
}

window.app.mapController.config.recordReadableTypePlural = 'Raw Data';
window.app.mapController.config.customGeohashAggs = [];
