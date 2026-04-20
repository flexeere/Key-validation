from django.contrib import admin
from django.urls import path, include
admin.site.site_header = "Flexeere Secure Administration"
admin.site.site_title = "Flexeere Admin Portal"
admin.site.index_title = "Welcome to Flexeere Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('registration.urls')),
]
