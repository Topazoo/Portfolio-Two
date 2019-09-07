// REGISTER ANGULAR JS FIXTURES HERE:


var Fixtures = {

    modules: [

    ],

    widgets: [
        {
            name: 'header',
        },

        {
            name: 'sidebar',
            models: [{'model': 'category'}]
        },
    ],

    routes: [

    ]
};


/**
    FIXTURE SPECIFICS
        modules
            Custom Angular modules defined in any script included in the DOM should be
            registered here. This allows any number of modules to be mixed and matched.
        
            Parameters:
                name - The name of the module.
                // TODO - services

        widgets
            Templates to compile with (optional) models from the API. Registered widgets
            can be added to the DOM using a specified tag (e.g. <widget-name></widget-name>).
            Templates and stylesheets used to render the widgets are delivered by the API and are stored on the 
            server in <<STATIC_ROOT>/widgets/.

            Parameters:
                name - The name of the widget (will be the HTML tag that renders the widget).
                models - A list of models to compile the template with, in the proper format for GET() (e.g. {'model': 'mymodel'} or 
                        {'model': 'mymodel', 'filter': 'name:model_name'}). Optional.
                html_template - The template to use when rendering the widget. <<STATIC_ROOT>/widgets/<<name>>.html by default. Optional.

        routes
            Routes and associated pages to be used by ngRoute in Single Page Applications.
**/