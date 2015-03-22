// #Options
// -----------------------------------------------------------------------------

OPTIONS = {};

OPTIONS.fields = {};

OPTIONS.fields.order = ["X",  "Unit_X",  "Z",  "Unit_Z",  "W",  "Unit_W",  "U",
"Unit_U",  "V",  "Unit_V",  "Min_X",  "Max_X",  "Min_Z",  "Max_Z",  "Output",
"Output_TR",  "Unit_Y",  "Age",  "Veg_Component",  "B",  "Bd",  "Bg",  "Bt",
"L",  "Rb",  "Rf",  "Rm",  "S",  "T",  "F",  "Equation",  "Substitute_equation",
"Top_dob",  "Stump_height",  "R2",  "R2_Adjusted",  "RMSE",  "SEE",
"Corrected_for_bias",  "Bias_correction",  "Ratio_equation",
"Segmented_equation",  "Sample_size",  "Population",  "Tree_type"];

OPTIONS.language = "en"

// #Models
//
// -----------------------------------------------------------------------------

// Field Model
// ===========
var FieldModel = Backbone.Model.extend({
});

// Dataset Model
// =============
var DatasetModel = Backbone.Model.extend({});

// #Collections
//
// -----------------------------------------------------------------------------


// Field Collection
// ================
var FieldCollection = Backbone.Collection.extend({
  model: FieldModel,
  // Description:
  // ------------
  //
  // Initialize using the default fields defined in OPTIONS.
  initialize: function (options) {
    var i;

    if (options === void(0)) {
      _.each(OPTIONS.fields.order, function (key) {
        this.add({key: key, value: void(0)})
      }, this)
    }
  }
});

// Dataset Collection
// ==================
var DatasetCollection = Backbone.Collection.extend({
  model: DatasetModel
});

// #Views
//
// -----------------------------------------------------------------------------

// Field Item View
// ===============
var FieldItemView = Marionette.ItemView.extend({
  template: "#templateInput",
  tagName: "li",
  className: "form-group",

  // Parameters:
  // -----------
  //
  // 1. `options` - object
  initialize: function (options) {},


  // Description:
  // ------------
  //
  // Extends the model passed to the view with additional  _fieldParameters_.
  templateHelpers: function () {
    var key = this.model.get("key")
      , fieldParameters = this._fieldParameters[key] || {};

    return {
      // Description:
      // ------------
      //
      // By default return the value of _name_ with underscores replaced by
      // whitespace
      label: fieldParameters.label || key.replace(/_/g, " "),
      // Description:
      // ------------
      //
      // By default return the value of _name_
      id: fieldParameters.id || key,
      // Description:
      // ------------
      //
      // By default return an empty string
      value: this.model.get("value") || "",
      // Description:
      // ------------
      //
      // Sets the _type_ attribute of input elements.
      type: this.model.get("type") || "text"
    }
  },

  _fieldParameters: {
    "Bias_correction": {},
    "Corrected_for_bias": {},
    "Tree_type": {},
    "Sample_size": {},
    "Stump_height": {},
    "Output_TR": {},
    "Veg_Component": {
      label: "Vegetation component"
    },
    "SEE": {},
    "Equation": {
      maxlength: 500
    },
    "Substitute_equation": {},
    "Segmented_equation": {},
    "Ratio_equation": {},
    "Population": {},
    "Age": {},
    "Top_dob": {},
    "Contributor": {},
    "Operator": {},
    "Output": {
      maxlength: 30
    },
    "R2": {
      label: "R&sup2;"
    },
    "R2_Adjusted": {
      label: "R&sup2; Adjusted"
    },
    "RMSE": {
      label: "Root mean-square error"
    },
    "B": {
      label: "B - Bark"
    },
    "Bd": {
      label: "Bd - Dead branches"
    },
    "Bg": {
      label: "Bg - Big branches"
    },
    "Bt": {
      label: "Bt - Thin branches"
    },
    "L": {
      label: "L - Leaves"
    },
    "Rb": {
      label: "Rb - Large roots"
    },
    "Rf": {
      label: "Rf - Fine roots"
    },
    "Rm": {
      label: "Rm - Medium roots"
    },
    "S": {
      label: "S - Stump"
    },
    "T": {
      label: "T - Trunks"
    },
    "F": {
      label: "F - Fruit"
    },
    "U": {},
    "Unit_U": {},
    "V": {},
    "Unit_V": {},
    "W": {},
    "Unit_W": {},
    "X": {
      maxlength: 20
    },
    "Unit_X": {
      maxlength: 20
    },
    //"Y": {},
    "Unit_Y": {},
    "Z": {
      maxlength: 20
    },
    "Unit_Z": {
      maxlength: 20
    },
    "Min_X": {
      maxlength: 16
    },
    "Max_X": {
      maxlength: 16
    },
    "Min_Z": {
      maxlength: 16
    },
    "Max_Z": {
      maxlength: 16
    }
  }
});

