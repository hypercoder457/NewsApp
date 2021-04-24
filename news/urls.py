from typing import List

from django.urls import URLPattern, path

from . import views

app_name = 'news'
urlpatterns: List[URLPattern] = [
    path('', views.HomeView.as_view(), name='home'),
    path('articles/', views.ArticlesListView.as_view(), name='articles'),
    path('article-detail/<slug>/',
         views.ArticleDetailView.as_view(), name='article-detail'),
    path('issues/', views.IssueListView.as_view(), name='issues'),
    path('issue-detail/<slug>', views.IssueDetailView.as_view(), name='issue-detail'),
    path('create-article/', views.create_article, name='create-article'),
    path('create-issue/', views.create_issue, name='create-issue'),
    path('create-comment/<int:article_id>/',
         views.create_comment, name='create-comment'),
    path('edit-article/<int:article_id>/',
         views.edit_article, name='edit-article'),
    path('edit-issue/<int:issue_id>/', views.edit_issue, name='edit-issue'),
    path('edit-comment/<int:comment_id>/',
         views.edit_comment, name='edit-comment'),
    path('delete-article/<slug>/',
         views.DeleteArticleView.as_view(), name='delete-article'),
    path('delete-issue/<slug>/',
         views.DeleteIssueView.as_view(), name='delete-issue'),
    path('delete-comment/<slug>/',
         views.DeleteCommentView.as_view(), name='delete-comment')
]
