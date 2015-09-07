// NOTE: This closure serves to keep the _window_ object tidy.
(function () {
  // #  Application
  var Application = Backbone.Marionette.Application.extend({

    // **Parameters:**
    //
    // 1. `options` - object
    initialize: function (options) {
      // Initialize the router.
      new Application.routers.main();

      // Push the current page state onto the routers stack.
      Backbone.history.start({pushState: true});
    }

  });

  // ###  Aplication.events
  //
  // **Description:**
  //
  // A global event listener which enables messaging between the different parts
  // of the application.  This is primarily useful for messaging between
  // nested views.
  //
  // NOTE: This is an instantiated object and the only non-compartmentalized
  //       entry of _Application_.
  Application.events = _.extend({}, Backbone.Events);


  // ###  Application.timers:
  //
  // **Description:**
  //
  // Stores timers used in the application.
  //
  // Timers:
  //
  // * save
  Application.timers = {};

  // ###  Application.models
  Application.models = {};

  // ###  Application.collections
  Application.collections = {};

  // ###  Application.views
  Application.views = {};

  // ###  Application.routers
  Application.routers = {};

  // ## Router
  // ---------------------------------------------------------------------------

  // ###  Main Router
  Application.routers.main = Backbone.Marionette.AppRouter.extend({

    routes: {
      "data/sharing/datasets/:id/*params": "loadDataset"
    },

    // **Description:**
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

  // ## Models
  // ---------------------------------------------------------------------------


  // ###  Base Model
  Application.models.base = Backbone.Model.extend({

    // **Description:**
    //
    // Stores _options_ passed to initialize.
    initialize: function (attrs, options) {
      this.options = options;
    },

  });

// ###  Dataset Model
  //
  // **Description:**
  //
  // A model containing the entire dataset which syncs with the server via
  // calls to _save_.
  Application.models.dataset = Backbone.Model.extend({

    "urlRoot": "/api/v1/datasets/",

    initialize: function (attrs, options) {
      var self = this;

      // TODO: Remove this debugging code.
      this.on("change", function () {
        console.log(this.toJSON());
      });

      this.once("sync", function () {
        self.on("sync", function () {
          Application.events.trigger("alert", "success", "Saved Dataset.");

          self.setSaveTimer();
        });

        self.setSaveTimer();
      });
    },

    setSaveTimer: function () {
      var self = this;

      if (Application.timers.save) {
        window.clearTimeout(Application.timers.save);
        delete Application.timers.save;
      }

      Application.timers.save = window.setTimeout(function () {
        self.save();
      }, 60000);
    },
      
    // **Description:**
    //
    // Appends a trailing forward slash to the URL so the request is not
    // redirected. Saves the application a round trip to the server.
    url: function () {
      return this.urlRoot + this.get("id") + "/";
    },
      
    // **Description:**
    //
    // Parses the JSON response from the server.
    //
    // **Parameters:**
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
      
    // **Description:**
    //
    // Returns a JSON object to send the server.
    //
    // [Source](http://stackoverflow.com/questions/17050022/how-to-make-backbones-tojson-function-include-sub-models-and-collections)
    toJSON: function (options) {
      var json = _.clone(this.attributes)

      json.Data_as_json = JSON.stringify(this.get("Data_as_json").toJSON());

      return json;
    }
      
  });

  // ###  Field Model
  //
  // Inherits:
  // 
  // Application.models.base
  //
  // **Description:**
  //
  // This model acts as a base class for other field types it introduces
  // pre-validation and several validation routines.
  //
  // Each field has two attributes recorded the _name_ of the field and _value_.
  Application.models.field = Application.models.base.extend({

    validations: [
      "nullable",
      "blank",
      "maxLength"
    ],

    // **Description:**
    //
    // Validates if a field can be null.
    //
    // **Parameters:**
    //
    // 1. `value` - [any type]
    validateNullable: function (value) {
      if (! this.options.nullable && value === null) {
        return "Field cannot be null.";
      }
    },

    // **Description:**
    //
    // Validates if a field can be blank.
    //
    // **Parameters:**
    //
    // 1. `value` - [any type]
    validateBlank: function (value) {
      if (! this.options.blank && value === "") {
        return "Field cannot be blank.";
      }
    },

    // **Description:**
    //
    // Validates if a field meets its maxLength requirement.
    //
    // **Parameters:**
    //
    // 1. `value` - [any type]
    validateMaxLength: function (value) {
      if (value.length > this.options.maxLength) {
        return "Field cannot exceed maximum length of "+this.options.maxLength+".";
      }
    },

    // **Description:**
    //
    // Validates `value` against the choices list.
    //
    // **Parameters:**
    //
    // 1. `value` - [any type]
    validateChoices: function (value) {
      if (this.options.choices && ! _.contains(this.options.choices, value)) {
        return "Invalid option."
      }
    },

    // **Description:**
    //
    // Calls the validate methods indexed in _validations_.
    //
    // **Parameters:**
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

  // ###  Char Field Model
  //
  // NOTE: The word "char" has special meaning in Javascript which is why object
  //       literal syntax is not used here.
  Application.models.field["char"] = Application.models.field.extend({

  });

  // ###  Decimal Field Model
  Application.models.field["decimal"] = Application.models.field.extend({

    validations: [
      "nullable",
      "blank",
      "numeric",
      "decimalPlaces",
      "maxDigits"
    ],

    // **Parameters:**
    //
    // 1. `value` - [any type]
    validateNumeric: function (value) {
      if (isNaN(value)) {
        return "Field must be a number."
      }
    },

    // **Parameters:**
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

    // **Parameters:**
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

    // **Description:**
    //
    // Convert the field _value_ to a number.
    get: function (key, options) {
      var value = Backbone.Model.prototype.get.call(this, key, options);

      return key === "value" ? Number(value): value;
    }

  });

  // ###  Integer Field Model
  Application.models.field["integer"] = Application.models.field.extend({

  });

  // Null-Boolean Field Model
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

    // **Description:**
    //
    // Convert the field _value_ to a Javascript primitive (null, false, true).
    get: function (key, options) {
      var value = Backbone.Model.prototype.get.call(this, key, options);

      return key === "value" ? JSON.parse(value) : value;
    }
    
  });

  // Biome-FAO Field Model
  Application.models.field["ajaxSelect"] = Application.models.field.extend({

    validations: [
      "nullable",
      "blank",
      "choices"
    ],

    initialize: function (attrs, options) {
      var self = this;

      this.options = options;
      this.options.nullable = true;
      this.options.blank = false;

      $.ajax(this.options.url, {
        data: {
          format: "json",
          limit: 500
        },
        success: function (result) {
          self.options.choices = _.pluck(result.results, "Name")
        },
        dataType: "json"
      });
    }

  });

  // ###  Lookup Field Model
  //
  // **Description:**
  //
  // Not used at the moment would theoretically act as a mixin for fields
  // which need auto-complete with the server.
  //
  Application.models.field.lookup = Application.models.field.extend({
  });

  // ###  Reference Well Model
  Application.models.field.referenceWell = Application.models.base.extend({

    defaults: {
      value: {}
    }

  });

  // ###  Species Detail Model
  Application.models.field.speciesDetail = Application.models.base.extend({

    defaults: {
      value: [{}]
    }

  });

  // ###  Location Detail Model
  Application.models.field.locationDetail = Application.models.base.extend({

    defaults: {
      value: [{}]
    }

  });

  // ###  Species Model
  Application.models.species = Application.models.base.extend({

  });

  // ###  Location Model
  Application.models.location = Application.models.base.extend({

  });


  // ## Application Collections
  // ---------------------------------------------------------------------------

  // ###  Equation Collection
  Application.collections.equation = Backbone.Collection.extend({

    // **Description:**
    //
    // Parse the _Data_as_json_ string from the dataset.
    //
    // **Parameters:**
    //
    // 1. `models` - array
    // 2. `options` - object
    parse: function (models, options) {
      this.add(JSON.parse(models));
    }
    
  });

  // ###  Species Collection
  Application.collections.species = Backbone.Collection.extend({

    model: Application.models.species

  });

  // ###  Location Collection
  Application.collections.location = Backbone.Collection.extend({

    model: Application.models.location

  });

  // ###  Fields Collection
  Application.collections.field = Backbone.Collection.extend({
    
    // **Description:**
    //
    // Sets the _model_ for the collection entry to the _type_
    model: function (attrs, options) {
      return new Application.models.field[options.type](attrs, options);
    }

  });

  // ## Application Views
  // ---------------------------------------------------------------------------

  // ###  Layout View
  Application.views.layout = Backbone.Marionette.LayoutView.extend({

    template: "#templateLayout",
    el: "#equationEdit",

    regions: {
      "modal": "#equationModal",
      "page": "#equationPage"
    }

  });

  // ###  Field View
  //
  // **Description:**
  //
  // This view is inherited by other subsquent field views.
  Application.views.field = Backbone.Marionette.ItemView.extend({

    className: "form-group row",
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

    // **Description:**
    //
    // Hides the field's help block.
    hideHelp: function (event) {
      this.$el.removeClass("has-error");
      this.$el.find(".help-block").text("");
    },

    // **Description:**
    //
    // Shows the field's help block with the current _validationError_.
    showHelp: function (event) {
      this.$el.addClass("has-error");
      this.$el.find(".help-block").text(this.model.validationError);
    },

    // **Description:**
    //
    // Updates the model with the value of the field from the user interface.
    valueFieldChange: function (event) {
      this.hideHelp();

      this.model.set("value", this.ui.valueField.val(), {validate: true});
    },

    templateHelpers: function () {
      var name = this.model.get("name");

      return {
        // **Description:**
        //
        // By default return the value of _name_ with underscores replaced by
        // whitespace
        label: this.model.options.label || name.replace(/_/g, " "),
        // **Description:**
        //
        // By default return the value of _name_
        id: this.model.options.id || _.uniqueId("field_")
      }
    }
  });

  // ###  Char Field View
  //
  // Inherits:
  //
  // Application.views.field
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

  // ###  Char Field View
  //
  // Inherits:
  //
  // Application.views.field
  Application.views.field["text"] = Application.views.field.extend({
    
    template: "#templateTextarea",

    ui: {
      "valueField": "input"
    }
  });

  // ###  Integer Field View
  //
  // Inherits:
  //
  // Application.views.field
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

  // ###  Decimal Field View
  //
  // Inherits:
  //
  // Application.views.field
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

  // ###  NullBoolean Field View
  //
  // Inherits:
  //
  // Application.views.field
  Application.views.field["nullBoolean"] = Application.views.field.extend({
    
    template: "#templateOption",
    
    ui: {
      "valueField": "select"
    },

    // **Description:**
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

  Application.views.field["ajaxSelect"] = Application.views.field.extend({

    template: "#templateOption",
    
    ui: {
      "valueField": "select"
    },

    onRender: function () {
      var target = this.$el.find("select")
        , value = this.model.get("value");

      $.ajax(this.model.options.url, {
        data: {
          format: "json",
          limit: 500
        },
        success: function (result) {
          _.each(result.results, function (field) {
            var selected = (field.Name === value) ? "selected=\"selected\"" : "";
            target.append("<option value=\""+field.Name+"\" "+selected+">"+field.Name+"</option>");
          });
        },
        dataType: "json"
      });
    },

    // **Description:**
    //
    // Assigns template variables on render.
    templateHelpers: function () {
      var helpers = Application.views.field.prototype.templateHelpers.call(this);

      // Initialize with one _blank_ option.
      helpers.options = [
        {label: "", value: ""}
      ]

      return helpers;
    }

  });

  // ###  Lookup Field View
  //
  // Inherits:
  //
  // Application.views.field
  Application.views.field["lookup"] = Application.views.field.extend({

    template: "#templateInput",

    ui: {
      "valueField": "input"
    },



  });

  // ###  Field Group View
  //
  // Inherits:
  //
  // Backbone.Marionette.CompositeView
  //
  // **Description:**
  //
  // A group of fields assembled together in a list.
  Application.views.field.group = Backbone.Marionette.CompositeView.extend({

    childViewContainer: "ul",

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
    
    // **Description:**
    //
    // Return the corresponding entry from
    // _Application.views.field[child.options.type]_.
    //
    // **Parameters:**
    //
    // 1. `child` - Backbone.Model
    getChildView: function (child) {
      return Application.views.field[child.options.type];
    },

    // **Description:**
    //
    // Event listener which fires when any field in the collection is changed.
    // Updates the parent model's named attribute with the field's value.
    changeField: function (childModel, options) {
      if (childModel) {
        var name = childModel.get("name")
          , value = childModel.get("value");

        this.model.set(name, value);
      }
    }
    
  });

  // ###  Modal Group View

  // ###  Nested Form Group View
  Application.views.field.group.well = Application.views.field.group.extend({

    template: "#templateWell"

  });

  // ###  Species Group View
  Application.views.field.detail = Backbone.Marionette.ItemView.extend({

    template: "#templateDetail",
    tagName: "li"

  });

  Application.views.field.speciesDetail = Application.views.field.detail.extend({

    ui: {
      "add": ".add"
    },

    events: {
      "click @ui.add": "uiAdd"
    },

    templateHelpers: function () {
      var value = this.model.get("value")
        , description;

      if (value.length > 0) {
        description = _.pluck(value, "Scientific_name").join(", ")
      }

      description = description || "Choose from one of the options below to add a species group";

      return {
        title: "Species Group",
        description: description
      }
    },

    uiAdd: function () {
      var fieldGroup = new Application.views.speciesGroup({
        model: this.model
      });

      fieldGroup.render();
      var modalEl = $("#equationModal .modal");
      modalEl.html(fieldGroup.el);
      modalEl.modal("show")
    }

  });

  Application.views.field.locationDetail = Application.views.field.detail.extend({

    ui: {
      "add": ".add"
    },

    events: {
      "click @ui.add": "uiAdd"
    },

    templateHelpers: function () {
      var value = this.model.get("value")
        , description;

      if (value.length > 0) {
        description = _.pluck(value, "Country").join(", ")
      }

      description = description || "Choose from one of the options below to add a location group";

      return {
        title: "Location Group",
        description: description
      }
    },

    uiAdd: function () {
      var fieldGroup = new Application.views.locationGroup({
        model: this.model
      });

      fieldGroup.render();
      var modalEl = $("#equationModal .modal");
      modalEl.html(fieldGroup.el);
      modalEl.modal("show")
    }

  });

  // ###  Modal Form Group View
  Application.views.modal = Backbone.Marionette.CompositeView.extend({

    template: "#templateModal",

    childViewContainer: ".panel-group",

    ui: {
      "remove": ".remove",
      "add": ".modal-footer .add"
    },

    // Collection Events:
    collectionEvents: {
      "change": "collectionChange",
      "remove": "collectionRemove"
    },

    events: {
      "click @ui.remove": "uiRemove",
      "click @ui.add": "uiAdd"
    },

    // **Description:**
    //
    // Updates the parent model's _value_ attribute using _\_.clone_ which
    // causes will trigger the change event of parent _models_ and
    // _collections_.
    //
    // For more information see this
    // [blog post](http://www.crittercism.com/blog/nested-attributes-in-backbone-js-models)
    // .
    collectionChange: function (childModel, options) {
      this.model.set("value", this.collection.toJSON());
      this.model.trigger("change");
    },

    collectionRemove: function () {
      this.render();
    },

    templateHelpers: function () {
      var helpers = {};

      helpers.footer = _.template($("#templateModalFormButtons").html())();

      return helpers;
    },

    uiAdd: function (event) {
      this.collection.add({});
    },

    // **Description:**
    //
    // Removes the equation when clicked.
    uiRemove: function (event) {
      var element = $(event.currentTarget)
        , index = element.data("index");

      this.collection.remove(this.collection.at(element.data("index")));

      return false;
    },

    // **Parameters:**
    //
    // 1. `model` - object
    // 2. `index` - numbers
    childViewOptions: function (model, index) {
      return {
        prefix: "species",
        index: index,
        isExpanded: index === 0 ? true : false
      }
    }

  });

  // ###  Reference View
  //
  // **Description:**
  //
  // Manipulates a model with the following attributes.  The attibute _value_
  // is itself an object. Marionette does not set listeners recursively for
  // for nested objects so we have to do some extra work to trigger the
  // parent model's `change` event.
  //
  // {
  //   name: "Reference",
  //   value: {
  //     "Label": "...",
  //     "Author": "...",
  //     "Year": "..."
  //     ""
  //   }
  // }
  Application.views.field.referenceWell = Application.views.field.group.well.extend({

    tagName: "li",

    initialize: function (options) {
      var i
        , field
        , values = options.model.get("value") || {}

      this.collection = new Application.collections.field();

      for (i = 0; i < this.fields.length; i += 1) {
        field = this.fields[i];

        this.collection.add(
          { name: field.name, value: values[field.name]},
          field.options
        )
      }
    },

    fields: [
      {name: "Label", options: {type: "char", maxLength: 20, nullable: true, blank: true}},
      {name: "Author", options: {type: "char", maxLength: 200, nullable: true, blank: true}},
      {name: "Year", options: {type: "char", maxLength: 12, nullable: true, blank: true}},
      {name: "Reference", options: {type: "char", nullable: true, blank: true}}
    ],

    // **Description:**
    //
    // Updates the parent model's _value_ attribute using _\_.clone_ which
    // causes will trigger the change event of parent _models_ and
    // _collections_.
    //
    // For more information see this
    // [blog post](http://www.crittercism.com/blog/nested-attributes-in-backbone-js-models)
    // .
    changeField: function (childModel, options) {
      // Get a reference to 
      var clone = _.clone(this.model.get("value"))
      clone[childModel.get("name")] = childModel.get("value");
      this.model.set("value", clone);
    }

  });

  // ### Modal Field Group View
  Application.views.field.group.modal = Application.views.field.group.extend({

    ui: {
      "title": ".modal-title"
    },

    template: "#templateFieldGroup",
    className: "panel panel-default",

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
    }

  });

  // ###  Species View
  Application.views.species = Application.views.field.group.modal.extend({

    modelEvents: {
      "change:Family change:Species change:Species": "modelChangeTitle"
    },

    fields: [
      {name: "Family",                 options: {type: "char", maxLength: 80}},
      {name: "Genus",                  options: {type: "char", maxLength: 80}},
      {name: "Species",                options: {type: "char", maxLength: 80}},
      {name: "Species_local_names",    options: {type: "char", maxLength: 80, label: "Species local names"}},
      {name: "Subspecies",             options: {type: "char", maxLength: 80}}
    ],

    // **Description:**
    //
    // Sets some additional view variables.
    templateHelpers: function () {
      var name = this.model.get("Scientific_name")
        , heading = name || "Species "+(this.options.index + 1);

      return {
        heading: heading,
        prefix: this.options.prefix,
        index: this.options.index,
        isExpanded: this.options.index === 0 ? true : false
      }
    },

    modelChangeTitle: function () {
      var title = ""
                + this.model.get("Family") + " "
                + this.model.get("Genus") + " "
                + this.model.get("Species")

      this.ui.title.html($("em").text(title));
    }

  });

  // ###  Location View
  Application.views.location = Application.views.field.group.modal.extend({

    modelEvents: {
      "change:Continent change:Country": "modelChangeTitle"
    },

    fields: [
      {name: "Location_name",   options: {type: "char", maxLength: 255, nullable: true, blank: true, label: "Location name"}},
      {name: "Region",          options: {type: "char", maxLength: 255, blank: true, nullable: true}},
      {name: "Country",         options: {type: "ajaxSelect", url: "/api/v1/countries/" }},
      {name: "Zone_FAO",       options: {type: "ajaxSelect", url: "/api/v1/biomes-fao/", blank: true, nullable: true, label: "Biome (FAO)"}},
      {name: "Ecoregion_Udvardy",   options: {type: "ajaxSelect", url: "/api/v1/biomes-udvardy", blank: true, nullable: true, label: "Biome (UDVARDY)"}},
      {name: "Ecoregion_WWF",       options: {type: "ajaxSelect", url: "/api/v1/biomes-wwf", blank: true, nullable: true, label: "Biome (WWF)"}},
      {name: "Division_BAILEY", options: {type: "ajaxSelect", url: "/api/v1/divisions-bailey/", blank: true, nullable: true, label: "Division (BAILEY)"}},
      {name: "Zone_Holdridge", options: {type: "char", blank: true, nullable: true, label: "Biome (HOLDRIDGE)"}},
      {name: "Vegetation_type",     options: {type: "char", maxLength: 255, nullable: true, blank: true, label: "Forest type"}},
    ],

    // **Description:**
    //
    // Sets some additional view variables.
    templateHelpers: function () {
      var equation = this.model.get("Equation")
        , heading = equation || "Location "+(this.options.index + 1);

      return {
        heading: heading,
        prefix: this.options.prefix,
        index: this.options.index,
        isExpanded: this.options.index === 0 ? true : false
      }
    },

    modelChangeTitle: function () {
      var title = ""
                + this.model.get("Continent") + " "
                + this.model.get("Country")

      this.ui.title.text(title);
    }

  });

  Application.views.speciesGroup = Application.views.modal.extend({
    
    childView: Application.views.species,

    initialize: function (options) {
      this.model = options.model;
      this.collection = new Application.collections.species(this.model.get("value"));
    },

    templateHelpers: function () {
      var helpers = Application.views.modal.prototype.templateHelpers.call(this);

      helpers.title = "Species Group";

      return helpers;
    },


    // **Parameters:**
    //
    // 1. `model` - object
    // 2. `index` - numbers
    childViewOptions: function (model, index) {
      return {
        prefix: "species",
        index: index,
        isExpanded: index === 0 ? true : false
      }
    }

  });

  Application.views.locationGroup = Application.views.modal.extend({
    
    childView: Application.views.location,

    initialize: function (options) {
      this.model = options.model
      this.collection = new Application.collections.location(this.model.get("value"))
    },

    templateHelpers: function () {
      var helpers = Application.views.modal.prototype.templateHelpers.call(this);

      helpers.title = "Location Group"

      return helpers;
    },

    // **Parameters:**
    //
    // 1. `model` - object
    // 2. `index` - numbers
    childViewOptions: function (model, index) {
      return {
        prefix: "location",
        index: index,
        isExpanded: index === 0 ? true : false
      }

    }

  });

  // ###  Equation View
  Application.views.equation = Application.views.field.group.extend({

    template: "#templateFieldGroup",
    className: "panel panel-default",

    ui: {
      "heading": ".panel-heading h3 a"
    },

    modelEvents: {
      "change:Equation": "modelChangeEquation"
    },

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
      {name: "Tree_type",           options: {type: "lookup"}},
      {name: "Reference",           options: {type: "referenceWell"}},
      {name: "Species_group",       options: {type: "speciesDetail"}},
      {name: "Location_group",      options: {type: "locationDetail"}}
    ],

    // **Description:**
    //
    // Changes the _title_ of the corresponding child view's panel.
    modelChangeEquation: function(model, options) {
      this.ui.heading.text(model.get("Equation"));
    },

    
    // **Description:**
    //
    // Sets some additional view variables.
    templateHelpers: function () {
      var equation = this.model.get("Equation")
        , heading = equation || "Equation "+(this.options.index + 1);

      return {
        heading: heading,
        prefix: this.options.prefix,
        index: this.options.index,
        isExpanded: this.options.index === 0 ? true : false
      }
    }
    
  });

// ###  Dataset View
  Application.views.dataset = Backbone.Marionette.CompositeView.extend({
    
    template: "#templateDataset",
    childView: Application.views.equation,
    childViewContainer: "#equations",
    
    // User Interface Elements
    ui: {
      "equationAdd": "#equationAdd",
      "form": "form",
      "editField": ".editField",
      "equationRemove": ".remove",
      "equationAlert": "#equationAlert"
    },
    
    // User Interface Events
    events: {
      "click @ui.equationAdd": "uiEquationAdd",
      "submit @ui.form": "uiFormSubmit",
      "click @ui.editField .read a": "uiFieldEdit",
      "click @ui.editField .edit a": "uiFieldSubmit",
      "click @ui.equationRemove": "uiEquationRemove"
    },

    // Collection Events
    collectionEvents: {
      "change": "collectionChange",
      "remove": "collectionRemove"
    },
    
    // **Description:**
    //
    // Initializes the view using the model specified by `options.model`
    //
    // **Parameters:**
    // 
    // 1. `options` - object
    initialize: function (options) {
      this.model = options.model;
      this.collection = this.model.get("Data_as_json");

      // Bind a listener to _alert_ events triggered on the
      // _Application.events_ object.
      Application.events.on("alert", this.alert, this);
    },

    // **Description:**
    //
    // Constructs a dismissable alert
    alert: function (type, msg) {
      var element = $("<div>");

      this.ui.equationAlert.empty();

      element
        .addClass("alert")
        .addClass("alert-"+type)
        .attr("role", "alert")
        .text(msg)
        .appendTo(this.ui.equationAlert)

      // Show the alert for two seconds then close.
      element
        .delay(2000)
        .slideUp(200, function () { $(this).alert("close"); });
    },

    // **Description:**
    //
    // Clones the _Data\_as\_json_ collection and binds a change event listener
    // to the parent model.
    collectionChange: function (model, options) {
      this.model.trigger("change");
    },

    collectionRemove: function () {
      this.render()
    },
    
    // **Description:**
    //
    // This function is called when the "Add Equation" button element is
    // clicked.
    //
    // TODO: Find out why this is not firing.
    uiEquationAdd: function () {
      this.collection.add({});
      this.$el.find(".panel:last").collapse("show");
    },

    // **Description:**
    //
    // Removes the equation when clicked.
    uiEquationRemove: function (event) {
      var element = $(event.currentTarget)
        , index = element.data("index");

      this.collection.remove(this.collection.at(element.data("index")));
    },

    uiFormSubmit: function () {
      this.ui.editField.find(".edit a").trigger("click");

      this.model.save();
      return false;
    },

    // **Description:**
    //
    // Shows the input elements for the _Title_ and _Description_ fields.
    uiFieldEdit: function (event) {
      var parent = $(event.target).closest(".editField")
        , input = parent.find("input")
        , length = input.val().length * 2;

      parent.find(".read").hide();
      parent.find(".edit").show();
      
      input.focus();
      input[0].setSelectionRange(length, length);
    },

    // **Description:**
    //
    // Saves the values of the _Title_ and _Description_ fields.
    uiFieldSubmit: function (event) {
      var parent = $(event.target).closest(".editField")
        , input = parent.find("input")
        , field = parent.find(".field")
        , value = input.val();

      this.model.set(parent.data("field"), value);
      field.text(value);

      parent.find(".read").show();
      parent.find(".edit").hide();
    },
    
    // **Parameters:**
    //
    // 1. `model` - object
    // 2. `index` - numbers
    childViewOptions: function (model, index) {
      return {
        prefix: "equations",
        index: index,
        isExpanded: index === 0 ? "true" : "false"
      }
    }
    
  });


  // ## Application Initialization
  // 
  // ---------------------------------------------------------------------------

  // Set a jQuery domReady listener which initializes the application.
  $(function () {
    // **Description:**
    //
    // Parses cookie components.
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

    // Prepends the CSRFToken to the headers of any subsequent jqXHR requests.
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