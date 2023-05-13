from django.contrib import admin
from django.urls import path, include
from data_sync.views import *

urlpatterns = [
    path('data_sync/', online_data_sync, name='data_sync'),
    path('intranet/list/', get_intranet_config, name='get_intranet_config'),
    path('intranet/data/', get_intranet_db, name='get_intranet_db'),
    path('online/data/', get_online_db, name='get_online_db'),
    path('intranet/add/', add_intranet_config, name='add_intranet_config'),
    path('intranet/edit/', update_intranet_config, name='update_intranet_config'),
    path('intranet/delete/', delete_intranet_config, name='delete_intranet_config'),
    path('query/', query,name='query'),

]
