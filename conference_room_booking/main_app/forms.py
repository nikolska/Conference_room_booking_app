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


class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'comment']
        widgets = {
            'date': forms.SelectDateWidget(),
            'comment': forms.Textarea(attrs={'cols': 30, 'rows': 3}),
        }

