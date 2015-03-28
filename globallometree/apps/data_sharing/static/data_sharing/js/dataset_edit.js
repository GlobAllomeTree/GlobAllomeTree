// NOTE: This closure serves to keep the _window_ object tidy.
(function () {
  // # Application
  // ---------------------------------------------------------------------------

  // Application
  // ===========
  var Application = Backbone.Marionette.Application.extend({

    // Parameters:
    // -----------
    //
    // 1. `options` - object
    initialize: function (options) {
      // Initialize the router.
      new Application.routers.main();

      // Push the current page state onto the routers stack.
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

    // Description:
    // ------------
    //
    // Called from _AppRouter_ with string arguments corresponding to the named
    // route above.
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

  // Dataset Model
  // =============
  Application.models.dataset = Backbone.Model.extend({

    initialize: function () {
      window.dataset = this;

      this.on("change", function () {
        console.log(this.toJSON());
      })
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
      response.Data_as_json = new Application.collections.equation(
        response.Data_as_json,
        {parse: true}
      );

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
  Application.models.equation = Backbone.Model.extend({
  });

  // Field Model
  // ===========
  //
  // Description:
  // ------------
  //
  // This model acts as a base class for other field types it introduces
  // pre-validation and several validation routines.
  //
  // Each field has two attributes recorded the _name_ of the field and _value_.
  Application.models.field = Backbone.Model.extend({

    validations: [
      "nullable",
      "blank",
      "maxLength"
    ],

    // Description:
    // ------------
    //
    // Attaches `options` as a member of the instanced object.
    //
    // Parameters:
    // -----------
    //
    // 1. `attrs` - object
    // 2. `options` - object
    initialize: function (attrs, options) {
      this.options = options;
    },

    // Description:
    // ------------
    //
    // Validates if a field can be null.
    //
    // Parameters:
    // -----------
    //
    // 1. `value` - [any type]
    validateNullable: function (value) {
      if (! this.options.nullable && value === null) {
        return "Field cannot be null.";
      }
    },

    // Description:
    // ------------
    //
    // Validates if a field can be blank.
    //
    // Parameters:
    // -----------
    //
    // 1. `value` - [any type]
    validateBlank: function (value) {
      if (! this.options.blank && value === "") {
        return "Field cannot be blank.";
      }
    },

    // Description:
    // ------------
    //
    // Validates if a field meets its maxLength requirement.
    //
    // Parameters:
    // -----------
    //
    // 1. `value` - [any type]
    validateMaxLength: function (value) {
      if (value.length > this.options.maxLength) {
        return "Field cannot exceed maximum length of "+this.options.maxLength+".";
      }
    },

    // Description:
    // ------------
    //
    // Validates `value` against the choices list.
    //
    // Parameters:
    // -----------
    //
    // 1. `value` - [any type]
    validateChoices: function (value) {
      if (this.options.choices && ! _.contains(this.options.choices, value)) {
        return "Invalid option."
      }
    },

    // Description:
    // ------------
    //
    // Calls the validate methods indexed in _validations_.
    //
    // Parameters:
    // -----------
    //
    // 1. `attrs` - object
    // 2. `options` - object
    validate: function (attrs, options) {
      var value = attrs.value
        , i
        , methodName
        , out;

      for (i = 0; i < this.validations.length; i += 1) {
        methodName = "validate"
                   + this.validations[i].charAt(0).toUpperCase()
                   + this.validations[i].substring(1);

        out = this[methodName](value, options);
        if (out) break;
      }

      return out;
    }
    
  });

  // Char Field Model
  // ================
  //
  // NOTE: The word "char" has special meaning in Javascript which is why object
  //       literal syntax is not used here.
  Application.models.field["char"] = Application.models.field.extend({

  });

  // Decimal Field Model
  // ===================
  Application.models.field["decimal"] = Application.models.field.extend({

    validations: [
      "nullable",
      "blank",
      "numeric",
      "decimalPlaces",
      "maxDigits"
    ],

    // Parameters:
    // -----------
    //
    // 1. `value` - [any type]
    validateNumeric: function (value) {
      if (isNaN(value)) {
        return "Field must be a number."
      }
    },

    // Parameters:
    // -----------
    //
    // 1. `value` - [any type]
    validateDecimalPlaces: function (value) {
      var description = new RegExp("^([0-9]*\.)?[0-9]{0,"+this.options.decimalPlaces+"}$")

      if (
        this.options.decimalPlaces &&
        ! description.test(value)
      ) {
        return "Field can have a maximum of "
        + this.options.decimalPlaces
        + " decimal places."
      }
    },

    // Parameters:
    // -----------
    //
    // 1. `value` - [any type]
    validateMaxDigits: function (value) {
      var description = new RegExp("[^0-9]", "g")
        , max =  Number("1e"+(this.options.maxDigits - this.options.decimalPlaces || 0));

      if (this.options.maxDigits) {
        if(value.replace(description, "").length > this.options.maxDigits) {
          return "Field can have a maximum of "
          + this.options.maxDigits
          + " digits."
        }
        else if (Number(value) >= max) {
          return "Field must be less than "+max+".";
        }
      }
    },

    // Description:
    // ------------
    //
    // Convert the field _value_ to a number.
    get: function (key, options) {
      var value = Backbone.Model.prototype.get.call(this, key, options);

      return key === "value" ? Number(value): value;
    }

  });

  // Integer Field Model
  // ===================
  Application.models.field["integer"] = Application.models.field.extend({

  });

  // Null/Boolean Field Model
  // ========================
  Application.models.field["nullBoolean"] = Application.models.field.extend({
    
    validations: [
      "nullable",
      "blank",
      "choices"
    ],

    initialize: function (attrs, options) {
      this.options = options;
      this.options.choices = ["null", "false", "true"];
      this.options.nullable = true;
      this.options.blank = false;
    },

    // Description:
    // ------------
    //
    // Convert the field _value_ to a Javascript primitive (null, false, true).
    get: function (key, options) {
      var value = Backbone.Model.prototype.get.call(this, key, options);

      return key === "value" ? JSON.parse(value) : value;
    }
    
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

    // Description:
    // ------------
    //
    // Parse the _Data_as_json_ string from the dataset.
    //
    // Parameters:
    // -----------
    //
    // 1. `models` - array
    // 2. `options` - object
    parse: function (models, options) {
      this.add(JSON.parse(models));
    }
    
  });

  // Fields Collection
  // =================
  Application.collections.field = Backbone.Collection.extend({
    
    // Description:
    // ------------
    //
    // Sets the _model_ for the collection entry to the _type_
    model: function (attrs, options) {
      return new Application.models.field[options.type](attrs, options);
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

  // Field View
  // ==========
  Application.views.field = Backbone.Marionette.ItemView.extend({

    className: "form-group",
    tagName: "li",

    ui: {
      "valueField": "input"
    },

    events: {
      "change @ui.valueField": "valueFieldChange"
    },

    modelEvents: {
      "invalid": "showHelp"
    },

    // Description:
    // ------------
    //
    // Hides the field's help block.
    hideHelp: function (event) {
      this.$el.removeClass("has-error");
      this.$el.find(".help-block").text("");
    },

    // Description:
    // ------------
    //
    // Shows the field's help block with the current _validationError_.
    showHelp: function (event) {
      this.$el.addClass("has-error");
      this.$el.find(".help-block").text(this.model.validationError);
    },

    // Description:
    // ------------
    //
    // Updates the model with the value of the field from the user interface.
    valueFieldChange: function (event) {
      this.hideHelp();

      this.model.set("value", this.ui.valueField.val(), {validate: true});
    },

    templateHelpers: function () {
      var name = this.model.get("name");

      return {
        // Description:
        // ------------
        //
        // By default return the value of _name_ with underscores replaced by
        // whitespace
        label: this.model.options.label || name.replace(/_/g, " "),
        // Description:
        // ------------
        //
        // By default return the value of _name_
        id: this.model.options.id || _.uniqueId("field_")
      }
    }
  });

  // Char Field View
  // ===============
  Application.views.field["char"] = Application.views.field.extend({
    
    template: "#templateInput",

    events: {
      "change @ui.valueField": "valueFieldChange",
      "keyup @ui.valueField": "valueFieldChange"
    },

    ui: {
      "valueField": "input"
    }
  });

  // Char Field View
  // ===============
  Application.views.field["text"] = Application.views.field.extend({
    
    template: "#templateTextarea",

    ui: {
      "valueField": "input"
    }
  });

  // Integer Field View
  // ==================
  Application.views.field["integer"] = Application.views.field.extend({
    
    template: "#templateNumber",

    events: {
      "change @ui.valueField": "valueFieldChange",
      "keyup @ui.valueField": "valueFieldChange"
    },

    ui: {
      "valueField": "input"
    }

  });

  // Decimal Field View
  // ==================
  Application.views.field["decimal"] = Application.views.field.extend({
    
    template: "#templateInput",

    events: {
      "change @ui.valueField": "valueFieldChange",
      "keyup @ui.valueField": "valueFieldChange",
    },

    ui: {
      "valueField": "input"
    }

  });

  // NullBoolean Field View
  // ======================
  Application.views.field["nullBoolean"] = Application.views.field.extend({
    
    template: "#templateOption",
    
    ui: {
      "valueField": "select"
    },

    // Description:
    // ------------
    //
    // Assigns template variables on render.
    templateHelpers: function () {
      var helpers = Application.views.field.prototype.templateHelpers.call(this);

      helpers.options = [
        {label: "", value: null},
        {label: "No", value: false},
        {label: "Yes", value: true}
      ]

      return helpers;
    }

  });

  // Lookup Field View
  // =================
  Application.views.field.lookup = Application.views.field.extend({

    template: "#templateInput",

    ui: {
      "valueField": "input"
    }

  });

  // Field Group View
  // ================
  Application.views.field.group = Backbone.Marionette.CompositeView.extend({

    collectionEvents: {
      "change": "changeField"
    },
    
    initialize: function (options) {
      var i
        , field;

      this.collection = new Application.collections.field();

      for (i = 0; i < this.fields.length; i += 1) {
        field = this.fields[i];

        this.collection.add(
          { name: field.name, value: options.model.get(field.name)},
          field.options
        )
      }
    },
    
    // Parameters:
    // -----------
    //
    // 1. `child` - Backbone.Model
    getChildView: function (child) {
      if (typeof child.options.type === "string") {
        return Application.views.field[child.options.type];
      }
      else if (child.options.type instanceof Backbone.View) {

      }
    },

    changeField: function (model, options) {
      this.model.set(model.get("name"), model.get("value"));
    }
    
  });

  // Reference View
  // ==============
  Application.views.reference = Application.views.field.group.extend({

    template: "#templateModal",
    childViewContainer: "#equationModal",

    fields: [
      {name: "Label", options: {type: "char", maxLength: 20, nullable: true, blank: true}},
      {name: "Author", options: {type: "char", maxLength: 200, nullable: true, blank: true}},
      {name: "Year", options: {type: "char", maxLength: 12, nullable: true, blank: true}},
      {name: "Reference", options: {type: "text", nullable: true, blank: true}}
    ]
  });

  // Equation View
  // =============
  Application.views.equation = Application.views.field.group.extend({

    template: "#templateEquation",
    className: "panel panel-default",
    childViewContainer: "ul",
    
    fields: [
      {name: "X",                   options: {type: "char", maxLength: 20, nullable: true, blank: true}},
      {name: "Unit_X",              options: {type: "char", maxLength: 20, nullable: true, blank: true}},
      {name: "Z",                   options: {type: "char", maxLength: 20, nullable: true, blank: true}},
      {name: "Unit_Z",              options: {type: "char", maxLength: 20, nullable: true, blank: true}},
      {name: "W",                   options: {type: "char", maxLength: 20, nullable: true, blank: true}},
      {name: "Unit_W",              options: {type: "char", maxLength: 20, nullable: true, blank: true}},
      {name: "U",                   options: {type: "char", maxLength: 20, nullable: true, blank: true}},
      {name: "Unit_U",              options: {type: "char", maxLength: 20, nullable: true, blank: true}},
      {name: "V",                   options: {type: "char", maxLength: 20, nullable: true, blank: true}},
      {name: "Unit_V",              options: {type: "char", maxLength: 20, blank: true}},
      {name: "Min_X",               options: {type: "decimal", nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Max_X",               options: {type: "decimal", nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Min_Z",               options: {type: "decimal", nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Max_Z",               options: {type: "decimal", nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Output",              options: {type: "char", maxLength: 30, nullable: true}},
      {name: "Output_TR",           options: {type: "char", maxLength: 30, nullable: true, blank: true}},
      {name: "Unit_Y",              options: {type: "char", maxLength: 50, nullable: true, blank: true}},
      {name: "Age",                 options: {type: "char", maxLength: 50, nullable: true, blank: true}},
      {name: "Veg_Component",       options: {type: "char", maxLength: 150, nullable: true, blank: true, label: "Vegetation Component"}},
      {name: "B",                   options: {type: "nullBoolean", label: "B - Bark"}},
      {name: "Bd",                  options: {type: "nullBoolean", label: "Bd - Dead branches"}},
      {name: "Bg",                  options: {type: "nullBoolean", label: "Bg - Big branches"}},
      {name: "Bt",                  options: {type: "nullBoolean", label: "Bt - Thin branches"}},
      {name: "L",                   options: {type: "nullBoolean", label: "L - Leaves"}},
      {name: "Rb",                  options: {type: "nullBoolean", label: "Rb - Large roots"}},
      {name: "Rf",                  options: {type: "nullBoolean", label: "Rf - Fine roots"}},
      {name: "Rm",                  options: {type: "nullBoolean", label: "Rm - Medium roots"}},
      {name: "S",                   options: {type: "nullBoolean", label: "S - Stump"}},
      {name: "T",                   options: {type: "nullBoolean", label: "T - Trunks"}},
      {name: "F",                   options: {type: "nullBoolean", label: "F - Fruit"}},
      {name: "Equation",            options: {type: "char", maxlength: 500}},
      {name: "Substitute_equation", options: {type: "char", maxLength: 500, nullable: true, blank: true}},
      {name: "Top_dob",             options: {type: "decimal", nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Stump_height",        options: {type: "decimal", nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "R2",                  options: {type: "decimal", nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10, label: "R&sup2;"}},
      {name: "R2_Adjusted",         options: {type: "decimal", nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10, label: "R&sup2; Adjusted"}},
      {name: "RMSE",                options: {type: "decimal", nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10, label: "Root mean-square error"}},
      {name: "SEE",                 options: {type: "decimal", nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Corrected_for_bias",  options: {type: "nullBoolean"}},
      {name: "Bias_correction",     options: {type: "decimal", nullable: true, blank: true, maxDigits: 16, decimalPlaces: 10}},
      {name: "Ratio_equation",      options: {type: "nullBoolean"}},
      {name: "Segmented_equation",  options: {type: "nullBoolean"}},
      {name: "Sample_size",         options: {type: "char", maxLength: 150, nullable: true, blank: true}},
      {name: "Population",          options: {type: "lookup"}},
      {name: "Tree_type",           options: {type: "lookup"}}
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
    
    // User Interface Elements
    // -----------------------
    ui: {
      "equationAdd": "#equationAdd",
      "form": "form",
      "editField": ".editField"
    },
    
    // User Interface Events
    // ---------------------
    events: {
      "click @ui.equationAdd": "equationAdd",
      "submit @ui.form": "formSubmit",
      "click @ui.editField .read a": "fieldEdit",
      "click @ui.editField .edit a": "fieldSubmit"
    },


    // Collection Events
    // -----------------
    collectionEvents: {
      "change": "changeCollection"
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
    // ------------
    //
    // Clones the _Data\_as\_json_ collection and binds a change event listener
    // to the parent model.
    changeCollection: function (model, options) {
      var clone = model.collection.clone()
        , self = this;

      this.model.set("Data_as_json", clone);
      // NOTE: Neccesary call after changing the collection.
      this.model.listenToOnce(clone, "change", function () {
        // NOTE: Subsequent change events will call this function recursively.
        self.changeCollection.apply(self, arguments)
      });
    },
    
    // Description:
    //
    // This function is called when the "Add Equation" button element is
    // clicked.
    equationAdd: function () {
      this.collection.add({});
    },

    formSubmit: function () {
      this.model.save();
      return false;
    },

    fieldEdit: function (event) {
      var parent = $(event.target).closest(".editField")
        , input = parent.find("input")
        , length = input.val().length * 2;

      parent.find(".read").hide();
      parent.find(".edit").show();
      
      input.focus();
      input[0].setSelectionRange(length, length);
    },

    fieldSubmit: function (event) {
      var parent = $(event.target).closest(".editField")
        , input = parent.find("input")
        , field = parent.find(".field")
        , value = input.val();

      this.model.set(parent.data("field"), value);
      field.text(value);

      parent.find(".read").show();
      parent.find(".edit").hide();
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
    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
      var token;
      options.xhrFields = {
        withCredentials: true
      };
      token = getCookie('csrftoken');
      if (token) {
        return jqXHR.setRequestHeader('X-CSRFToken', token);
      }
    });

    new Application();
  });

}());