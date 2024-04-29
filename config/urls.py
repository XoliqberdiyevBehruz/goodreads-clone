from django.contrib import admin
from django.urls import path, include
from .views import landing_page, home_page
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='main'),
    path('home/', home_page, name='home'),

    # API URLS
    path('api/', include('api.urls')),
    
    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
