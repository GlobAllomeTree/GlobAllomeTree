
// Add in keys and config unique to the allometric equation search 
window.app.searchManager.config.termFilterKeys = [
		'Ecosystem', 
		'Population',
		'B',
		'Bd',
		'Bg',
		'Bt',
		'L',
		'Rb',
		'Rf',
		'Rm',
		'S',
		'T',
		'F',
		'U',
		'V',
		'W',
		'X',
		'Z',
		'Unit_U', 
		'Unit_V',
		'Unit_W',
		'Unit_X',
		'Unit_Y',
		'Unit_Z',
		'Output'];

window.app.searchManager.config.rangeFilterKeys = [
		'Min_X__gte',
		'Max_X__gte',
		'Min_Z__gte',
		'Max_Z__gte',
		'Min_X__lte',
		'Max_X__lte',
		'Min_Z__lte',
		'Max_Z__lte'
	];

window.app.searchManager.config.indexName = 'allometricequation';


window.app.listController.config.recordLinkPrefix = 'allometric-equations';
window.app.listController.config.recordReadableType = 'Allometric Equation';
window.app.searchManager.config.sortField = 'ID_AE';
window.app.listController.config.customListTemplate = '\
  <dt><small>Equation</small></dt>					   \
  <dd><code>{{Equation}}</code></dd>				   \
  <dt><small>Output</small></dt>					   \
  <dd><small>{{Output}}&nbsp;</small></dd>';

window.app.listController.config.getRecordContext = function (data) {
	data['ID'] = data['ID_AE'];
	data['Equation'] = data['Substitute_equation'];
	if(data['Output']) {
		data['Output'] = data['Output'];
	} else {
		data['Output'] = '';
	}
	debugger;
	return data;
}

window.app.mapController.config.renderCustomAggHTML = function (aggregation) {
	var html = '';
	if(aggregation['Output'].buckets.length){
		html += '<h5>Output</h5>'  
		html += '<p style="margin-top:0px;">' + window.app.mapController.getBucketsAsList(aggregation['Output'].buckets, ', ') + '</p>';
	}
	return html;
}

window.app.mapController.config.recordReadableTypePlural = 'Allometric Equations';
window.app.mapController.config.customGeohashAggs = [
	ejs.TermsAggregation('Output').field('Output')
];
