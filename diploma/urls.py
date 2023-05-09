from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    
    path('', include('playground.urls')),
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls'))
]
