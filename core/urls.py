from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.log_in, name='login'),
    path('character/', views.select_character, name='select_character'),
    path('character/<str:character_id>/', views.edit_character, name='character'),
]
