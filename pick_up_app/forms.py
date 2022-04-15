from django import forms
from django.forms import ModelForm

# Team Table
from .models import PickupTeam, Games

# Error Handling
from django.core.exceptions import ValidationError


# Registration Form
class NewPickupUserForm(ModelForm):
    class Meta:
        model = PickupTeam

        # These are the attributes to be stored
        fields = (
            'teamname',
            'email',
            'password',
            'checkpassword',
            'longitude',
            'latitude',)

        # This is what the form displays them as
        labels = {
            'teamname': "New Team Name:",
            'email': "Registration Email:",
            'password': "Password:",
            'checkpassword': "Password Confirmation:",
            'longitude': "Longitude:",
            'latitude': "Latitude:",
        }

    ##########################################################
    # Handles cleaning data of form / checking accurate data
    ##########################################################
    def clean(self):

        # initial clean of form data
        f = self.cleaned_data

        # gets some of the form fields
        password1 = f.get("password")
        password2 = f.get("checkpassword")
        latitude = f.get("latitude")
        longitude = f.get("longitude")

        # validate passwords
        if password1 != password2:
            raise ValidationError("ERROR: Passwords are mismatched")

        # validate register email
        if PickupTeam.objects.filter(email=f.get("email")):
            raise ValidationError("ERROR: A Team Captain has already registered this email address")

        # validate teamname
        if PickupTeam.objects.filter(teamname=f.get("teamname")):
            raise ValidationError("ERROR: This team name has already been taken")

        # validate latitude
        if latitude < -90 or latitude > 90:
            raise ValidationError("ERROR: Latitude must be within -90 to 90")

        # validate longitude
        if longitude < -180 or longitude > 180:
            raise ValidationError("ERROR: Longitude must be within -180 to 180")


class GameDropDown(forms.ModelForm):
    game = forms.CharField(label='Choose game: ', widget=forms.Select(my_games=Games.objects.all()))