import os
import shutil
import subprocess
import tempfile
from android.models import *
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login


def login(request,username,password):
	user = authenticate(email=username, password=password)
	
	if(user != None):
		try:
			user.androiduser
			auth_login(request,user)
			return True
		except:
			return False
	else:
		return False

def is_logged_in(request):
	if(request.user.is_authenticated()):
		try:
			request.user.androiduser
			return True
		except:
			return False
	else:
		return False

def get_apps(request):
	return AndroidApp.objects.all().filter(user__user__email=request.user.email).values('title','app_id')

def get_apks(request,app):
	try:
		return AppVersion.objects.all().filter(app__app_id=app)
	except:
		return []

def get_apk(request,app,apk):
	try:
		return AppVersion.objects.get(app__app_id=app,local_id=apk)
	except:
		return None

def get_latest_apk(request,app,beta):
	query = AppVersion.objects.filter(app__app_id = app)
	
	print beta
	
	if(not beta):
		query = query.exclude(beta = True)
	
	query = query.order_by('-local_id')
	return query[0]

def add_apk(request,app,apk,beta):
	try:
		app = AndroidApp.objects.get(user__user__email=request.user.email,app_id=app)
		temp_folder = tempfile.mkdtemp()
		temp_file_path = temp_folder + '/file'
		
		with open(temp_file_path, 'wb+') as destination:
			for chunk in apk.chunks():
				destination.write(chunk)
			destination.close()
			
			code = subprocess.Popen(["bash",os.path.join(settings.AAPT_PATH,"getVersionCode.bash"),destination.name],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().strip()
			name = subprocess.Popen(["bash",os.path.join(settings.AAPT_PATH,"getVersionName.bash"),destination.name],stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().strip()
		
		temp = open(temp_file_path, 'r')
		
		new_file_path = AppVersion.APK_FOLDER + app.app_id + "_" + name + ".apk"
		new_file = open(settings.MEDIA_ROOT + new_file_path, "wb+")
		
		new_file.write(temp.read());
		
		new_file.close()
		temp.close();
		
		AppVersion.objects.create(
			apk = new_file_path,
			local_id = code,
			version_name = name,
			app = app,
			beta=beta
		)
		
		shutil.rmtree(temp_folder)
		
		return True;
	finally:
		pass
	#except Exception as e:
	#	raise e
	#	return False
