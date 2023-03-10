from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from user_auth.models import Profile

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this email already exists.')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('User with this username already exists.')
    
class SignupForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True,)
    email = forms.CharField(max_length=100, required=True,)
    password = forms.CharField(required=True,)
    confirm_password = forms.CharField(required=True)

    class Meta:

        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(InvalidUser)
        self.fields['username'].validators.append(UniqueUser)
        self.fields['email'].validators.append(UniqueEmail)

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Passwords do not match. Try again.....'])
		
        return self.cleaned_data

class ChangePasswordForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(required=True)
	new_password = forms.CharField(required=True)
	confirm_password = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ('id', 'old_password', 'new_password', 'confirm_password')

	def clean(self):
		super(ChangePasswordForm, self).clean()
		id = self.cleaned_data.get('id')
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		user = User.objects.get(pk=id)
		if not user.check_password(old_password):
			self._errors['old_password'] =self.error_class(['Old password do not match.'])
		if new_password != confirm_password:
			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
		return self.cleaned_data
	

class ProfileEditForm(forms.ModelForm):
	first_name = forms.CharField(max_length=150, required=False)
	last_name = forms.CharField(max_length=150, required=False)
	course = forms.CharField(max_length=150,required=False)
	profile_picture = forms.FileField(required=False)
	profile_info = forms.CharField(widget=forms.Textarea,max_length=300,required=False)

	class Meta:
		model = Profile
		fields = ('profile_picture','first_name','last_name','course','profile_picture','profile_info')

	


        
		
    


