from django.contrib import admin
from django.urls import path

import main.views as Main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.LadingPageView.as_view(), name='landing-page'),
    path('add_donation', Main.AddDonationView.as_view(), name='add-donation-page'),
    path('register', Main.RegisterView.as_view(), name='register-page'),
    path('login', Main.LoginView.as_view(), name='login-page'),
    path('logout', Main.logout_view, name='logout-page'),
    path('profil', Main.UserProfileView.as_view(), name='profile-page'),
    path('settings', Main.UserSettingsView.as_view(), name='settings-page'),
    path('donation_confirm', Main.takenConfirm, name='confirm-page'),

]
