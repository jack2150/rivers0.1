from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    # url(r'^$', 'rivers2.views.home', name='home')
    '',

    # base_app
    url(r'^base/', include('base_app.urls')),

    # pms_app
    url(r'^pms/', include('pms_app.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)
