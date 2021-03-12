from datetime import date

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.views.generic import View

from .models import Room, Reservation


class RoomsListView(View):
    def get(self, request, *args, **kwargs):
        rooms_list = get_list_or_404(Room.objects.order_by('name'))

        for room in rooms_list:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = date.today() in reservation_dates

        ctx = {'rooms_list': rooms_list}
        return render(request, 'rooms_list.html', ctx)


class RoomDetailsView(View):
    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, pk=kwargs['room_id'])
        reservations = room.reservation_set.filter(date__gte=str(date.today())).order_by('date')
        ctx = {
            'room': room,
            'reservations': reservations
        }
        return render(request, 'room_details.html', ctx)


class RoomModifyView(View):
    def get_room(self, **kwargs):
        room = get_object_or_404(Room, pk=kwargs['room_id'])
        return room

    def get(self, request, *args, **kwargs):
        room = self.get_room(**kwargs)
        ctx = {'room': room}
        return render(request, 'room_modify.html', ctx)

    def post(self, request, *args, **kwargs):
        room = self.get_room(**kwargs)
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector') == 'on'

        if not name:
            ctx = {'message': 'Name can not be empty!'}
            return render(request, 'room_modify.html', ctx)
        if name != room.name and Room.objects.filter(name=name):
            ctx = {'message': 'Conference room with this name is already exist!'}
            return render(request, 'room_modify.html', ctx)
        if len(name) > 255:
            ctx = {'message': 'Room name is too long. Must be less than 255 characters!'}
            return render(request, 'room_modify.html', ctx)
        if capacity < 0:
            ctx = {'message': 'Room capacity must not be less than zero!'}
            return render(request, 'room_modify.html', ctx)

        room.name = name
        room.capacity = capacity
        room.projector = projector
        room.save()
        return HttpResponseRedirect(reverse('rooms_list'))


class RoomDeleteView(View):
    def get_room(self, **kwargs):
        room = get_object_or_404(Room, pk=kwargs['room_id'])
        return room

    def get(self, request, *args, **kwargs):
        ctx = {'room': self.get_room(**kwargs)}
        return render(request, 'delete_room.html', ctx)

    def post(self, request, *args, **kwargs):
        btn = request.POST.get('btn')
        if btn == 'Yes':
            self.get_room(**kwargs).delete()
        return HttpResponseRedirect(reverse('rooms_list'))


class RoomReserveView(View):
    def get_room(self, **kwargs):
        room = get_object_or_404(Room, pk=kwargs['room_id'])
        return room

    def get(self, request, *args, **kwargs):
        room = self.get_room(**kwargs)
        reservations = Reservation.objects.filter(room=room)
        ctx = {
            'room': room,
            'reservations': reservations
        }
        return render(request, 'room_reservation.html', ctx)

    def post(self, request, *args, **kwargs):
        room = self.get_room(**kwargs)
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


class AddNewRoomView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_new_room.html')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector') == 'on'

        if not name:
            ctx = {'message': 'Name can not be empty!'}
            return render(request, 'add_new_room.html', ctx)
        if Room.objects.filter(name=name):
            ctx = {'message': 'Conference room with this name is already exist!'}
            return render(request, 'add_new_room.html', ctx)
        if len(name) > 255:
            ctx = {'message': 'Room name is too long. Must be less than 255 characters!'}
            return render(request, 'add_new_room.html', ctx)
        if capacity < 0:
            ctx = {'message': 'Room capacity must not be less than zero!'}
            return render(request, 'add_new_room.html', ctx)

        Room.objects.create(
            name=name,
            capacity=int(capacity),
            projector=projector
        )
        return HttpResponseRedirect(reverse('rooms_list'))


class SearchRoomView(View):
    def get(self, request, *args, **kwargs):
        rooms_list = Room.objects.all()
        name = request.GET.get('name')
        min_capacity = request.GET.get('min_capacity')
        min_capacity = int(min_capacity) if min_capacity else 0
        projector = request.GET.get('projector') == 'on'

        if name:
            rooms_list = rooms_list.filter(name=name)
        if min_capacity:
            rooms_list = rooms_list.filter(capacity__gte=min_capacity)
        if projector:
            rooms_list = rooms_list.filter(projector=projector)

        for room in rooms_list:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = str(date.today()) in reservation_dates

        ctx = {
            'rooms_list': rooms_list,
            'date': date.today()
        }
        return render(request, 'found_room.html', ctx)
