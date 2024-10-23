from django.urls import path
from . import views

urlpatterns = [
    path('configure-email/', views.configure_email, name='configure_email'),
    path('success/', views.success, name='success'),
    path('fetch-emails/', views.fetch_emails_view, name='fetch_emails'),
    path('emails/', views.email_list, name='email_list'),
    path('emails/<int:email_id>/', views.email_detail, name='email_detail'),
]