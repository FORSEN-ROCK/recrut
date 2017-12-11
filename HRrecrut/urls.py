from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.authorization, name='auth'),
    url(r'^logout/$', views.exit, name='authExit'),
    url(r'^$', views.homespace, name='home'),
    ##url(r'^$', views.hello_page, name='index'),
    ##url(r'^search/', views.searchView, name='search'),searchForm
    url(r'^search/$', views.searchForm, name='searchForm'),
    url(r'^search\/result/$', views.searchOrigen, name='searchResponse'), ##views.responseView, name='searchResponse'),
    #url(r'^search\/result\/resume\/http.+\/incoming/$', views.incomingTreatment, name='parsing'),
    url(r'^search\/result\/incoming/$', views.incomingTreatment, name='parsing'),
    #url(r'^search\/result\/resume\/(http.+)$', views.parsingOrigen, name='parsing'), ##views.resumeScanAndPasing, name='search'),
    url(r'^search\/result\/(\d+)$', views.parsingOrigen, name='parsing'),
    url(r'^resume\/add/$', views.saveResume, name='createResume'),
    url(r'^resume/$', views.showeResumes, name='ShoweResume'),
    url(r'^resume\/link\/(\d+)$', views.showeLink, name='ShoweLink'),
    url(r'^search\/search_task/$', views.searchTask, name='SearchTask'),
    url(r'^search\/search_task\/(\d+)$', views.searchForTask, name='searchForTask'),
    ##url(r'^resume\/incoming/$', views.incomingTreatment, name='incoming'),
    url(r'^test/$', views.Test)

]