from django.urls import path
from . import views


urlpatterns = [
  path('',views.room,name='room'),
  path('create-room/',views.createroom,name='create-room'),
  path('update-room/<str:pk>/',views.updateroom,name='update-room'),
  path('delete-room/<str:pk>/',views.deleteroom,name='delete-room'),
  path('delete-message/<str:pk>/',views.deletemessage,name='delete-message'),
  path('<str:pk>/',views.room_page,name='room-page'),

]