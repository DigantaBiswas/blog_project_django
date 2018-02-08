from django import forms

from django.contrib.auth.models import User 

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	
)

user = get_user_model()
class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget= forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		
		if  username and password:

			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("this user not exists")
			if not user.check_password(password):
				raise forms.ValidationError("incorrect password")
			if not user.is_active:
				raise forms.ValidationError("This user is not active")
		return super(UserLoginForm, self).clean(*args, *kwargs)


class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email address')
	password = forms.CharField(widget= forms.PasswordInput)
	class Meta:
		model = user
		fields = [
			'username',
			'email',
			'password'

		]
	def clean_email(self):
		email = self.cleaned_data.get('email')
		email_qs = user.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")
		return email