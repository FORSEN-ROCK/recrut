from django.conf.urls import url
from . import views


urlpatterns = [
    ##url(r'^login/$', views.authorization, name='auth'),
    url(r'^login/$', views.AuthorizationView.as_view(), name='auth'),
    ##url(r'^logout/$', views.exit, name='authExit'),
    url(r'^logout/$', views.ExitView.as_view(), name='exit'),
    ##url(r'^$', views.homespace, name='home'),
    url(r'^$', views.HomespaceView.as_view(), name='home'),
    ##url(r'^$', views.hello_page, name='index'),
    ##url(r'^search/', views.searchView, name='search'),searchForm
    #url(r'^search/$', views.searchForm, name='searchForm'),
    url(r'^search/$', views.SearchFormView.as_view(), name='searchForm'),
    #url(r'^search\/result/$', views.searchOrigen, name='searchResponse'), ##views.responseView, name='searchResponse'),
    #url(r'^search\/result\/resume\/http.+\/incoming/$', views.incomingTreatment, name='parsing'),
    ##url(r'^search\/result/(\d+)$', views.free_search, name='Search'),
    url(r'^search\/result/(\d+)$', views.FreeSearchView.as_view(), 
        name='Search'),
    url(r'^search\/result\/incoming/$', views.incomingTreatment, name='parsing'),
    #url(r'^search\/result\/resume\/(http.+)$', views.parsingOrigen, name='parsing'), ##views.resumeScanAndPasing, name='search'),
    #url(r'^search\/result\/(\d+)$', views.parsingOrigen, name='parsing'),
    url(r'^search\/result\/resume/(\d+)$', views.parsingOrigen,
        name='parsing'),
    url(r'^resume\/add/$', views.saveResume, name='createResume'),
    ##url(r'^resume/$', views.showeResumes, name='ShoweResume'),
    url(r'^resume/$', views.ShoweResume.as_view(), name='ShoweResume'),
    #url(r'^resume\/link\/(\d+)$', views.showeLink, name='ShoweLink'),
    url(r'^resume\/link\/(\d+)$', views.ShoweLinkView.as_view(),
        name='ShoweLink'),
    url(r'^search\/search_task/$', views.searchTask, name='SearchTask'),
    #url(r'^search_pattern/$', views.showe_patterns),
    url(r'^search_pattern/$', views.ShowePattersView.as_view(), 
        name='patterns_list'),
    ##url(r'^search\/(\d+)$', views.search),
    url(r'^search\/(\d+)$', views.SearchView.as_view()),
    ##url(r'^search\/(\d+)\/result/(\d+)', views.respons_search),
    url(r'^search\/(\d+)\/result/(\d+)', views.ResponsSearcheView.as_view()),
    #url(r'^search\/search_task\/(\d+)$', views.searchForTask, name='searchForTask'),
    ##url(r'^resume\/incoming/$', views.incomingTreatment, name='incoming'),
    #url(r'^test/$', views.Test)

]