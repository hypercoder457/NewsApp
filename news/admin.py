from django.contrib import admin

from news.models import Article, Comment, Issue


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'updated_at',
                    'created_by', 'slug', 'get_issues']
    list_filter = ['title']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['issue_num', 'title', 'slug']
    list_filter = ['issue_num']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'article']
