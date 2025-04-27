from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ProfileDetailView,ProfileUpdateView
urlpatterns = [
    path('signup/employer',views.employer_signup,name="employer_signup"),
    path('signup/candidate',views.candidate_signup,name="candidate_signup"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
        path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset_form.html'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),       # View profile
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),  # Edit profile
]
