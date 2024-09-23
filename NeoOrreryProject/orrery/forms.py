from django import forms
from .models import Planet, Comet, Asteroid, UserProfile
from django.contrib.auth.models import User

class PlanetForm(forms.ModelForm):
    class Meta:
        model = Planet
        fields = [
            'name',
            'size',
            'distance',
            'nasa_id',
            'semi_major_axis',
            'eccentricity',
            'inclination',
            'argument_of_periapsis',
            'longitude_of_ascending_node',
            'mean_anomaly',
        ]
        widgets = {
            'size': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' km'}),
            'distance': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' km'}),
            'semi_major_axis': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' AU'}),
            'eccentricity': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'inclination': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' degrees'}),
            'argument_of_periapsis': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' degrees'}),
            'longitude_of_ascending_node': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' degrees'}),
            'mean_anomaly': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' degrees'}),
        }


class CometForm(forms.ModelForm):
    class Meta:
        model = Comet
        fields = [
            'name',
            'distance',
            'nasa_id',
            'orbital_period',
            'eccentricity',
            'inclination',
            'argument_of_periapsis',
            'longitude_of_ascending_node',
        ]
        widgets = {
            'distance': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' km'}),
            'orbital_period': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' years'}),
            'eccentricity': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'inclination': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' degrees'}),
            'argument_of_periapsis': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' degrees'}),
            'longitude_of_ascending_node': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' degrees'}),
        }


class AsteroidForm(forms.ModelForm):
    class Meta:
        model = Asteroid
        fields = [
            'name',
            'size',
            'distance',
            'nasa_id',
            'is_potentially_hazardous',
        ]
        widgets = {
            'size': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' meters'}),
            'distance': forms.NumberInput(attrs={'readonly': 'readonly', 'suffix': ' km'}),
            'is_potentially_hazardous': forms.CheckboxInput(attrs={'disabled': 'disabled'}),
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Include only the fields you want users to edit

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
