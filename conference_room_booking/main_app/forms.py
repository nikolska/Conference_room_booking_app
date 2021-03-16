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
            'date': forms.DateInput(),
            'comment': forms.Textarea(attrs={'cols': 30, 'rows': 3}),
        }


class RoomSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    capacity = forms.IntegerField(min_value=0, required=False)
    projector = forms.BooleanField(required=False)

