// Library for loading arbitrary modules, routes and widgets from a specified fixtures file (fixtures.js).

var Bootstrapper = {
    bootstrap: function() {
        /**
                                        *CALLED AUTOMATICALLY*
            Load fixtures from <<STATIC_ROOT>>/js/fixtures.js and register them with AngularJS on page load.
        **/

        angular.element(document).ready(function () { 
            Fixtures.widgets.map(function(widget) { Bootstrapper.register_widget(widget.name, widget.models, widget.template); });
            
            angular.bootstrap(angular.element(document).find('body'), Fixtures.modules);
        });
    }(),

    register_widget: function(name, models, html_template) {
        /**
            Register a widget that can be added to the DOM with a custom HTML tag. Widgets should be declared in a fixtures.js
            or by calling this function ( Bootstrapper.register_module() ).
            
            A widget is an HTML template and an optional set of models from the API that is fetched, compiled, and displayed when 
            specified on the DOM using an HTML tag of the widget's name (e.g. <widget-name></widget-name>).
            
            --> name - The name of the widget to register (and tag to render the widget on the DOM).
            --> models - A list of models (with optional filter and sort) to compile the template with, in the proper format for GET() (e.g. {'model': 'mymodel'} or 
                        {'model': 'mymodel', 'filter': 'name:model_name'}). Optional.
            --> html_template - The template to specify in the directive. Optional.
        **/
    
        var widget_module = angular.module(name + '-widget', []); // Widget module can be referenced as <<name>>-widget.
        
        widget_module.directive(name, function($http, $compile) { // Link the custom HTML tag to the widget renderer.
            return {
                restrict: 'E',
                template: html_template,
                link: function($scope, element) { Renderer.render_template($scope, $http, $compile, element, models, name); },
            };
        });

        Bootstrapper.register_module(widget_module.name);
    },

    register_module: function(name, create) { // TODO - ALLOW SERVICE INJECTION
        /**
            Register or create an AngularJS module to use in the application. Modules can be declared in any script included in the DOM but must be 
            registered in fixtures.js or by calling this function ( Bootstrapper.register_module() ) before they can be used.
            
            --> name - The name of the module to register.
            --> create - True if the module should be created as it is being registered. False (or null) if the module has
                         already been created.

            <-- AngularJS Module if a model was created. Otherwise null. 
        **/

        Fixtures.modules.push(name);

        if(create)
            return angular.module(name, []);
    }
};
