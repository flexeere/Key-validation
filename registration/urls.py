from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterCompanyView.as_view(), name='register_company'),
    path('verify/<str:token>/', views.VerifyKeyView.as_view(), name='verify_email'),
]
