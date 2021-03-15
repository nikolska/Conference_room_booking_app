"""conference_room_booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path

from main_app.views import (
    RoomsListView, RoomDetailsView, RoomUpdateView, RoomDeleteView, RoomReserveView, RoomCreateView, SearchRoomFormView
)


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    re_path(r'^$', RoomsListView.as_view(), name='rooms_list'),
    re_path(r'^room/(?P<room_id>\d+)/$', RoomDetailsView.as_view(), name='room_details'),
    re_path(r'^room/modify/(?P<room_id>\d+)/$', RoomUpdateView.as_view(), name='room_modify'),
    re_path(r'^room/delete/(?P<room_id>\d+)/$', RoomDeleteView.as_view(), name='room_delete'),
    re_path(r'^room/reserve/(?P<room_id>\d+)/$', RoomReserveView.as_view(), name='room_reserve'),
    re_path(r'^room/new/$', RoomCreateView.as_view(), name='add_new_room'),
    re_path(r'^search/$', SearchRoomFormView.as_view(), name='search_room'),
]
