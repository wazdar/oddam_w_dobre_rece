from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize

from datetime import datetime

from .models import (
    Category,
    Donation,
    Institution,
    FOUNDATION,
    NON_GOV,
    LOCAL_COLLECTION
)
from .forms import UserRegister, UserLoginForm, DonationForm, UserProfile


class LadingPageView(View):
    def get(self, request):
        return render(request, 'main/lading_page_view.html', {
            'total_bags_count': sum([x.quantity for x in Donation.objects.all()]),
            'total_institution_count': Donation.objects.all().distinct('institution').count(),
            'help_foundations': Institution.objects.filter(institution_type=FOUNDATION),
            'help_gov': Institution.objects.filter(institution_type=NON_GOV),
            'help_local_collection': Institution.objects.filter(institution_type=LOCAL_COLLECTION),
        })


class AddDonationView(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request):
        step = request.GET.get('step')
        if step is not None:
            if step == '1':
                categories = Category.objects.all()
                result = [[category.id, category.name] for category in categories]
                return JsonResponse(result, safe=False)
            elif step == '3':
                institution_set = Institution.objects.filter(
                    categories__pk__in=request.GET.getlist('categories[]')).distinct()
                result = [
                    [institution.id, institution.name, institution.description]
                    for institution in institution_set
                ]
                return JsonResponse(result, safe=False)
        return render(request, 'main/add_donation_view.html', {
            'form_category': Category.objects.all(),
        })

    def post(self, request):
        post_data = {**request.POST}
        donation = Donation.objects.create(
            quantity=post_data['bags'][0],
            institution=Institution.objects.get(pk=post_data['organization'][0]),
            address=post_data['address'][0],
            phone_number=post_data['phone'][0],
            city=post_data['city'][0],
            zip_code=post_data['postcode'][0],
            pick_up_date=datetime.fromisoformat(post_data['data'][0]).date(),
            pick_up_time=datetime.strptime(post_data['time'][0], '%H:%M').time(),
            pick_comment=post_data['more_info'][0],
            user=request.user
        )
        for category in post_data['categories']:
            cat = Category.objects.get(pk=category)
            donation.categories.add(cat)
            donation.save()

        return render(request, 'main/donation_confirm.html')


class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'main/login_view.html', {
            'form': form
        })

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            try:
                user_db = User.objects.get(email=form.cleaned_data['email'])
                user = authenticate(request, username=user_db.username, password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('landing-page')
            except User.DoesNotExist:
                return redirect('register-page')
        return render(request, 'main/login_view.html', {
            'form': form,
            'msg': 'Błędne hasło'
        })


class RegisterView(View):
    def get(self, request):
        form = UserRegister
        return render(request, 'main/register_view.html', {
            'form': form,
        })

    def post(self, request):
        form = UserRegister(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                del form.cleaned_data['password2']
                form.cleaned_data['password'] = form.cleaned_data.pop('password1')
                User.objects.create_user(**form.cleaned_data)
                return redirect('login-page')

        return render(request, 'main/register_view.html', {
            'form': form,
            'msg': "Password didn't match"
        })


def logout_view(request):
    logout(request)
    return redirect('landing-page')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserProfile(initial={
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,

        })
        return render(request, 'main/user_profile.html', {
            'form': form
        })
