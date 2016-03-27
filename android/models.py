from django.db import models
from django.db.models import Max

# Create your models here.

class AndroidUser(models.Model):
	user = models.OneToOneField('RSS.User')
	
	def __unicode__(self):
		return self.user.__unicode__()

class AndroidApp(models.Model):
	title = models.CharField(max_length=128)
	app_id = models.CharField(max_length=32, primary_key=True)
	
	user = models.ForeignKey('AndroidUser')
	
	def __unicode__(self):
		return self.title

class AppVersion(models.Model):
	APK_FOLDER = "android/apk/";
	
	apk = models.FileField(upload_to=APK_FOLDER)
	local_id = models.IntegerField(default=0)
	version_name = models.CharField(max_length=32)
	
	downloads = models.IntegerField(default=0)
	
	app = models.ForeignKey('AndroidApp')
	
	beta = models.BooleanField(default=False)
	
	class Meta:
		unique_together = ('app','local_id')
	
	def save(self,*args,**kwargs):
		if(self.local_id == 0):
			if(AppVersion.objects.all().filter(app = self.app).exists()):
				self.local_id = AppVersion.objects.all().filter(app = self.app).aggregate(max_local_id=Max('local_id'))['max_local_id']
			else:
				self.local_id = 1
		super(AppVersion,self).save(*args,**kwargs)
	
	def __unicode__(self):
		return self.version_name
