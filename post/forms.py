from django import forms
from post.models import Post

class PostForm(forms.ModelForm):
    post_picture = forms.FileField(required=True,)
    post_caption = forms.CharField(required=True,)
    tags = forms.CharField(required=True,)

    class Meta:
        model = Post
        fields = ('post_picture','post_caption','tags')

    
