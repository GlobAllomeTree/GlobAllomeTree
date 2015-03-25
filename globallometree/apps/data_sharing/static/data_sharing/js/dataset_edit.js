// NOTE: This closure serves to keep the _window_ object tidy.
(function () {
  // # Application
  //
  // ---------------------------------------------------------------------------

  // Application
  // ===========
  var Application = Backbone.Marionette.Application.extend({

    // Parameters:
    // -----------
    //
    // 1. `options` - object
    initialize: function (options) {
      new Application.routers.main();

      Backbone.history.start({pushState: true});
    }

  });

  // Application.models
  // ==================
  Application.models = {};

  // Application.collections
  // =======================
  Application.collections = {};

  // Application.views
  // =================
  Application.views = {};

  // Application.routers
  // ===================
  Application.routers = {};

  // # Router
  // ---------------------------------------------------------------------------

  // Main Router
  // ===========
  Application.routers.main = Backbone.Marionette.AppRouter.extend({

    routes: {
      "data/sharing/datasets/:id/*params": "loadDataset"
    },

    loadDataset: function (id, params) {
      var dataset = new Application.models.dataset({id: id});

      dataset.fetch({
        success: function (model, response, options) {
          var layoutView = new Application.views.layout()
            , datasetView = new Application.views.dataset({model: model});

          layoutView.render();
          layoutView.showChildView("page", datasetView);
        }
      });
    }

  });

  // # Models
  // ---------------------------------------------------------------------------

  Application.models.base = Backbone.Model.extend({
    nest: function (key, value) {
      var self = this;

      this.listenToOnce(value, "change", function () {
        var clone = value.clone();
        self.set(key, clone);
        self.listenToOnce(clone, "change", arguments.callee);
      });
    }
  });

  // Dataset Model
  // =============
  Application.models.dataset = Application.models.base.extend({
    initialize: function () {
      this.on("change", function () {
        console.log(this.toJSON());
      })
      window.dataset = this;
    },
    "urlRoot": "/api/v1/datasets/",
    // Description:
    // ------------
    //
    // Appends a trailing forward slash to the URL so the request is not
    // redirected. Saves the application a round trip to the server.
    url: function () {
      return this.urlRoot + this.get("id") + "/";
    },
    // Description:
    // ------------
    //
    // Parses the JSON response from the server.
    //
    // Parameters:
    // -----------
    //
    // 1. `response` - object
    // 2. `options` - object
    parse: function (response, options) {
      var dataAsJson = JSON.parse(response.Data_as_json)
        , self = this;

      // Turn the _dataAsJson_ object into a collection.
      response.Data_as_json = new Application.collections.equation(dataAsJson);

      this.nest("Data_as_json", response.Data_as_json);

      return response;
    },
    // Description:
    // ------------
    //
    // Returns a JSON object to send the server.
    //
    // [Source](http://stackoverflow.com/questions/17050022/how-to-make-backbones-tojson-function-include-sub-models-and-collections)
    toJSON: function (options) {
      var json = _.clone(this.attributes)

      json.Data_as_json = this.get("Data_as_json").toJSON();

      return json;
    }
  });

  // Equation Model
  // ==============
  Application.models.equation = Application.models.base.extend({
  });

  // Field Model
  // ===========
  Application.models.field = Application.models.base.extend({
    initialize: function (attrs, options) {
      this.parentModel = options.parentModel;
      window.test = this
    },
    set: function (key, value, options) {
      if (key === "value") {
        this.parentModel.set(this.get("name"), value, options);
      }
      else {
        Backbone.Model.prototype.set.call(this, key, value, options);
      }
    }
  });

  // Char Field Model
  // ================
  Application.models.field.txt = Application.models.field.extend({

  });

  // Decimal Field Model
  // ===================
  Application.models.field.decimal = Application.models.field.extend({

  });

  // Integer Field Model
  // ===================
  Application.models.field.integer = Application.models.field.extend({

  });

  // Null/Boolean Field Model
  // ========================
  Application.models.field.nullBoo = Application.models.field.extend({

  });

  // Lookup Field Model
  // ==================
  Application.models.field.lookup = Application.models.field.extend({

  });


  // # Application Collections
  // ---------------------------------------------------------------------------

  // Equation Collection
  // ===================
  Application.collections.equation = Backbone.Collection.extend({
    model: Application.models.equation,
    toJSON: function () {
      return this.models.map(function (model) {
        return model.toJSON();
      });
    }
  });

  // Fields Collection
  // =================
  Application.collections.field = Backbone.Collection.extend({
    model: function (attrs, options) {
      return new Application.models.field[attrs.type](attrs, options);
    },
    validate: function () {
      var value = this.options.parentModel.get(this.get("name"));
      if (this.options.blank) {

      }
    },
    toJSON: function () {
      return this.models.map(function (model) {
        return model.toJSON();
      });
    }
  });

  // # Application Views
  // ---------------------------------------------------------------------------

  // Layout View
  // ===========
  Application.views.layout = Backbone.Marionette.LayoutView.extend({
    template: "#templateLayout",
    el: "#equationEdit",
    regions: {
      "modal": "#equationModal",
      "page": "#equationPage"
    }
  });

  Application.views.field = Backbone.Marionette.ItemView.extend({
    className: "form-group",
    tagName: "li",
    templateHelpers: function () {
      var name = this.model.get("name");

      return {
        // Description:
        // ------------
        //
        // By default return the value of _name_ with underscores replaced by
        // whitespace
        label: this.model.get("label") || name.replace(/_/g, " "),
        // Description:
        // ------------
        //
        // By default return the value of _name_
        id: this.model.get("id") || name,
        // Description:
        // ------------
        //
        // By default return an empty string
        value: this.options.parentModel.get(name) || ""
      }
    }
  });

  Application.views.field.txt = Application.views.field.extend({
    initialize: function (configuration, options) {
    },
    template: "#templateInput"
  });

  Application.views.field.integer = Application.views.field.extend({
    template: "#templateInput"
  });

  Application.views.field.decimal = Application.views.field.extend({
    template: "#templateInput"
  });

  Application.views.field.nullBoo = Application.views.field.extend({
    template: "#templateNullBoolean"
  });

  Application.views.field.lookup = Application.views.field.extend({
    template: "#templateInput"
  });

  Application.views.field.group = Backbone.Marionette.CompositeView.extend({
    initialize: function (options) {
      this.collection = new Application.collections.field(
        this.fields,
        this.childViewOptions()
      );
    },
    getChildView: function (child) {
      return Application.views.field[child.get("type")];
    },
    childViewOptions: function () {
      return {
        parentModel: this.model
      };
    }
  })

  // Equation View
  // =============
  Application.views.equation = Application.views.field.group.extend({
    template: "#templateEquation",
    className: "panel panel-default",
    childViewContainer: "ul",
    fields: [
      {name: "X",                   type: "txt",     options: {maxLength: 20, nullable: true, blank: true}},
      {name: "Unit_X",              type: "txt",     options: {maxLength: 20, nullable: true, blank: true}},
      {name: "Z",                   type: "txt",     options: {maxLength: 20, nullable: true, blank: true}},
      {name: "Unit_Z",              type: "txt",     options: {maxLength: 20, nullable: true, blank: true}},
      {name: "W",                   type: "txt",     options: {maxLength: 20, nullable: true, blank: true}},
      {name: "Unit_W",              type: "txt",     options: {maxLength: 20, nullable: true, blank: true}},
      {name: "U",                   type: "txt",     options: {maxLength: 20, nullable: true, blank: true}},
      {name: "Unit_U",              type: "txt",     options: {maxLength: 20, nullable: true, blank: true}},
      {name: "V",                   type: "txt",     options: {maxLength: 20, nullable: true, blank: true}},
      {name: "Unit_V",              type: "txt",     options: {maxLength: 20, blank: true}},
      {name: "Min_X",               type: "decimal", options: {nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Max_X",               type: "decimal", options: {nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Min_Z",               type: "decimal", options: {nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Max_Z",               type: "decimal", options: {nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Output",              type: "txt",     options: {maxLength: 30, nullable: true}},
      {name: "Output_TR",           type: "txt",     options: {maxLength: 30, nullable: true, blank: true}},
      {name: "Unit_Y",              type: "txt",     options: {maxLength: 50, nullable: true, blank: true}},
      {name: "Age",                 type: "txt",     options: {maxLength: 50, nullable: true, blank: true}},
      {name: "Veg_Component",       type: "txt",     options: {maxLength: 150, nullable: true, blank: true}},
      {name: "B",                   type: "nullBoo", options: {}},
      {name: "Bd",                  type: "nullBoo", options: {}},
      {name: "Bg",                  type: "nullBoo", options: {}},
      {name: "Bt",                  type: "nullBoo", options: {}},
      {name: "L",                   type: "nullBoo", options: {}},
      {name: "Rb",                  type: "nullBoo", options: {}},
      {name: "Rf",                  type: "nullBoo", options: {}},
      {name: "Rm",                  type: "nullBoo", options: {}},
      {name: "S",                   type: "nullBoo", options: {}},
      {name: "T",                   type: "nullBoo", options: {}},
      {name: "F",                   type: "nullBoo", options: {}},
      {name: "Equation",            type: "txt",     options: {maxlength: 500}},
      {name: "Substitute_equation", type: "txt",     options: {maxLength: 500, nullable: true, blank: true}},
      {name: "Top_dob",             type: "decimal", options: {nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Stump_height",        type: "decimal", options: {nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "R2",                  type: "decimal", options: {nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "R2_Adjusted",         type: "decimal", options: {nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "RMSE",                type: "decimal", options: {nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "SEE",                 type: "decimal", options: {nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Corrected_for_bias",  type: "nullBoo", options: {}},
      {name: "Bias_correction",     type: "decimal", options: {nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Ratio_equation",      type: "nullBoo", options: {}},
      {name: "Segmented_equation",  type: "nullBoo", options: {}},
      {name: "Sample_size",         type: "txt",     options: {maxLength: 150, nullable: true, blank: true}},
      {name: "Population",          type: "lookup",  options: {}},
      {name: "Tree_type",           type: "lookup",  options: {}}
    ],
    // Description:
    // ------------
    //
    // Sets some additional view variables.
    templateHelpers: function () {
      return {
        index: this.options.index,
        isExpanded: this.options.index === 0 ? "true" : "false"
      }
    }
  });

  // Dataset View
  // ============
  Application.views.dataset = Backbone.Marionette.CompositeView.extend({
    template: "#templateDataset",
    childView: Application.views.equation,
    childViewContainer: "#equations",
    ui: {
      "equationAdd": "#equationAdd"
    },
    events: {
      "click @ui.equationAdd": "equationAdd"
    },
    // Description:
    // ------------
    //
    // Initializes the view using the model specified by `options.model`
    //
    // Parameters:
    // -----------
    // 
    // 1. `options` - object
    initialize: function (options) {
      this.model = options.model;
      this.collection = this.model.get("Data_as_json");
    },
    // Description:
    //
    // This function is called when the "Add Equation" button element is
    // clicked.
    equationAdd: function () {
      this.collection.add({});
    },
    childViewOptions: function (model, index) {
      return {
        index: index,
        isExpanded: index === 0 ? "true" : "false"
      }
    }
  });

  // # Application Initialization
  // 
  // ---------------------------------------------------------------------------

  // Set a jQuery domReady listener which initializes the application.
  $(function () {
    new Application();
  });
}());