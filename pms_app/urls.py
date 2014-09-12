from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'pms_app',
    url(r'^position/import', include('pms_app.pos_import_app.urls')),
    url(r'^position/view', include('pms_app.pos_view_app.urls')),
    url(r'^spreads/view', include('pms_app.spread_view_app.urls')),
)
