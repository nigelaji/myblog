from django.contrib import admin
from .models import Post



# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'content', 'tags')


from django.contrib import admin
from .models import MDExampleModel

@admin.register(MDExampleModel)
class MDExampleModel(admin.ModelAdmin):
    list_display = ('name',)


