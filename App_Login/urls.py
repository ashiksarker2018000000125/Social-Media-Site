from django.urls import path
from App_Login import views

app_name = 'App_Login'

urlpatterns = [
    path('singup/',views.sing_up, name='singup'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('edit/',views.edit_Profile,name='edit'),
    path('profile',views.profile, name='profile'),
    path('user/<username>/',views.user,name='user'),
    path('follow/<username>',views.follow,name='follow'),
    path('unfollow/<username>',views.unfollow,name='unfollow'),
]