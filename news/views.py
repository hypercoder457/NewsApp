from typing import Any, Union

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import (Http404, HttpRequest, HttpResponse,
                         HttpResponsePermanentRedirect, HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, DetailView, ListView, TemplateView

from news.forms import ArticleForm, CommentForm, IssueForm
from news.models import Article, Comment, Issue


class HomeView(TemplateView):
    """The home page for the news app."""
    template_name = 'news/home.html'


class ArticlesListView(ListView):
    """Show all the articles, ordered by the date published."""
    model = Article
    template_name = 'news/articles.html'
    context_object_name = 'articles'

    def get_queryset(self) -> QuerySet:
        """Return all the articles ordered by the date published."""
        return Article.objects.order_by('published')


class ArticleDetailView(DetailView):
    """Detail page for a single article. Show the comments as well."""
    model = Article
    template_name = 'news/article-detail.html'


class IssueListView(ListView):
    """Show all the issues."""
    model = Issue
    template_name = 'news/issues.html'
    context_object_name = 'issues'


class IssueDetailView(DetailView):
    """Detail page for a single issue."""
    model = Issue
    template_name = 'news/issue-detail.html'


@login_required
def create_article(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect,
                                                  HttpResponse]:
    """Create a new article."""
    if request.method != 'POST':
        form = ArticleForm()
    else:
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_article: Article = form.save(commit=False)
            new_article.created_by = request.user
            new_article.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Successfully created article.')
            return redirect('news:articles')
    context = {'form': form}
    return render(request, 'news/create-article.html', context)


@login_required
def create_issue(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect,
                                                HttpResponse]:
    """Create a new issue."""
    if request.method != 'POST':
        form = IssueForm()
    else:
        form = IssueForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Issue created successfully.')
            return redirect('news:issues')
    context = {'form': form}
    return render(request, 'news/create-issue.html', context)


@login_required
def create_comment(request: HttpRequest, article_id) -> Union[HttpResponseRedirect,
                                                              HttpResponsePermanentRedirect, HttpResponse]:
    """Create a new comment."""
    article = get_object_or_404(Article, id=article_id)
    if article.created_by != request.user:
        raise Http404
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment: Comment = form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Comment created successfully.')
            return redirect('news:article-detail', slug=article.slug)
    return render(request, 'news/create-comment.html', {'form': form, 'article': article})


@login_required
def edit_article(request: HttpRequest, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.created_by != request.user:
        raise Http404
    if request.method != 'POST':
        form = ArticleForm(instance=article)
    else:
        form = ArticleForm(
            instance=article, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Article updated successfully.')
            return redirect('news:article-detail', slug=article.slug)
    context = {'form': form, 'article': article}
    return render(request, 'news/edit-article.html', context)


@login_required
def edit_issue(request: HttpRequest, issue_id: int):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method != 'POST':
        form = IssueForm(instance=issue)
    else:
        form = IssueForm(instance=issue, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Issue updated successfully.')
            return redirect('news:issue-detail', slug=issue.slug)
    context = {'form': form, 'issue': issue}
    return render(request, 'news/edit-issue.html', context)


@login_required
def edit_comment(request: HttpRequest, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    article: Article = comment.article
    if article.created_by != request.user:
        raise Http404
    if request.method != 'POST':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Comment updated successfully.')
            return redirect('news:article-detail', slug=article.slug)
    context = {'form': form, 'article': article, 'comment': comment}
    return render(request, 'news/edit-comment.html', context)


class DeleteArticleView(DeleteView):
    model = Article
    template_name = 'news/delete-article.html'
    success_url = '/'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.add_message(request, messages.SUCCESS,
                             'Successfully deleted article.')
        return super().post(request, *args, **kwargs)


class DeleteIssueView(DeleteView):
    model = Issue
    template_name = "news/delete-issue.html"
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.add_message(request, messages.SUCCESS,
                             'Successfully deleted issue.')
        return super().post(request, *args, **kwargs)


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = "news/delete-comment.html"
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.add_message(request, messages.SUCCESS,
                             'Successfully deleted comment.')
        return super().post(request, *args, **kwargs)
