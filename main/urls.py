"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import accounts.views
import users.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', accounts.views.user_login, name='login'),
    path('logout/', accounts.views.user_logout, name='logout'),
    path('signup/', accounts.views.user_signup, name='signup'),
    path('api/user/', users.views.get_user_profile, name='user'),
    path('api/bookings/', include('bookings.urls')),
    path('api/products/', include('products.urls')),
    path('api/services/', include('services.urls')),
    path('api/events/', include('events.urls')),
    path('api/orders/', include('orders.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
