from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.sites.models import Site
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=False, blank=True,
                            help_text="Slug will be generated automatically from the title of the post")
    content = RichTextUploadingField(blank=True)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    pic_url = models.CharField(max_length=1000)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id, self.slug])

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Category(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=False, blank=True)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "categories"


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    message = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.message


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact"

    def __str__(self):
        return self.name + "-" +  self.email
