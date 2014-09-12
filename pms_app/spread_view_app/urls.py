from django.conf.urls import patterns, url
from pms_app.spread_view_app import views


urlpatterns = patterns(
    # title
    'pms_app.spread_view_app',

    # page: index
    url(r'^/index/$', views.index, name='spread_view_app_index'),

    # javascript: webix.js, logic.js
    url(r'^/webix.js', views.webix_js, name='spread_view_webix_js'),
    url(r'^/logic.js', views.logic_js, name='spread_view_logic_js'),

    # json: spreads
    url(r'^/(?P<date>[-\w]+)/(?P<context>[\w]+)/spreads.json',
        views.spreads_json, name='spread_view_spreads_json'),

    # json: symbols
    url(r'^/(?P<date>[-\w]+)/symbols.json', views.symbols_json,
        name='spread_view_symbols_json'),
)