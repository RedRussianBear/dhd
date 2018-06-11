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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    xp_spent = models.IntegerField

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
        hash_source.update(self.name)
        hash_source.update(self.description)
        hash_source.update(self.home_world)

        return hash_source.hexdigest()

    def save(self, *args, **kwargs):
        if self.code is None:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CharacterElement(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)


class Skill(CharacterElement):
    TYPE = [
        ('B', 'Basic'),
        ('A', 'Advanced'),
    ]

    type = models.CharField(max_length=1, choices=TYPE)
    skilled = models.BooleanField()
    trained = models.BooleanField()
    mastered = models.BooleanField()


class Trait(CharacterElement):
    description = models.CharField(max_length=1024)


class Talent(CharacterElement):
    description = models.CharField(max_length=1024)


class Cybernetic(CharacterElement):
    effects = models.CharField(max_length=512)


class PsychicPower(CharacterElement):
    effects = models.CharField(max_length=512)

    threshold = models.IntegerField()
    focus_time = models.FloatField()
    sustain = models.BooleanField()
    range = models.IntegerField()


class Disorder(CharacterElement):
    SEVERITY = [
        ('M', 'Minor'),
        ('S', 'Severe'),
        ('A', 'Acute'),
    ]

    severity = models.CharField(max_length=1, choices=SEVERITY)
    description = models.CharField(max_length=512)


class Malignancy(CharacterElement):
    description = models.CharField(max_length=512)


class Mutation(CharacterElement):
    description = models.CharField(max_length=512)


class Weapon(CharacterElement):
    CLASS = [
        ('M', 'Melee'),
        ('T', 'Thrown'),
        ('P', 'Pistol'),
        ('B', 'Basic'),
        ('H', 'Heavy'),
    ]

    TYPE = [
        ('E', 'Energy'),
        ('X', 'Explosive'),
        ('R', 'Rending'),
        ('I', 'Impact'),
    ]

    size_class = models.CharField(max_length=1, choices=CLASS)
    damage = models.CharField(max_length=16)
    dmg_type = models.CharField(max_length=1, choices=TYPE)
    penetration = models.IntegerField()

    special = models.CharField(max_length=64)
    weight = models.FloatField()


class MeleeWeapon(Weapon):
    handedness = models.CharField(max_length=16)


class RangedWeapon(Weapon):
    effective_range = models.IntegerField(blank=True)

    semi_auto = models.IntegerField()
    full_auto = models.IntegerField()

    clip = models.IntegerField()
    reload = models.FloatField()


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = []

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs['placeholder'] = field.label
        super(CharacterForm, self).__init__(*args, **kwargs)
