from django import forms
from feedback.models import Feedback

class FeedbackForm(forms.ModelForm):
    category = forms.IntegerField(required=True)
    feedback = forms.CharField(required=True)

    class Meta:
        model = Feedback
        fields = ('category','feedback',)