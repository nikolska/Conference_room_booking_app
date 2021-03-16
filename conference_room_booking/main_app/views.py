from datetime import date

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import View, FormView, CreateView, UpdateView

from .forms import RoomCreateForm, RoomUpdateForm, ReservationCreateForm, SearchRoomForm
from .models import Room, Reservation


class RoomsListView(View):
    def get(self, request, *args, **kwargs):
        rooms_list = get_list_or_404(Room.objects.order_by('name'))

        for room in rooms_list:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = date.today() in reservation_dates

        ctx = {'rooms_list': rooms_list}
        return render(request, 'main_app/rooms_list.html', ctx)


class RoomDetailsView(FormView):
    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, pk=kwargs['room_id'])
        reservations = room.reservation_set.filter(date__gte=str(date.today())).order_by('date')
        ctx = {
            'room': room,
            'reservations': reservations
        }
        return render(request, 'room_details.html', ctx)


class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomUpdateForm
    template_name = 'main_app/room_update_form.html'
    success_url = reverse_lazy('rooms_list')

    def get_object(self, queryset=None):
        return Room.objects.get(pk=self.kwargs['room_id'])


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


class RoomReserveView(CreateView):
    model = Reservation
    template_name = 'main_app/reservation_form.html'
    form_class = ReservationCreateForm
    success_url = reverse_lazy('rooms_list')

    def get_context_data(self, **kwargs):
        room = get_object_or_404(Room, pk=self.kwargs['room_id'])
        ctx = super().get_context_data(**kwargs)
        ctx["room"] = room
        return ctx


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomCreateForm
    template_name = 'main_app/room_form.html'
    success_url = reverse_lazy('rooms_list')


# class SearchRoomFormView(FormView):
#     model = Room
#     form_class = SearchRoomForm
#     template_name = 'main_app/room_list.html'
#     success_url = reverse_lazy('rooms_list')

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
