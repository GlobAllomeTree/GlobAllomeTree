
// Add in keys unique to the allometric equation search form
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

window.app.listController.config.recordLinkPrefix = 'allometric-equations';
window.app.listController.config.recordReadableType = 'Allometric Equation';
window.app.listController.config.customListTemplate = '\
  <dt><small>Equation</small></dt>					\
  <dd><code>{{Equation}}</code></dd>				\
  <dt><small>Output</small></dt>					\
  <dd><small>{{Output}}&nbsp;</small></dd>';

window.app.listController.config.getRecordContext = function (data) {
	var context = {};
	context['ID'] = data['Allometric_equation_ID'];
	context['Equation'] = data['Substitute_equation'];
	if(data['Output']) {
		context['Output'] = data['Output'];
	} else {
		context['Output'] = '';
	}
	return context;
}

