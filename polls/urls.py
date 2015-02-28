from django.conf.urls import patterns,url
from polls import views
from polls.views import genericChoice
urlpatterns=patterns('',
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^(?P<pk>\d+)/$',views.DetailView.as_view(),name='detail'),
    url(r'^(?P<pk>\d+)/results/$',views.ResultsView.as_view(),name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    url(r'^form/$',views.contact,name='contact'),
    url(r'^hello/$',views.hello,name='hello'),
   # url(r'^about/',views2.aboutView.as_view()),
    url(r'^generic/$', genericChoice.as_view()),
    )
