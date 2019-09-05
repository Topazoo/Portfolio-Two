function GET($http, params, callback, key) {
    /**
     *  Simplifies the boilerplate code necessary to send an AngularJS GET request to the server.
     *  IMPORTANT: Since requests are asynchronous, this function passes the returned response to a
     *  callback function when received and DOES NOT return the response.
     * 
     *  --> $http - The AngularJS HTTP serviced passed from the controller sending the request.
     *  --> params - A map of parameters to send with the request (e.g. {'model': 'mymodel'}).
     *  --> callback - The function to call when a response from the server is received. *The passed
     *                 callback function MUST specify a response parameter (e.g. func(response){})*.
     *  --> key - A dot seperated path to specify a partial chunk of the response to send to the callback 
     *            (e.g. 'model.name' to access the sub-value name of the value model in the response).
    **/

    $http({ url: '/api/',  method: "GET",  params: params })
    .then((! key) ? callback : function (response) { parse_response_closure(response, key, callback); });
}

function parse_response_closure(response, key, callback) {
    /**
     *  Handles parsing the JSON response for the specified value or sub-value.
     * 
     *  --> response - The raw JSON response from the server to parse.
     *  --> key - A dot seperated path to specify a partial chunk of the response to send to the callback 
     *            (e.g. 'models.0.name' to access the sub-value name of the first model in the response's array of models).
     *  --> callback - The function to call with the retreived chunk. *The passed
     *                 callback function MUST specify a response parameter (e.g. func(response){})*.
    **/

    key.split('.').forEach(function(path) { 
        response = (Array.isArray(response[path])) ? fix_json_list(response[path]) : response[path]; 
    });

    callback(response);
}

function fix_json_list(json_list) {
    /**
     *  Fixes nested JSON in lists (if it is in string form). Fixes occur on-demand by either calling this function
     *  with a list of JSON in string form, or when a parsing a response in parse_response_closure().
     * 
     *  --> json_list - A list of JSON in string form (e.g. [ "{"key1": "value1"}", "{"key2": "value2"}" ]).
     * 
     *  <-- List<Object> A list of containing the parsed JSON objects.
    **/

    try {
        return json_list.map(JSON.parse);
    } catch (e) { return json_list; }
}

function render_template($scope, $http, $compile, element, models, template) {
    /**
     *  Greatly simplifies rendering directives that include models from the API. Fetches all models
     *  from the API and a corresponding template, populates the template with the fetched data and adds it to 
     *  the specified DOM element.
     * 
     *  --> $scope - The scope passed from the directive link function.
     *  --> $http - The http service passed from the directive link function.
     *  --> $compile - The compile service passed from the directive link function.
     *  --> element - The DOM element to add the template to. Passed from the directive link function.
     *  --> models - A list of models to compile the template with, in the proper format for GET() (e.g. {'model': 'mymodel'} or 
     *              {'model': 'mymodel', 'filter': 'name:model_name'}). Optional.
     *  --> template - The name of the template to load (excluding the extension).
    **/

    if(models.length > 0)
        GET(
            $http, 
            models[0], 
            function (response) {
                $scope[models[0].model] = response; 
                render_template($scope, $http, $compile, element, models.slice(1), template); 
            }, 
            'data.models'
        );
    else
        GET(
            $http,
            {'model': 'widget', 'filter': 'name:' + template},
            function(template) { 
                element.append($compile(template)($scope)); 
            },
            'data.models.0.template'
        );
}

function widget_directive_factory(name, models, html_template) {
    /**
     *  Greatly simplifies creating a directive that uses a template and models fetched from the API
     *  to build a piece of the DOM.
     * 
     *  --> name - The name of the widget (must also be the name of the template).
     *  --> models - A list of models to compile the template with, in the proper format for GET() (e.g. {'model': 'mymodel'} or 
     *              {'model': 'mymodel', 'filter': 'name:model_name'}). Optional.
     *  --> html_template - The template to specify in the directive.
    **/

    var widgetModule = angular.module(name.charAt(0).toUpperCase() + name.slice(1) +  'WidgetModule', []);

    widgetModule.directive(name, function($http, $compile) {
        return {
            restrict: 'E',
            template: html_template,
            link: function($scope, element) { render_template($scope, $http, $compile, element, models, name); },
        };
    });
}
