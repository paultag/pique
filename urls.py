from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('pique.views',
    url(r'^', include('pique.qview.urls')),
)
