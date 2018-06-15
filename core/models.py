from django.contrib.auth.models import User
from django.db import models
from django import forms
from hashlib import sha256


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    username.widget.attrs['placeholder'] = 'Username'
    password.widget.attrs['placeholder'] = 'Password'


class Character(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    race = models.CharField(max_length=32, blank=True)
    home_world = models.CharField(max_length=64, blank=True)
    gender = models.CharField(max_length=32, blank=True)
    build = models.CharField(max_length=32, blank=True)

    height = models.CharField(max_length=64, blank=True)
    weight = models.CharField(max_length=32, blank=True)
    age = models.CharField(max_length=32, blank=True)

    skin_color = models.CharField(max_length=64, blank=True)
    hair_color = models.CharField(max_length=64, blank=True)
    eye_color = models.CharField(max_length=64, blank=True)

    quirk = models.CharField(max_length=128, blank=True)
    divination = models.CharField(max_length=128, blank=True)
    alignment = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=256, blank=True)

    career = models.CharField(max_length=128, blank=True)
    rank = models.CharField(max_length=128, blank=True)

    weapon_skill = models.IntegerField()
    ballistic_skill = models.IntegerField()
    strength = models.IntegerField()
    toughness = models.IntegerField()
    agility = models.IntegerField()
    intelligence = models.IntegerField()
    perception = models.IntegerField()
    willpower = models.IntegerField()
    fellowship = models.IntegerField()

    xp = models.IntegerField()
    xp_spent = models.IntegerField()

    fate = models.IntegerField()
    insanity = models.IntegerField()
    corruption = models.IntegerField()
    wealth = models.IntegerField()

    degree_of_madness = models.CharField(max_length=64, blank=True)
    degree_of_corruption = models.CharField(max_length=64, blank=True)

    tot_wounds = models.IntegerField()
    cur_wounds = models.IntegerField()

    background = models.CharField(max_length=1024, blank=True)
    notes = models.CharField(max_length=1024, blank=True)
    injuries = models.CharField(max_length=512, blank=True)

    def generate_code(self):
        hash_source = sha256()
        hash_source.update(self.name.encode('utf8'))
        hash_source.update(self.description.encode('utf8'))
        hash_source.update(self.home_world.encode('utf8'))

        return hash_source.hexdigest()

    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CharacterElement(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Skill(CharacterElement):
    TYPE = [
        ('', ''),
        ('B', 'B'),
        ('A', 'A'),
    ]

    type = models.CharField(max_length=1, choices=TYPE, default='')
    skilled = models.BooleanField()
    trained = models.BooleanField()
    mastered = models.BooleanField()


class Trait(CharacterElement):
    description = models.CharField(max_length=1024, blank=True)


class Talent(CharacterElement):
    description = models.CharField(max_length=1024, blank=True)


class Cybernetic(CharacterElement):
    effects = models.CharField(max_length=512, blank=True)


class PsychicPower(CharacterElement):
    effects = models.CharField(max_length=512, blank=True)

    threshold = models.IntegerField()
    focus_time = models.FloatField()
    sustain = models.BooleanField()
    range = models.IntegerField()


class Disorder(CharacterElement):
    SEVERITY = [
        ('', ''),
        ('M', 'Minor'),
        ('S', 'Severe'),
        ('A', 'Acute'),
    ]

    severity = models.CharField(max_length=1, choices=SEVERITY, default='')
    description = models.CharField(max_length=512, blank=True)


class Malignancy(CharacterElement):
    description = models.CharField(max_length=512, blank=True)


class Mutation(CharacterElement):
    description = models.CharField(max_length=512, blank=True)


class Item(CharacterElement):
    location = models.CharField(max_length=32)
    weight = models.FloatField()


class Weapon(CharacterElement):
    CLASS = [
        ('', ''),
        ('M', 'Melee'),
        ('T', 'Thrown'),
        ('P', 'Pistol'),
        ('B', 'Basic'),
        ('H', 'Heavy'),
    ]

    TYPE = [
        ('', ''),
        ('E', 'Energy'),
        ('X', 'Explosive'),
        ('R', 'Rending'),
        ('I', 'Impact'),
    ]

    size_class = models.CharField(max_length=1, choices=CLASS, default='')
    damage = models.CharField(max_length=16)
    dmg_type = models.CharField(max_length=1, choices=TYPE, default='')
    penetration = models.IntegerField()

    special = models.CharField(max_length=64, blank=True)
    weight = models.FloatField()

    class Meta:
        abstract = True


class MeleeWeapon(Weapon):
    handedness = models.CharField(max_length=16, blank=True)


class RangedWeapon(Weapon):
    effective_range = models.IntegerField(blank=True)

    semi_auto = models.IntegerField()
    full_auto = models.IntegerField()

    clip = models.IntegerField()
    reload = models.FloatField()


class CharacterForm(forms.ModelForm):
    basic_skills = [
        'Awareness (Per)',
        'Barter (Fel)',
        'Carouse (T)',
        'Charm (Fel)',
        'Climb (Str)',
        'Concealment (Ag)',
        'Contortionist (Ag)',
        'Deceive (Fel)',
        'Disguise (Fel)',
        'Dodge (Ag)',
        'Evaluate (Int)',
        'Gamble (Int)',
        'Inquiry (Fel)',
        'Intimidate (Str)',
        'Logic (Int)',
        'Scrutiny (Per)',
        'Search (Per)',
        'Silent Move (Ag)',
        'Swim (Str)'
    ]

    groups = {
        'top': [[('race', 1), ('home_world', 2), ('career', 2), ('rank', 2)],
                [('gender', 1), ('build', 1), ('height', 1), ('weight', 1)],
                [('skin_color', 1), ('hair_color', 1), ('eye_color', 1), ('age', 1)],
                [('alignment', 1), ('divination', 5)],
                [('description', 1), ]],
        'characteristics': ['weapon_skill', 'ballistic_skill', 'strength', 'toughness', 'agility', 'intelligence',
                            'perception', 'willpower', 'fellowship'],
        'insanity': ['insanity', 'degree_of_madness'],
        'corruption': ['corruption', 'degree_of_corruption'],
        'wounds': ['tot_wounds', 'cur_wounds']
    }

    melee_weapon = [
        ['name'],
        ['size_class', 'damage', 'dmg_type', 'penetration'],
        ['special', 'weight']
    ]

    ranged_weapon = [
        ['name'],
        ['size_class', 'damage', 'dmg_type', 'penetration'],
        ['effective_range', 'semi_auto', 'full_auto', 'clip', 'reload'],
        ['special', 'weight']
    ]

    abbr = {
        'weapon_skill': 'WS',
        'ballistic_skill': 'BS',
        'strength': 'Str',
        'toughness': 'T',
        'agility': 'Ag',
        'intelligence': 'Int',
        'perception': 'Per',
        'willpower': 'WP',
        'fellowship': 'Fel',

        'size_class': 'Class',
        'damage': 'Dmg',
        'dmg_type': 'Type',
        'penetration': 'Pen',
        'effective_range': 'Range',
        'reload': 'Rld',
        'weight': 'Wt',
        'semi_auto': 'S/',
        'full_auto': '/'

    }

    class Meta:
        model = Character
        fields = ['name', 'race', 'home_world', 'gender', 'build', 'height', 'weight', 'age', 'skin_color',
                  'hair_color', 'eye_color', 'quirk', 'divination', 'alignment', 'description', 'career', 'rank',
                  'weapon_skill', 'ballistic_skill', 'strength', 'toughness', 'agility', 'intelligence', 'perception',
                  'willpower', 'fellowship', 'xp', 'xp_spent', 'fate', 'insanity', 'corruption', 'wealth',
                  'degree_of_madness', 'degree_of_corruption', 'tot_wounds', 'cur_wounds', 'background', 'notes',
                  'injuries']
        widgets = {
            'background': forms.Textarea(attrs={'cols': 10, 'rows': 10}),
            'injuries': forms.Textarea(attrs={'cols': 10, 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs['placeholder'] = field.label

        for characteristic in self.groups['characteristics']:
            # noinspection PyTypeChecker
            self.base_fields[characteristic].widget.attrs['placeholder'] = self.abbr[characteristic]

        super(CharacterForm, self).__init__(*args, **kwargs)


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    new_password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm New Password')

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs['placeholder'] = field.label

        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(PasswordChangeForm, self).is_valid()
        if not valid:
            return False

        if not self.cleaned_data['new_password'] == self.cleaned_data['new_password_confirm']:
            self.add_error('new_password_confirm', 'Password and confirmation don not match.')
            return False

        return True
