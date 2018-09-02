from django import forms
from django.forms import widgets
from .models import Post
import datetime


class PasswordField(forms.Field):
    widget = forms.PasswordInput

class TextFiled(forms.Field):
    widget = forms.Textarea


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20)
    password = PasswordField(label='密码')

class TagInput(widgets.Input):
    input_type = 'text'
    template_name = 'myblog/widgets/input.html'

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tags', 'content']
        widgets = {
            'tags': TagInput
        }

    def save(self, commit=True):
        self.instance.key = abs(hash(self.instance.title))
        self.instance.date = datetime.datetime.now().strftime('%Y-%m-%d')

        self.instance.save()

        return self.instance

    def modify(self, key):
        self.instance.key = key
        self.instance.date = datetime.datetime.now().strftime('%Y-%m-%d')

        self.instance.save()

        return self.instance



from mdeditor.fields import MDTextFormField
from mdeditor.widgets import MDEditorWidget


class MarkdownForm(forms.Form):
    name = forms.CharField()
    content = MDTextFormField(widget=MDEditorWidget)

class PasswordInput(widgets.Input):
    input_type = 'password'
    template_name = 'myblog/widgets/input.html'

class TestForm(forms.Form):
    name = forms.CharField()
    content = forms.CharField()
    password = forms.CharField(widget=PasswordInput)



