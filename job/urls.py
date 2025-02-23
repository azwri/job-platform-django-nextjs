from django.urls import path
from .views import get_all_jobs, get_job, create_job, update_job, delete_job, destroy_job

app_name = 'job'

urlpatterns = [
    path('jobs/', get_all_jobs, name='get_all_jobs'),
    path('jobs/<int:pk>/', get_job, name='get_job'),
    path('jobs/create/', create_job, name='create_job'),
    path('jobs/update/<int:pk>/', update_job, name='update_job'),
    path('jobs/delete/<int:pk>/', delete_job, name='delete_job'),
    path('jobs/destroy/<int:pk>/', destroy_job, name='destroy_job'),
    
]