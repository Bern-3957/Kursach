from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from .forms import *

menu = [{'title': 'Услуги', 'url_name': 'services'},
        {'title': 'Каталог продукции', 'url_name': 'shop_catalog'},
        {'title': 'О компании', 'url_name': 'about_us'},
        {'title': 'Контакты', 'url_name': 'contacts_ways'},
        ]

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = AuthorisationUserForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                # return redirect('index')
                return HttpResponseRedirect(reverse('home'))
    else:
        form = AuthorisationUserForm()
    context = {'form': form, 'menu': menu}

    return render(request, 'users/authorisation.html', context)


def registration(request):
    if request.method == 'POST':
        form = RegistrationUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            auth.login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = RegistrationUserForm()
    context = {'form': form, 'menu':menu}
    return render(request, 'users/registration.html', context)


#
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     context = {
#         'title': 'Store - Профиль',
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),
#     }
#     return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:authorisation'))
