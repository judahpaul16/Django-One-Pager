from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.template.defaultfilters import slugify
from multiselectfield import MultiSelectField
from audiofield.fields import AudioField
from autoslug import AutoSlugField
from PIL import Image

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    intro = models.TextField(max_length=100, blank=True, editable=False)
    post_image = models.ImageField(default='default_post.png', upload_to='post-pics')
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='title', default='', unique=True, null=False, editable=False)
    draft = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return f'{self.author.first_name}\'s Post'

    def __str__(self):
        return f'{self.author.first_name}\'s Post'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.intro = self.content[0:240]
        super(Post, self).save(*args, **kwargs)

        img = Image.open(self.post_image.path)

        if img.height > 720 or img.width > 1280:
            output_size = (1280,720)
            img.thumbnail(output_size)
            img.save(self.post_image.path)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.id, 'slug': self.slug})

class Testimonial(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField(max_length=120)
    timestamp = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return f'{self.author.first_name}\'s Testimonial'

    def __str__(self):
        return f'{self.author.first_name}\'s Testimonial'

    def save(self, *args, **kwargs):
        super(Testimonial, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('home')

class AudioFile(models.Model):
    header = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)
    checked_by = models.ForeignKey(User, related_name='checker', default='', blank=True, null=True, editable=False, on_delete=models.PROTECT)
    verified_by = models.ForeignKey(User, related_name='verifier', default='', blank=True, null=True, editable=False, on_delete=models.PROTECT)
    is_checked = models.BooleanField(default=False, editable=False)
    is_verified = models.BooleanField(default=False, editable=False)
    audio_file = AudioField(upload_to='audio', blank=True,
                            ext_whitelist=(".mp3", ".wav", ".ogg"),
                            help_text=("Allowed type - .mp3, .wav, .ogg"))
    CHOICES = (
        ('1', 'Important'),
        ('2', 'Not Important'),
        ('3', 'Unsure')
    )
    checked_status = MultiSelectField(choices = CHOICES, blank=True, default="")
    verified_status = MultiSelectField(choices = CHOICES, blank=True, default="")

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return f'Audio File: {self.header}'

    def __str__(self):
        return f'Audio File: {self.header}'

    def audio_file_player(self):
        if self.audio_file:
            file_url = settings.MEDIA_URL + str(self.audio_file)
            player_string = f'<audio src="{file_url}" controls>Your browser does not support the audio element.</audio>'
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = ('Audio file player')

    def save(self, *args, **kwargs):
        super(AudioFile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('audio', kwargs={'pk': self.id})

class VideoFile(models.Model):
    header = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    video_file = models.FileField(upload_to='videos', null=True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return f'Video File: {self.header}'

    def __str__(self):
        return f'Video File: {self.header}'

    def video_file_player(self):
        if self.video_file:
            file_url = settings.MEDIA_URL + str(self.video_file)
            player_string = f"<video id='autoplay' controls><source src={file_url} type='video/mp4'>Your browser does not support the video tag.</video>"
            return player_string

    video_file_player.allow_tags = True
    video_file_player.short_description = ('Video file player')

    def save(self, *args, **kwargs):
        super(VideoFile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('videos', kwargs={'pk': self.id})
