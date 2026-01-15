from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list_view, name='list'),
    path('create/', views.job_create_view, name='create'),
    path('<int:job_id>/update/', views.job_update_view, name='update'),
    path('<int:job_id>/delete/', views.job_delete_view, name='delete'),
]
