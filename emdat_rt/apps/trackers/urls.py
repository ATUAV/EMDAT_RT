from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^connect$', views.connect, name='connect'),
    url(r'^(?P<id>[-\w]+)/disconnect$', views.disconnect, name='disconnect'),
    url(r'^(?P<id>[-\w]+)/start_tracking$', views.start_tracking, name='start_tracking'),
    url(r'^(?P<id>[-\w]+)/get_features', views.get_features, name='get_features'),
    url(r'^(?P<id>[-\w]+)/stop_tracking$', views.stop_tracking, name='stop_tracking'),
]
