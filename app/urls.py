from django.urls import path

from . import views

urlpatterns = [
    path('appointments/', views.appointments_view, name='appointments'),
    path('appointments_form_view/', views.appointments_form_view, name='appointments_form_view'),
    path('create_appointment_client/', views.create_appointment_client, name='create_appointment_client'),
    path('thank_you_page_view/', views.thank_you_page_view, name='thank_you_page_view_name'),
    path('management/', views.appointment_list_view, name='management'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('accounts/login/', views.custom_login_view, name='custom_login_view'),

]