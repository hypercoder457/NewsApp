from django import forms

from news.models import Article, Comment, Issue


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description', 'content', 'image', 'issues']
        widgets = {'title': forms.Textarea(
            attrs={'cols': 80}), 'description': forms.Textarea(attrs={'cols': 80}),
            'content': forms.Textarea(attrs={'cols': 80}), 'image': forms.ClearableFileInput()}


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'issue_num']
        widgets = {'description': forms.Textarea(attrs={'cols': 80})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
