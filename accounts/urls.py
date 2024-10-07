from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserRegisterView, UserLoginView, UserLogoutView, \
	CustomPasswordResetCompleteView

app_name = 'accounts'

urlpatterns = [
	path('register/', UserRegisterView.as_view(), name='user_register'),
	path('login/', UserLoginView.as_view(), name='user_login'),
	path('logout/', UserLogoutView.as_view(), name='user_logout'),
	
	# Password reset URLs
	path('password_reset/', auth_views.PasswordResetView.as_view(
		template_name='accounts/password_reset.html'), name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
		template_name='accounts/password_reset_done.html'),
	     name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
		template_name='accounts/password_reset_confirm.html'),
	     name='password_reset_confirm'),
	
	# Custom view for completion of password reset
	path('reset/done/', CustomPasswordResetCompleteView.as_view(),
	     name='password_reset_complete'),
]
