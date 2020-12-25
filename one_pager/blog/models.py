from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    intro = models.TextField(max_length=100, blank=True)
    post_image = models.ImageField(default='default_post.png', upload_to='post-pics')
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='title', default='', unique=True, null=False, editable=False)
    draft = models.BooleanField(default=False)

    def __unicode__(self):
        return f'{self.author.first_name}\'s Post'

    def __str__(self):
        return f'{self.author.first_name}\'s Post'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.intro = self.content[0:240]
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.id, 'slug': self.slug})

class Testemonial(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=240)
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='title', default='', unique=True, null=False, editable=False)

    def __unicode__(self):
        return f'{self.author.first_name}\'s Testemonial'

    def __str__(self):
        return f'{self.author.first_name}\'s Testemonial'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Testemonial, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('testemonial-detail', kwargs={'pk': self.id, 'slug': self.slug})
