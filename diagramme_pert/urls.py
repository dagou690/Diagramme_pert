from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('projets:index'), name='home'),
    path('projets/', include('pert_app.urls')),
]
