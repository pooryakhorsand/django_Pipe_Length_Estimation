from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.Form):
	"""
    A form for user registration, allowing new users to create an account.
    """
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
		label='Username'
	)
	email = forms.EmailField(
		widget=forms.EmailInput(
			attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
		label='Email'
	)
	password1 = forms.CharField(
		label='Password',
		widget=forms.PasswordInput(attrs={'class': 'form-control',
		                                  'placeholder': 'Enter your password'})
	)
	password2 = forms.CharField(
		label='Confirm Password',
		widget=forms.PasswordInput(attrs={'class': 'form-control',
		                                  'placeholder': 'Re-enter your password'})
	)
	
	def clean_email(self):
		"""
        Validate that the provided email is unique.
        Raises ValidationError if the email is already in use.
        """
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise ValidationError('This email is already in use.')
		return email
	
	def clean(self):
		"""
        Validate that both password fields match.
        Raises ValidationError if the passwords do not match.
        """
		cd = super().clean()
		p1 = cd.get('password1')
		p2 = cd.get('password2')
		
		if p1 and p2 and p1 != p2:
			raise ValidationError('Passwords must match.')


class UserLoginForm(forms.Form):
	"""
    A form for user login, allowing existing users to authenticate.
    """
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
		label='Username'
	)
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control',
		                                  'placeholder': 'Enter your password'}),
		label='Password'
	)
