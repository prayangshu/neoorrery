from django import forms
from .models import Planet, Comet, Asteroid, UserProfile, BlogPost, Topic, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Form for Planet
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
            'size': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Size in kilometers'}),
            'distance': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Distance in kilometers'}),
            'semi_major_axis': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'AU'}),
            'eccentricity': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Eccentricity'}),
            'inclination': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Degrees'}),
            'argument_of_periapsis': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Degrees'}),
            'longitude_of_ascending_node': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Degrees'}),
            'mean_anomaly': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Degrees'}),
        }

# Form for Comet
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
            'distance': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Distance in kilometers'}),
            'orbital_period': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Period in years'}),
            'eccentricity': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Eccentricity'}),
            'inclination': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Degrees'}),
            'argument_of_periapsis': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Degrees'}),
            'longitude_of_ascending_node': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Degrees'}),
        }

# Form for Asteroid
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
            'size': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Size in meters'}),
            'distance': forms.NumberInput(attrs={'readonly': 'readonly', 'placeholder': 'Distance in kilometers'}),
            'is_potentially_hazardous': forms.CheckboxInput(attrs={'disabled': 'disabled'}),
        }

# Form for editing user profile
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Form for UserProfile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'real_time_distance', 'critical_distance']
        labels = {
            'real_time_distance': 'Set Real-Time Close Approaches Distance (KM)',
            'critical_distance': 'Set Critical Close Approaches Distance (KM)',
        }
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'real_time_distance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '100,000'}),
            'critical_distance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '10,000'}),
        }

# Form for blog post contributions
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['topic', 'title', 'content', 'thumbnail']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter blog title...', 'required': 'required'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Write your blog content here...'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# Form for adding comments to blog posts
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here...'}),
        }

# Custom UserCreationForm for Signup with Email
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Add a valid email address.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