// Field Composite View
// ====================
var FieldCompositeView = Backbone.Marionette.CompositeView.extend({
  template: "#templateFieldCollection",
  className: "panel panel-default",
  childView: FieldItemView,
  childViewContainer: "ul",
  // Description:
  // ------------
  //
  // Sets the collection for this composite view to that of the value of the
  // _fields_ for the of the parent model.
  initialize: function (options) {
    this.collection = this.model.get("fields") || new FieldCollection();
  },
  // Description:
  // ------------
  //
  // Sets some additional view variables.
  templateHelpers: function () {
    return {
      index: this._index,
      isExpanded: this._index === 0 ? "true" : "false"
    }
  }
});

// Dataset Collection View
// =======================
var DatasetCollectionView = Backbone.Marionette.CompositeView.extend({
  template: "#templateDatasetCollection",
  childView: FieldCompositeView,
  childViewContainer: "#datasetCollection",
  ui: {
    "equationAdd": "#equationAdd"
  },
  events: {
    "click @ui.equationAdd": "equationAdd"
  },
  equationAdd: function () {
    this.collection.add({})
  }
});


// #Application
//
// -----------------------------------------------------------------------------

// Application
// ===========
var Application = Backbone.Marionette.Application.extend({
  regions: {
    page: "#equationEditPage"
  },


  // Parameters:
  // -----------
  //
  // 1. `options` - object
  initialize: function (options) {},

  // Description:
  // ------------
  // 
  // Converts a raw object to a _FieldCollection_.
  //
  // NOTE: This function is defined as a closure.
  //
  // Parameters:
  // -----------
  //
  // 1. `obj` - object
  _toFieldCollection: function (obj) {
    var order = this.options.fields.order
      , self;

    list = _.map(order, function (item) {
      return {
        key: item,
        value: obj[item]
      };
    })

    return new FieldCollection(list);
  },

  // Description:
  //
  // Renders an edit form for the parsed JSON object returned from a call to the
  // dataset API.
  //
  // Parameters:
  // -----------
  //
  // 1. `dataset` - object
  renderDataset: function (dataset) {
    var datasetCollection = new DatasetCollection()
      , datasetCollectionView;

    _.each(dataset, function (value) {
      datasetCollection.add([{
        fields: this._toFieldCollection(value)
      }]);
    }, this)

    datasetCollectionView = new DatasetCollectionView({
      collection: datasetCollection,
      messages: this.options.messages,
      language: this.options.language
    });

    this.page.show(datasetCollectionView);  
  },
});

// #Routers
//
// -----------------------------------------------------------------------------

// Dataset Router
// ==============
//
// Defined Routes:
// ---------------
// * _data/sharing/datasets/:id/*params_ - Makes a call to the _datasets_ API
//    for the _id_ specified in the URL.
var DatasetRouter = Backbone.Router.extend({

  routes: {
    "data/sharing/datasets/:id/*params": "loadDataset"
  },

  // Parameters:
  // -----------
  //
  // 1. `id` - number
  // 2. `params` - string
  loadDataset: function (id, params) {
    // Make an asynch call to the datasets api for the id specified in the URL.
    $.ajax({
      url: "/api/v1/datasets/" + id + "/",
      data: {
        format: "json"
      },
      // Parameters:
      // -----------
      //
      // 1. `data` - object
      // 2. `textStatus` - string
      success: function (data, textStatus) {
        var dataset = JSON.parse(data.Data_as_json);

        (new Application(OPTIONS)).renderDataset(dataset);
      },
      dataType: "json"
    })
  }
});

// # Page Initialization
// 
// -----------------------------------------------------------------------------

// Set a jQuery domReady listener.
$(function () {
  // Initialize the router.
  var router = new DatasetRouter();

  // Initialize the Backbone.history handler using the page URL, this will make
  // the router trigger on page load.
  Backbone.history.start({pushState: true});
});