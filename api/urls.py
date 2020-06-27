from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_user_details', views.get_user_details, name="get_user_details"),
    path('update_user_details', views.update_user_details,
         name="update_user_details"),
    path('get_filtered_users', views.get_filtered_users, name="get_filtered_users"),
    path('send_test_dm', views.send_test_dm, name="send_test_dm"),
    path('start_campaign', views.start_campaign, name="start_campaign"),
    path('execute_es_search_query', views.execute_es_search_query,
         name="execute_es_search_query"),
    path('click_track', views.click_track, name="click_track"),
    path('subscribe_conversion', views.subscribe_conversion,
         name="subscribe_conversion"),
    path('start_index_users', views.start_index_users, name="start_index_users"),
]
