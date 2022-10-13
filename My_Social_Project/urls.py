from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static , staticfiles_urlpatterns
from App_Posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('accounts/',include('App_Login.urls')),
    path('post/',include('App_Posts.urls')),
]

urlpatterns = urlpatterns + static (settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()