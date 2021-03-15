from django import forms

from .models import Room, Reservation


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'projector']


class RoomUpdateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'projector']

