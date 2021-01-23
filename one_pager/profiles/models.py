from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_picture = models.ImageField(default='default.jpg', upload_to='profile-pics')

	def __str__(self):
		return f'{self.user.username}\'s Profile'

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		img = Image.open(self.profile_picture.path)

		if img.height > 256 or img.width > 256:
			output_size = (256,256)
			img.thumbnail(output_size)
			img.save(self.image.path)
