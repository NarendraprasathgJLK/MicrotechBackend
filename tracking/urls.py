from django.urls import path
from . import views

urlpatterns = [
    path('update_stage/', views.update_stage, name='update_stage'),
    path('get_all_stage_completions/', views.get_all_stage_completions, name='get_all_stage_completions'),
]
