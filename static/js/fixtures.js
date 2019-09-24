/**
    FIXTURE SPECIFICS
        modules
            Custom Angular modules defined in any script included in the DOM should be
            registered here. This allows any number of modules to be mixed and matched.
        

        widgets
            Templates to compile with (optional) models from the API. Registered widgets
            can be added to the DOM using a specified tag (e.g. <widget-name></widget-name>).

        routes
            Routes and associated pages to be used by ngRoute in Single Page Applications.
**/

var Fixtures = {

    modules: [
        'Animation_Library'
    ],

    widgets: [ 
    /* 
        {
            name:               The name to use for the widget (and the html tag that renders the widget).
            template_url:       The URL to fetch the widget template from (Optional - defaults to <<settings.default_api_url>> if 'template' not specified).
            template:           The widget template in string form (Optional - if template_url is specified).
            template_data_path: A dot-seperated path to use part of the API response JSON as template. 
                                (e.g. data.templates.navbar). (Optional - defaults to <<settings.default_template_data_path>>)
            directive_template: The template to use in the AngularJS directive (Optional.)

            models:             A list of objects to fetch from one or more APIs to compile the template with.
            [
                {
                    model:              The name of the model to retrieve.
                    scope_key:          The key used to store the retrieved models in the scope (and to reference them in the template) 
                                        (Optional - defaults to the model name).
                    url:                The url of the API to fetch the model from. (Optional - defaults to <<settings.default_api_url>>)
                    data_path:          A dot-seperated path to use part of the API response JSON as the model 
                                        (e.g. data.authors.Stephen_King). (Optional - defaults to <<settings.default_models_data_path>>)
                }
            ],

            models_override:   A list of pre-fetched objects to compile the template with.
            [ 
                {
                    model:             The name of the model (Optional). 
                    scope_key:         The key used to store the retrieved models in the scope.
                                       (and to reference them in the template) (Optional - defaults to 'model'
                                       if specified otherwise <<settings.default_model_scope_key>>).
                    
                    ...                The rest of the pre-fetched model's attributes.
                }
            ],
        }, 
    */
        {
            tag: 'header',
            api_template: {
                params: {'model': 'widget', 'filter': 'name:header'}
            }
            
        },

        {
            tag: 'sidebar',
            api_models: [{'model': 'category', 'scope_key': 'categories'}],
            api_template: {
                params: {'model': 'widget', 'filter': 'name:sidebar'}
            }
        },
        {
            tag: 'page',
            api_template: {
                params: {'model': 'widget', 'filter': 'name:page'}
            }
        },
        {
            tag: 'footer',
            api_template: {
                params: {'model': 'widget', 'filter': 'name:footer'}
            }
        },
    ],

    routes: [

    ],

    settings: {
        default_api_url: '/api/',
        default_template_url: '/api/',
        default_model_data_path: 'data.models',
        default_model_scope_key: 'extra',
        default_template_data_path: 'data.models.0.template',
        DOM_attach_point: 'body',
    }
};

