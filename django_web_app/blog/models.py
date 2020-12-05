from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile
import os

class Post(models.Model):
	title = models.CharField(max_length=100)
	file = models.FileField(null=True,blank=True,upload_to='Files')
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def extension(self):
		name, extension = os.path.splitext(self.file.name)
		return extension

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

	def delete(self, *args, **kwargs):
		if os.path.isfile(self.file.path):
			os.remove(self.file.path)
		super(Post, self).delete(*args, **kwargs)


class Comments(models.Model):
	usr=models.ForeignKey(User,on_delete=models.CASCADE)
	post=models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
	com=models.TextField()
	time=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{} - {}".format(self.usr,self.post)

	class Meta:
		ordering=['-time']


class gitrep(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	respo = models.CharField(max_length=255)
	files = models.CharField(max_length=255)
	download = models.CharField(max_length=255)
	time = models.DateField(auto_now=False, auto_now_add=False)
	rpid=models.CharField(max_length=255)

	class Meta:
		ordering = ['-time']
	def __str__(self):
		return '{} - {}'.format(self.respo,self.profile.user.username)



