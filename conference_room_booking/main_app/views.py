from datetime import date

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse

from .models import Room, Reservation


def rooms_list_view(request):
    rooms_list = get_list_or_404(Room)
    ctx = {'rooms_list': rooms_list}
    return render(request, 'rooms_list.html', ctx)


def room_details_view(request, room_id):
    pass


def room_modify_view(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'GET':
        ctx = {'room': room}
        return render(request, 'room_modify.html', ctx)
    elif request.method == 'POST':
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        if not name:
            ctx = {'message': 'Name can not be empty!'}
            return render(request, 'room_modify.html', ctx)
        if name != room.name and Room.objects.filter(name=name):
            ctx = {'message': 'Conference room with this name is already exist!'}
            return render(request, 'room_modify.html', ctx)
        if len(name) > 255:
            ctx = {'message': 'Room name is too long. Must be less than 255 characters!'}
            return render(request, 'room_modify.html', ctx)
        if not capacity:
            capacity = 0
        if int(capacity) < 0:
            ctx = {'message': 'Room capacity must not be less than zero!'}
            return render(request, 'room_modify.html', ctx)
        if projector == 'on':
            projector = True
        else:
            projector = False
        room.name = name
        room.capacity = capacity
        room.projector = projector
        room.save()
        return HttpResponseRedirect(reverse('rooms_list'))


def room_delete_view(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'GET':
        ctx = {'room': room}
        return render(request, 'delete_room.html', ctx)
    elif request.method == 'POST':
        room.delete()
        return HttpResponseRedirect(reverse('rooms_list'))


def room_reserve_view(request, room_id):
    # room = Room.objects.get(pk=room_id)
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'GET':
        ctx = {'room': room}
        return render(request, 'room_reservation.html', ctx)
    elif request.method == 'POST':
        reservation_date = request.POST.get('date')
        comment = request.POST.get('comment')
        if not reservation_date:
            ctx = {'message': 'Reservation date cannot be empty!'}
            return render(request, 'room_reservation.html', ctx)
        if reservation_date < str(date.today()):
            ctx = {'message': 'Reservation date cannot be less than today!'}
            return render(request, 'room_reservation.html', ctx)
        if Reservation.objects.filter(room=room, date=reservation_date):
            ctx = {'message': 'This conference room is already booked on this day!'}
            return render(request, "room_reservation.html", ctx)
        Reservation.objects.create(
            room=room,
            date=reservation_date,
            comment=comment
        )
        return HttpResponseRedirect(reverse('rooms_list'))


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
        if len(name) > 255:
            ctx = {'message': 'Room name is too long. Must be less than 255 characters!'}
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
