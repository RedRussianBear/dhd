from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import LoginForm, Character


def main(request):
    return render(request, 'base.html', {})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('/character')

    if request.method == 'POST':
        form = LoginForm(request.POST, prefix='login')

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/character')

    else:
        form = LoginForm(prefix='login')

    return render(request, 'login.html', {'form': form})


@login_required
def view_characters(request):
    characters = Character.objects.filter(user=request.user)
    return render(request, 'characters.html', {'characters': characters})


@login_required
def edit_character(request, character_id):
    context = {}

    if character_id == 'new':
        character = Character()

    else:
        character = Character.objects.get(code=character_id)

    return render(request, 'character.html', context)
