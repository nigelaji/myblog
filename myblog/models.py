from django.db import models
import datetime

# Create your models here.
class Post(models.Model):
    key = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    tags = models.CharField(max_length=50)
    date = models.DateField()


    def get_format_date(self):
        return f'{self.date.year}-{self.date.month}-{self.date.day}'

    def get_brief_content(self):
        return f'{self.content[:5]}...'

    def get_absolute_url(self):
        return f'/myblog/article/{self.date.year}/{self.date.month}/{self.key}'

    def get_modify_url(self):
        return f'/myblog/modifyArticle/{self.key}'

    def get_delete_url(self):
        return f'/myblog/deleteArticle/{self.key}'

from django.db import models
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget

class ExampleModel(models.Model):
    name = models.CharField(max_length=10)
    content = RichTextField()

from django.db import models
from mdeditor.fields import MDTextField

class MDExampleModel(models.Model):
    name = models.CharField(max_length=10)
    content = MDTextField()

