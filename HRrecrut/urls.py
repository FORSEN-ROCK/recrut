from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.authorization, name='auth'),
    url(r'^logout/$', views.exit, name='authExit'),
    url(r'^$', views.homespace, name='home'),
    ##url(r'^$', views.hello_page, name='index'),
    ##url(r'^search/', views.searchView, name='search'),searchForm
    url(r'^search/$', views.searchForm, name='searchForm'),
    url(r'^search\/result/$', views.responseView, name='searchResponse'),
    url(r'^search\/result\/resume\/(http.+)$', views.resumeScanAndPasing, name='search'),
    url(r'^resume\/add/$', views.saveResume, name='createResume')

]