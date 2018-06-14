from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import LoginForm, Character, CharacterForm, SkillFormSet, TraitFormSet, TalentFormSet, CyberneticFormSet, \
    PsychicPowerFormSet, DisorderFormSet, MalignancyFormSet, MutationFormSet, ItemFormSet, MeleeWeaponFormSet, \
    RangedWeaponFormSet, \
    PasswordChangeForm


def main(request):
    return render(request, 'base.html', {})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('/character/')

    if request.method == 'POST':
        form = LoginForm(request.POST, prefix='login')

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/character/')

    else:
        form = LoginForm(prefix='login')

    return render(request, 'login.html', {'form': form})


@login_required
def select_character(request):
    characters = Character.objects.filter(user=request.user)
    return render(request, 'characters.html', {'characters': characters})


@login_required
def edit_character(request, character_id):
    if request.method == 'POST':
        if character_id == 'new':
            character_form = CharacterForm(request.POST)
        else:
            character_form = CharacterForm(request.POST, instance=Character.objects.get(code=character_id))

        if character_form.is_valid():
            character = character_form.save()

            if character.user is None:
                character.user = request.user
                character.save()

            skill_form_set = SkillFormSet(request.POST, instance=character)
            trait_form_set = TraitFormSet(request.POST, instance=character)
            talent_form_set = TalentFormSet(request.POST, instance=character)
            cybernetic_form_set = CyberneticFormSet(request.POST, instance=character)
            psychic_power_form_set = PsychicPowerFormSet(request.POST, instance=character)
            disorder_form_set = DisorderFormSet(request.POST, instance=character)
            malignancy_form_set = MalignancyFormSet(request.POST, instance=character)
            mutation_form_set = MutationFormSet(request.POST, instance=character)
            item_form_set = ItemFormSet(request.POST, instance=character)
            melee_weapon_form_set = MeleeWeaponFormSet(request.POST, instance=character)
            ranged_weapon_form_set = RangedWeaponFormSet(request.POST, instance=character)

            if skill_form_set.is_valid() and trait_form_set.is_valid() and talent_form_set.is_valid() \
                    and cybernetic_form_set.is_valid() and psychic_power_form_set.is_valid() \
                    and disorder_form_set.is_valid() and malignancy_form_set.is_valid() \
                    and mutation_form_set.is_valid() and item_form_set.is_valid() and melee_weapon_form_set.is_valid() \
                    and ranged_weapon_form_set.is_valid():
                skill_form_set.save()
                trait_form_set.save()
                talent_form_set.save()
                cybernetic_form_set.save()
                psychic_power_form_set.save()
                disorder_form_set.save()
                malignancy_form_set.save()
                mutation_form_set.save()
                item_form_set.save()
                melee_weapon_form_set.save()
                ranged_weapon_form_set.save()

                character_id = character.code

                return redirect('/character/%s/' % character_id)

        else:
            character = Character()

            skill_form_set = SkillFormSet(instance=character)
            trait_form_set = TraitFormSet(instance=character)
            talent_form_set = TalentFormSet(instance=character)
            cybernetic_form_set = CyberneticFormSet(instance=character)
            psychic_power_form_set = PsychicPowerFormSet(instance=character)
            disorder_form_set = DisorderFormSet(instance=character)
            malignancy_form_set = MalignancyFormSet(instance=character)
            mutation_form_set = MutationFormSet(instance=character)
            item_form_set = ItemFormSet(instance=character)
            melee_weapon_form_set = MeleeWeaponFormSet(instance=character)
            ranged_weapon_form_set = RangedWeaponFormSet(instance=character)

    else:
        if character_id == 'new':
            character = Character()
            character_form = CharacterForm()

        else:
            character = Character.objects.get(code=character_id)
            character_form = CharacterForm(instance=character)

        skill_form_set = SkillFormSet(instance=character)
        trait_form_set = TraitFormSet(instance=character)
        talent_form_set = TalentFormSet(instance=character)
        cybernetic_form_set = CyberneticFormSet(instance=character)
        psychic_power_form_set = PsychicPowerFormSet(instance=character)
        disorder_form_set = DisorderFormSet(instance=character)
        malignancy_form_set = MalignancyFormSet(instance=character)
        mutation_form_set = MutationFormSet(instance=character)
        item_form_set = ItemFormSet(instance=character)
        melee_weapon_form_set = MeleeWeaponFormSet(instance=character)
        ranged_weapon_form_set = RangedWeaponFormSet(instance=character)

    context = {
        'character_id': character_id,
        'character_form': character_form,
        'skill_form_set': skill_form_set,
        'trait_form_set': trait_form_set,
        'talent_form_set': talent_form_set,
        'cybernetic_form_set': cybernetic_form_set,
        'psychic_power_form_set': psychic_power_form_set,
        'disorder_form_set': disorder_form_set,
        'malignancy_form_set': malignancy_form_set,
        'mutation_form_set': mutation_form_set,
        'item_form_set': item_form_set,
        'melee_weapon_form_set': melee_weapon_form_set,
        'ranged_weapon_form_set': ranged_weapon_form_set,
    }

    return render(request, 'character.html', context)


@login_required
def settings(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.POST, prefix='password_change')
        if password_change_form.is_valid():
            request.user.set_password(password_change_form.cleaned_data['new_password'])
            request.user.save()

    password_change_form = PasswordChangeForm(prefix='password_change')

    context = {
        'password_change_form': password_change_form
    }
    return render(request, 'settings.html', context)
