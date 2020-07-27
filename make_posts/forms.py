from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from make_posts.models import Post, Comment


class UserLoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(UserLoginForm, self).__init__(request=request, *args, **kwargs)

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'data-test': 'username'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'data-test': 'password'}),
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'data-test': 'post', 'class': 'form-control'})
        }

    def clean(self):
        super().clean()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']
        widgets = {
            'comment_content': forms.TextInput(attrs={'data-test': 'comment-text', 'class': 'form-control'})
        }
