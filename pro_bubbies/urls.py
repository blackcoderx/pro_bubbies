from django.contrib import admin
from django.urls import path,include
from base_app import views as base
from chatroom import views as chat_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',base.homepage,name='home-page'),
    path('login/',base.loginUser,name='login'),
    path('logout/',base.logoutUser,name='logout'),
    path('register/',base.register,name='register'),
    path('profile/<str:pk>/',base.profile,name='profile'),
    path('update/',chat_view.updateuser,name='update-user'),
    path('create-room/',chat_view.createroom,name='create-room'),
    path('room/',include('chatroom.urls')),
]
