from django.test import TestCase, Client

client = Client(HTTP_USER_AGENT='Mozilla/5.0')

class API_Test(TestCase):
    _method = None  # VIRTUAL: OVERRIDE FOR SPECIFIC METHOD TESTS

    def check_api_method(self, expected_code, expected_msg = None, params = {}):
        result = self._run_method(params).json()

        if expected_msg:
            self.assertEqual(result['msg'], expected_msg)

        self.assertEqual(result['code'], expected_code)

    def _run_method(self, params = {}): 
        return self._method('/api/', params)

class GET_Tests(API_Test):
    _method = client.get

    def test_get_requests(self):
        # Missing model and model filter
        self.check_api_method(400, 'GET - No model supplied in query parameters! (param: model)')
        
        # Missing model filter 
        self.check_api_method(400, 'GET - No model filter supplied in query parameters! (param: filter)', {'model': 'MODEL'})

        # Missing filter
        self.check_api_method(400, 'GET - No model supplied in query parameters! (param: model)', {'filter': 'FILTER'})
        
        # Valid request
        self.check_api_method(200, params={'model': 'MODEL', 'filter': 'FILTER'})

        print('4/4 {} Complete!'.format(self.__class__.__name__))

class POST_Tests(API_Test):
    _method = client.post

    def test_post_requests(self):
        # Missing model
        self.check_api_method(400, 'POST - No model supplied in POST body! (param: model)')
        
        # Valid request (no attrs)
        self.check_api_method(200, params={'model': 'MODEL'})

         # Valid request (with attrs)
        self.check_api_method(200, params={'model': 'MODEL', 'model_attrs': {'test': 'attribute'}})

        #TODO - TEST CREATING MODEL

        print('3/3 {} Complete!'.format(self.__class__.__name__))

class PUT_Tests(API_Test):
    _method = client.put

    def test_put_requests(self):
        # Missing model, model ID and attributes to update
        self.check_api_method(400, 'PUT - No model supplied in PUT body! (param: model)')
        
        # Missing model and model ID
        self.check_api_method(400, 'PUT - No model supplied in PUT body! (param: model)', {"model_attrs": {"test": "attribute"}})

        # Missing model ID and attributes to update
        self.check_api_method(400, 'PUT - No model ID supplied in PUT body! (param: model_id)', {"model": "MODEL"})

        # Missing model and attributes to update
        self.check_api_method(400, 'PUT - No model supplied in PUT body! (param: model)', {"model_id": 0})

         # Missing model
        self.check_api_method(400, 'PUT - No model supplied in PUT body! (param: model)', {"model_id": 0, "model_attrs": {"test": "attribute"}})

        # Missing model ID
        self.check_api_method(400, 'PUT - No model ID supplied in PUT body! (param: model_id)', {"model": "MODEL", "model_attrs": {"test": "attribute"}})

        # Missing attributes to update
        self.check_api_method(400, 'PUT - No attributes to update supplied in PUT body! (param: model_attrs)', {"model": "MODEL", "model_id": 0})

        # Valid request
        self.check_api_method(200, params={"model": "MODEL", "model_id": 0, "model_attrs": {"test": "attribute"}})

        # TODO - TEST UPDATING MODEL

        print('8/8 {} Complete!'.format(self.__class__.__name__))

class DELETE_Tests(API_Test):
    _method = client.delete

    def test_delete_requests(self):
        # Missing model and model ID
        self.check_api_method(400, 'DELETE - No model supplied in DELETE body! (param: model)')
        
        # Missing model ID 
        self.check_api_method(400, 'DELETE - No model ID supplied in DELETE body! (param: model_id)', {'model': 'MODEL'})

        # Missing model
        self.check_api_method(400, 'DELETE - No model supplied in DELETE body! (param: model)', {"model_id": 0})
        
        # Valid request
        self.check_api_method(200, params={'model': 'MODEL', "model_id": 0})

        #TODO - TEST DELETING MODEL

        print('4/4 {} Complete!'.format(self.__class__.__name__))