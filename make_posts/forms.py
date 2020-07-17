from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from make_posts.models import Post


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
            'content': forms.TextInput(attrs={'data-test': 'post'})
        }

    def clean(self):
        super().clean()
