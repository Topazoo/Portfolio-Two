from django.db import models

class Base_Menu_Content(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__str__())

class Category(Base_Menu_Content):
    pass

class Project(Base_Menu_Content):
    project_category = models.ForeignKey(Category, on_delete=models.CASCADE)