from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['id',
                  'post',
                  'author',
                  'category',
                  'heading',
                  'text'
                 ]