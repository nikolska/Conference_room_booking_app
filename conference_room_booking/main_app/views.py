from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404
from django.urls import reverse

from .models import Room


def main_page_view(request):
    return render(request, 'home_page.html')


def rooms_list_view(request):
    rooms_list = get_list_or_404(Room)
    ctx = {'rooms_list': rooms_list}
    return render(request, 'rooms_list.html', ctx)


def room_details_view(request, room_id):
    pass


def room_modify_view(request, room_id):
    pass


def room_delete_view(request, room_id):
    pass


def room_reserve_view(request, room_id):
    pass


def add_new_room(request):
    if request.method == 'GET':
        return render(request, 'add_new_room.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        if not name:
            ctx = {'message': 'Name can not be empty!'}
            return render(request, 'add_new_room.html', ctx)
        if Room.objects.filter(name=name):
            ctx = {'message': 'Conference room with this name is already exist!'}
            return render(request, 'add_new_room.html', ctx)
        if not capacity:
            capacity = 0

        if int(capacity) < 0:
            ctx = {'message': 'Room capacity must not be less than zero!'}
            return render(request, 'add_new_room.html', ctx)
        if projector == 'on':
            projector = True
        else:
            projector = False
        Room.objects.create(
            name=name,
            capacity=int(capacity),
            projector=projector
        )
        return HttpResponseRedirect(reverse('main_page'))
