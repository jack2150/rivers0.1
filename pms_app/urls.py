from django.conf.urls import patterns, include, url
from pms_app import views

urlpatterns = patterns(
    'pms_app',
    url(r'^position/import', include('pms_app.pos_import_app.urls')),
    #url(r'^position/import', views.index, name='views_index'),
    url(r'^position/view', include('pms_app.pos_view_app.urls')),
)
