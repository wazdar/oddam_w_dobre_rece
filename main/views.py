from django.shortcuts import render
from django.views.generic.base import View


class LadingPageView(View):
    def get(self, request):
        return render(request, 'main/lading_page_view.html', {

        })


class AddDonationView(View):
    def get(self, request):
        return render(request, 'main/add_donation_view.html', {

        })


class LoginView(View):
    def get(self, request):
        return render(request, 'main/login_view.html')

class RegisterView(View):
    def get(self, request):
        return render(request, 'main/register_view.html')