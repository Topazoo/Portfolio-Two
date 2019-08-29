from django.db import models
import json

class API_Model(models.Model):
    ''' The base model for all models the API can interact with.

        * @supported_methods can be overidden to restrict API interaction with a model to specific methods *
    ''' 
    
    supported_methods = ['ALL']

    def to_json(self):
        ''' Write all non-relational model data to JSON '''

        attrs_map = {}
        ignore_field_types = [
            models.fields.AutoField,
            models.fields.related.OneToOneField,
            models.fields.related.ManyToManyField,
            models.fields.related.ForeignKey,
        ]
        ignore_attrs = []

        for field in self._meta.fields:
            if type(field) not in ignore_field_types:
                attrs_map[field.name] = getattr(self, field.name, 'None')

        return json.dumps(attrs_map)

    def __str__(self):
        return str(self.__class__.__name__)
    
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__str__())

class Category(API_Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.name)

class Project(API_Model):
    project_category = models.ForeignKey(Category, on_delete=models.CASCADE)