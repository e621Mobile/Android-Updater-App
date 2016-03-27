import json
from android import controller
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import render
from django.template import RequestContext, loader


def index(request):
	if(not controller.is_logged_in(request)):
		return HttpResponseRedirect('/android/login')
	
	template = loader.get_template('html/android/index.html')
	
	context = RequestContext(request, {
		'apps': controller.get_apps(request),
	})
	
	return HttpResponse(template.render(context))

def login(request):
	if(request.method=="POST"):
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)
		
		if(controller.login(request, username, password)):
			return HttpResponseRedirect('/android/')
		else:
			template = loader.get_template('html/android/login.html')
			
			context = RequestContext(request, {
													'user': request.user,
													'error': True,
													'non_subscribe_account': False,
										})
			
			return HttpResponse(template.render(context))
	else:
		template = loader.get_template('html/android/login.html')
		
		context = RequestContext(request, {
												'user': request.user,
												'error': False,
												'non_subscribe_account': False,
									})
		
		return HttpResponse(template.render(context))

def app(request,app_id):
	template = loader.get_template('html/android/app.html')
	
	context = RequestContext(request, {
		'app': app_id,
		'apks': controller.get_apks(request, app_id),
	})
	
	return HttpResponse(template.render(context))

def get_apk(request,app_id,apk_id):
	apk = controller.get_apk(request, app_id, apk_id)
	
	apk.downloads = apk.downloads+1
	apk.save()
	
	return HttpResponseRedirect('/android/' if apk==None else apk.apk.url)

def app_last_apk(request,app_id):
	beta = request.GET.get("beta","false").lower() == "true";
	
	apk = controller.get_latest_apk(request, app_id, beta)
	
	return HttpResponseRedirect(reverse('android.views.get_apk',kwargs={'app_id':apk.app.app_id,'apk_id':apk.local_id}))

def add_apk(request):
	if(request.method=="POST"):
		app = request.POST.get('app',None)
		beta = request.POST.get('beta',False)
		apk = request.FILES.get('apk',None)
		
		if(app != None and apk != None):
			if(controller.add_apk(request, app, apk, beta)):
				return HttpResponseRedirect('/android/app/'+app)
		return HttpResponseRedirect('/android/')
	else:
		return HttpResponseRedirect('/android/')

def last_apk_json(request,app):
	beta = request.GET.get("beta","false").lower() == "true";
	
	apk = controller.get_latest_apk(request, app, beta)
	
	return HttpResponse(json.dumps({
		'versionCode':apk.local_id,
		'versionName':apk.version_name,
		'apkFile': reverse('android.views.get_apk',kwargs={'app_id':app,'apk_id':apk.local_id}),
	}))
