from django.db import models
import django.db.models.fields as field_types
import json

class API_Model(models.Model):
    supported_methods = ['ALL']

    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__str__())

    def to_json(self):
        attrs_map = {}
        ignore_field_types = [
            field_types.AutoField,
            field_types.related.OneToOneField,
            field_types.related.ManyToManyField,
            field_types.related.ForeignKey,
        ]
        ignore_attrs = []

        for field in self._meta.fields:
            if type(field) not in ignore_field_types:
                attrs_map[field.name] = getattr(self, field.name, 'None')

        return json.dumps(attrs_map)

class Category(API_Model):
    pass

class Project(API_Model):
    project_category = models.ForeignKey(Category, on_delete=models.CASCADE)