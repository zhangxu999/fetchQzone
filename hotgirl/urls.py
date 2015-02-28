from django.conf.urls import patterns,url
from hotgirl import views
#from django.views.generic import TemplateView
from hotgirl.views import AboutView
from hotgirl.views import gettitlesView
urlpatterns=patterns('',
    #url(r'^$',views.indexView,name='index'),
    url(r'^upimage/$',views.UploadImageView,name='uploadimage'),
    url(r'^vote/$',views.vote,),
    url(r'^getnext/$',views.getnext,),
    url(r'test/$',views.Template_test,),
    url(r'top/$',views.top,),
    url(r'qncallback/$',views.qnCallback,),
    url(r'resp/$',views.resp,),
    url(r'^qncallback_test2/$',views.qncallback_test,),
    url(r'^finnal/$',views.finnal,),
    url(r'^procfinals/$',views.procFinal,),
    url(r'^finalresualt/$',views.finalResualt,),
    url(r'^alltitles/$',views.gettitles,),
    url(r'^genecsv/$',views.genecsv,),
    (r'^about/',AboutView.as_view()),
    url(r'^showtitle/$',gettitlesView.as_view()),
   )