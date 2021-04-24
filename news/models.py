from django.core.validators import MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django_resized import ResizedImageField

from users.models import CustomUser


class Issue(models.Model):
    issue_num = models.IntegerField(
        'Issue number', validators=[MinValueValidator(1)])
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return f"""{self.description[:50]}...""" if len(self.description) > 50 else f"""{self.description[:50]}"""


class Article(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ResizedImageField(upload_to='article-images')
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(blank=True)
    issues = models.ManyToManyField(
        Issue, help_text="Select this article's related issue(s).", blank=True)

    def __str__(self) -> str:
        return self.title

    def get_issues(self) -> str:
        return ', '.join(issue.title for issue in self.issues.all()[:3])

    get_issues.short_description = 'Related Issue'


class Comment(models.Model):
    text = models.TextField('Comment text')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text


@receiver(models.signals.pre_save, sender=Article)
def slugify_title(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)


@receiver(models.signals.pre_save, sender=Issue)
def slugify_issue_title(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)
