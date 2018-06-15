from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.log_in, name='login'),
    path('settings/', views.settings, name='settings'),
    path('delete/<str:object_type>/<int:object_id>/', views.delete_object, name='delete'),
    path('character/', views.select_character, name='select_character'),
    path('character/<str:character_id>/', views.edit_character, name='character'),
]
