from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('message_list', views.message_list, name='message_list'),
    # path('ws/messages/', views.ws_messages, name='ws_messages'),
    path('message/respond/<int:message_id>/', views.respond_to_message, name='respond_to_message'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # API routes
    path('api/send_message/', views.send_message, name='send_message'),
    path('api/get_messages/', views.get_messages, name='get_messages'),
    path('api/send_message/', views.send_message_form, name='send_message_form'),
    path('claim/<int:message_id>/', views.claim_message, name='claim_message'),
]
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('messages/', views.get_messages, name='get_messages'),
#     path('messages/respond/', views.respond_to_message_api, name='respond_to_message'),
#     path('messages/search/', views.search_messages, name='search_messages'),
#     path('messages/receive/', views.receive_message, name='receive_message'),
# ]
