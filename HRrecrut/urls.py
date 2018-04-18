from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.AuthorizationView.as_view(), name='auth'),
    url(r'^logout/$', views.ExitView.as_view(), name='exit'),
    url(r'^$', views.HomespaceView.as_view(), name='home'),
    url(r'^search/$', views.SearchFormView.as_view(), name='searchForm'),
    url(r'^search\/result/$', views.FreeSearchView.as_view(), 
        name='Search'),
    url(r'^search\/result\/resume/(\d+)\/incoming/$', 
        views.ResumeParserView.as_view(),
        name='incoming'),
    url(r'^search\/result\/resume/(\d+)$', views.ResumeParserView.as_view(),
        name='parsing'),
    url(r'^resume/$', views.ShoweResume.as_view(), name='ShoweResume'),
    url(r'^search\/search_task/$', views.searchTask, name='SearchTask'),
    url(r'^search_pattern/$', views.ShowePattersView.as_view(), 
        name='patterns_list'),
    url(r'^search\/(\d+)$', views.SearchView.as_view()),
    url(r'^search\/(\d+)\/result/(\d+)', views.ResponsSearcheView.as_view()),
]