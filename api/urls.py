from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_user_details', views.get_user_details, name="get_user_details"),
    path('update_user_details', views.update_user_details,
         name="update_user_details"),
    path('get_filtered_users', views.get_filtered_users, name="get_filtered_users"),
]
