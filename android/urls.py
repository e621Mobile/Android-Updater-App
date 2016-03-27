from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'android.views.index'),
	url(r'^login/$', 'android.views.login'),
	url(r'^app/(?P<app_id>[^/]+)/$', 'android.views.app'),
	url(r'^app/(?P<app_id>[^/]+)/(?P<apk_id>\d+).apk$', 'android.views.get_apk'),
	url(r'^app/(?P<app_id>[^/]+)/latest.apk$', 'android.views.app_last_apk'),
	url(r'^add_apk/$', 'android.views.add_apk'),
	url(r'^last_json/(?P<app>[^/]+)/$', 'android.views.last_apk_json'),
)
