from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^index/{0,1}$', views.index, name='index'),
    re_path(r'^article/\d{4,4}/\d{1,2}/(?P<key>\d+)/{0,1}$', views.article),
    re_path(r'^articles/list/{0,1}$', views.article_list, name='article_list'),
    re_path(r'^addArticle/{0,1}$', views.addArticle, name='addArticle'),
    re_path(r'^modifyArticle/(?P<key>\d+)/{0,1}$', views.modifyArticle, name='modifyArticle'),
    re_path(r'^deleteArticle/(?P<key>\d+)/{0,1}$', views.deleteArticle, name='deleteArticle'),
    re_path(r'^accounts/login/{0,1}$', views.login, name='login'),
    re_path(r'^accounts/logout/{0,1}$', views.logout, name='logout'),
    re_path(r'test/markdown/{0,1}$', views.test, name='test'),
]