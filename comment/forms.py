from django import forms
from comment.models import PostComment

class CommentForm(forms.ModelForm):
    comment = forms.CharField(required=True)

    class Meta:
        model = PostComment
        fields = ('comment',)
