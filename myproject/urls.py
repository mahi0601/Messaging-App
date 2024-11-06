# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from messaging import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.message_list, name='message_list'),
    path('respond/<int:message_id>/', views.respond_to_message, name='respond_to_message'),
    path('', include('messaging.urls')),  # Include only once and avoid recursive references
    path('api/send_message/', views.send_message_form, name='send_message_form'),
    path('claim/<int:message_id>/', views.claim_message, name='claim_message'),
]
