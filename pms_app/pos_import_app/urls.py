from django.conf.urls import patterns, url
from pos_import_app import views

urlpatterns = patterns(
    'pms_app.pos_import_app',
    # index: select csv files page
    url(r'^/index', views.index, name='pos_import_app_index'),

    # complete: open csv file and insert data to db
    url(r'^/complete/$', views.complete, name='pos_import_app_complete'),
    url(r'^/complete/(?P<date>[-\w]+)/$', views.complete, name='pos_import_app_complete'),
)