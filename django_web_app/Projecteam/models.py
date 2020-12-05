from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django_web_app import settings
import os
import shutil
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment

def nameing(self,filename):
    path = "TeamFiles"
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, path, self.user.name)):
        return path + "/" + self.user.name+"/"+filename
    else:
        os.makedirs(os.path.join(settings.MEDIA_ROOT, path, self.user.name))
        return path + "/" + self.user.name+"/"+filename

class projectdb(models.Model):
    name=models.CharField(max_length=30,unique=True)
    title=models.CharField(max_length=20)
    leader=models.ForeignKey(User,on_delete=models.CASCADE)
    member=ArrayField(models.CharField(max_length=255),size=4)
    status=models.BooleanField(default=False)
    comments = GenericRelation(Comment)



    def __str__(self):
        return "{} - {}".format(self.name,self.title)

    def delete(self, *args, **kwargs):
        path = "TeamFiles"
        if os.path.isdir(os.path.join(settings.MEDIA_ROOT, path, self.name)):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, path, self.name))
        super().delete(*args, **kwargs)  # Call the "real" save() method.

class projectFiles(models.Model):
    user=models.ForeignKey(projectdb,on_delete=models.CASCADE)
    file=models.FileField(upload_to=nameing)

    def delete(self, *args, **kwargs):
        path = "TeamFiles"
        os.remove(settings.MEDIA_ROOT+'/'+str(self.file))
        super().delete(*args,**kwargs)

    def __str__(self):
        return "{} ".format(self.user.name)

