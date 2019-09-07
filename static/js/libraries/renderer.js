// Library for rendering widgets.

var Renderer = {
    render_template: function($scope, $http, $compile, element, models, template) {
        /**
         *  Fetch a template and models from the API. Compile the template with the fetched data and add it to 
         *  the passed DOM element.
         * 
         *  --> $scope - The scope passed from the directive link function.
         *  --> $http - The http service passed from the directive link function.
         *  --> $compile - The compile service passed from the directive link function.
         *  --> element - The DOM element to add the template to. Passed from the directive link function.
         *  --> models - A list of models to compile the template with, in the proper format for GET() (e.g. {'model': 'mymodel'} or 
         *              {'model': 'mymodel', 'filter': 'name:model_name'}). Optional.
         *  --> template - The name of the template to load (excluding the extension).
        **/
    
        if(models && models.length > 0) // Since API.GET runs asynchronously, recurse to get all models from the API using API.GET's optional
            API.GET(                    // callback.
                $http, 
                models[0], 
                function(response) {
                    $scope[models[0].model] = response; 
                    Renderer.render_template($scope, $http, $compile, element, models.slice(1), template); 
                }, 
                'data.models'
            );
        else                            // The final recursive call (after all models are retrieved) compiles and displays the widget.
            API.GET(
                $http,
                {'model': 'widget', 'filter': 'name:' + template},
                function(template) { 
                    element.append($compile(template)($scope));
                },
                'data.models.0.template'
            );
    }
};


