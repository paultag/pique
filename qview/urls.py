from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('pyqie.qview.views',
    url(r'^$',                        'home',   name='home'),
    url(r'^buginf/(?P<buginf>\d+)/$', 'buginf', name='buginf' ),
)
