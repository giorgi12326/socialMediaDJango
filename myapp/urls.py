from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name = "home"),
    path('room/<str:pk>/',views.room,name = 'room'),
    path('create-room',views.createRoom),
    path('update-room/<str:pk>/',views.updateRoom,name = "updateRoom"),
    path('delete-room/<str:pk>/',views.deleteRoom,name = "deleteRoom"),
    path('login/',views.loginPage,name = 'login'),
    path('logout/',views.logoutPage,name = "logout"),
    path('register/',views.registerPage,name = 'register'),
    path('delete-message/<str:pk>/',views.deleteMessage,name = 'delete-message'),
    path('user-profile/<str:pk>/',views.userProfile,name = 'profile'),
    path('topics/',views.topicset,name = 'topics'),
    path('settings/',views.settingsPage,name = 'settings'),
]