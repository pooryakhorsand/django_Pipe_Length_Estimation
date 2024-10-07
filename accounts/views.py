from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from .forms import UserRegistrationForm, UserLoginForm


class UserRegisterView(View):
	"""
	View for handling user registration.

	Provides methods for displaying the registration form and processing form submissions to create new users.
	"""
	form_class = UserRegistrationForm
	template_name = 'accounts/register.html'
	
	def get(self, request):
		"""
		Display the registration form.

		Args:
			request: The HTTP request object.

		Returns:
			HttpResponse: Rendered registration form template.
		"""
		form = self.form_class()
		return render(request, self.template_name, {'form': form})
	
	def post(self, request):
		"""
		Handle form submission for user registration.

		Args:
			request: The HTTP request object with form data.

		Returns:
			HttpResponse: Redirects to the index page if registration is successful or renders the registration form with errors.
		"""
		form = self.form_class(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password1']
			
			if User.objects.filter(username=username).exists():
				messages.error(request, 'Username already exists.', 'warning')
			elif User.objects.filter(email=email).exists():
				messages.error(request, 'Email already exists.', 'warning')
			else:
				User.objects.create_user(username=username, email=email,
				                         password=password)
				messages.success(request, 'You registered successfully',
				                 'success')
				return redirect('length:length')
		
		return render(request, self.template_name, {'form': form})


class UserLoginView(View):
	"""
	View for handling user login.

	Provides methods for displaying the login form and authenticating users.
	"""
	form_class = UserLoginForm
	template_name = 'accounts/login.html'
	
	def get(self, request):
		"""
		Display the login form.

		Args:
			request: The HTTP request object.

		Returns:
			HttpResponse: Rendered login form template.
		"""
		form = self.form_class()
		return render(request, self.template_name, {'form': form})
	
	def post(self, request):
		"""
		Handle form submission for user login.

		Args:
			request: The HTTP request object with form data.

		Returns:
			HttpResponse: Redirects to the next URL or index page upon successful login, or re-renders the login form with errors.
		"""
		form = self.form_class(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			
			if user is not None:
				login(request, user)
				messages.success(request, 'You logged in successfully',
				                 'success')
				next_url = request.GET.get('next', reverse_lazy('length:length'))
				return redirect(next_url)
			else:
				messages.error(request, 'Username or password is incorrect',
				               'warning')
		
		return render(request, self.template_name, {'form': form})


class UserLogoutView(View):
	"""
	View for handling user logout.

	Provides methods for displaying a logout confirmation page and logging out the user.
	"""
	
	def get(self, request):
		"""
		Display the logout confirmation page.

		Args:
			request: The HTTP request object.

		Returns:
			HttpResponse: Rendered logout confirmation template.
		"""
		return render(request, 'accounts/logout.html')
	
	def post(self, request):
		"""
		Log the user out and redirect to the login page.

		Args:
			request: The HTTP request object.

		Returns:
			HttpResponse: Redirects to the login page after logout.
		"""
		logout(request)
		return redirect('accounts:user_login')


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
	"""
	Custom view for handling password reset completion.

	Redirects to the login page after a successful password reset.
	"""
	
	def get(self, request, *args, **kwargs):
		"""
		Redirect to the login page after password reset.

		Args:
			request: The HTTP request object.
			*args: Additional positional arguments.
			**kwargs: Additional keyword arguments.

		Returns:
			HttpResponseRedirect: Redirects to the login page.
		"""
		return redirect(reverse_lazy('accounts:user_login'))
