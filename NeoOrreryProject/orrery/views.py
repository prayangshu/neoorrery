import csv
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Planet, Comet, Asteroid, CelestialBodyStats, UserProfile, NasaDataLog
from .forms import EditProfileForm, UserProfileForm
from .management.commands.check_close_approaches import Command as CloseApproachesCommand


@login_required
def dashboard(request):
    """Dashboard view to display celestial bodies statistics."""
    total_planets = Planet.objects.count()
    total_comets = Comet.objects.count()
    total_asteroids = Asteroid.objects.count()
    total_pha = Asteroid.objects.filter(is_potentially_hazardous=True).count()

    total_celestial_bodies = total_planets + total_comets + total_asteroids

    latest_stats = CelestialBodyStats.objects.last()

    if latest_stats:
        planet_change = CelestialBodyStats.calculate_change(latest_stats.total_planets, total_planets)
        comet_change = CelestialBodyStats.calculate_change(latest_stats.total_comets, total_comets)
        asteroid_change = CelestialBodyStats.calculate_change(latest_stats.total_asteroids, total_asteroids)
        pha_change = CelestialBodyStats.calculate_change(latest_stats.total_pha, total_pha)
        total_celestial_bodies_change = CelestialBodyStats.calculate_change(latest_stats.total_bodies, total_celestial_bodies)
    else:
        planet_change = comet_change = asteroid_change = pha_change = total_celestial_bodies_change = 0

    new_stats = CelestialBodyStats(
        total_bodies=total_celestial_bodies,
        total_planets=total_planets,
        total_comets=total_comets,
        total_asteroids=total_asteroids,
        total_pha=total_pha
    )
    new_stats.save_stats(latest_stats)

    # Celestial bodies search, filter, and sort logic
    celestial_bodies = []
    search_query = request.GET.get('search', '')
    filter_by = request.GET.get('filter_by', '')
    sort_by = request.GET.get('sort_by', '')

    planets = Planet.objects.all()
    comets = Comet.objects.all()
    asteroids = Asteroid.objects.all()

    if search_query:
        planets = planets.filter(name__icontains=search_query)
        comets = comets.filter(name__icontains=search_query)
        asteroids = asteroids.filter(name__icontains=search_query)

    if filter_by == 'Planet':
        celestial_bodies = list(planets)
    elif filter_by == 'Comet':
        celestial_bodies = list(comets)
    elif filter_by == 'Asteroid':
        celestial_bodies = list(asteroids.filter(is_potentially_hazardous=False))
    elif filter_by == 'PHA':
        celestial_bodies = list(asteroids.filter(is_potentially_hazardous=True))
    else:
        celestial_bodies = list(planets) + list(comets) + list(asteroids)

    if sort_by == 'name':
        celestial_bodies = sorted(celestial_bodies, key=lambda x: x.name)
    elif sort_by == 'distance_from_earth':
        celestial_bodies = sorted(celestial_bodies, key=lambda x: x.distance)

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    is_opted_in = user_profile.is_opted_in

    context = {
        'celestial_bodies': celestial_bodies,
        'total_celestial_bodies': total_celestial_bodies,
        'total_planets': total_planets,
        'total_comets': total_comets,
        'total_asteroids': total_asteroids,
        'total_pha': total_pha,
        'total_celestial_bodies_change': total_celestial_bodies_change,
        'planets_change': planet_change,
        'comets_change': comet_change,
        'asteroids_change': asteroid_change,
        'pha_change': pha_change,
        'search_query': search_query,
        'filter_by': filter_by,
        'sort_by': sort_by,
        'is_opted_in': is_opted_in,
    }

    return render(request, 'orrery/dashboard.html', context)


@login_required
def profile(request):
    """View for user's profile information."""
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'orrery/profile.html', {'user_profile': user_profile})


@login_required
def edit_profile(request):
    """View for users to edit their profile information including profile picture."""
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'orrery/edit_profile.html', {'form': form, 'profile_form': profile_form})


def body_detail(request, pk, body_type):
    """Displays detailed information about a celestial body."""
    if body_type == 'Planet':
        body = get_object_or_404(Planet, pk=pk)
        template = 'orrery/planets_body_detail.html'
    elif body_type == 'Comet':
        body = get_object_or_404(Comet, pk=pk)
        template = 'orrery/comets_body_detail.html'
    elif body_type == 'Asteroid':
        body = get_object_or_404(Asteroid, pk=pk)
        template = 'orrery/pha_body_detail.html' if body.is_potentially_hazardous else 'orrery/asteroids_body_detail.html'
    else:
        return HttpResponse('Body type not found', status=404)

    return render(request, template, {'body': body})


@login_required
def toggle_alert_subscription(request):
    """Toggles the user's subscription to Close Approaches Alert."""
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.is_opted_in = not user_profile.is_opted_in
    user_profile.save()

    if user_profile.is_opted_in:
        messages.success(request, 'You have successfully opted into Close Approaches Alert.')
    else:
        messages.success(request, 'You have opted out of Close Approaches Alert.')

    return redirect('dashboard')


@login_required
def get_close_approaches_now(request):
    """Allows users to get a personal close approach alert."""
    if request.method == 'POST':
        close_approaches = CloseApproachesCommand()
        close_approaches.handle()

        # Log this action
        NasaDataLog.objects.create(user=request.user, action='Requested Close Approaches Alert')

        messages.success(request, 'Close Approaches Alert sent to you!')
        return redirect('dashboard')
    else:
        return HttpResponseNotAllowed(['POST'])


def export_bodies_csv(request):
    """Exports celestial bodies data to CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="celestial_bodies.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Body Type', 'Size (meters)', 'Distance (km)', 'Last Updated'])

    planets = Planet.objects.all()
    comets = Comet.objects.all()
    asteroids = Asteroid.objects.all()

    for body in planets:
        writer.writerow([body.name, 'Planet', body.size, body.distance, body.last_updated])

    for body in comets:
        writer.writerow([body.name, 'Comet', body.size, body.distance, body.last_updated])

    for body in asteroids:
        body_type = 'PHA' if body.is_potentially_hazardous else 'Asteroid'
        writer.writerow([body.name, body_type, body.size, body.distance, body.last_updated])

    return response


def three_d_view(request):
    """Render the 3D view of celestial bodies."""
    return render(request, 'orrery/3d_view.html')


def fetch_orbital_data(request):
    """Fetches and returns orbital data for celestial bodies."""
    planets = Planet.objects.all()
    comets = Comet.objects.all()
    asteroids = Asteroid.objects.all()

    orbital_data = []

    for planet in planets:
        position = compute_orbital_position(planet)
        orbital_data.append({
            'name': planet.name,
            'position': position,
            'body_type': 'Planet'
        })

    for comet in comets:
        position = compute_orbital_position(comet)
        orbital_data.append({
            'name': comet.name,
            'position': position,
            'body_type': 'Comet'
        })

    for asteroid in asteroids:
        position = compute_orbital_position(asteroid)
        body_type = 'PHA' if asteroid.is_potentially_hazardous else 'Asteroid'
        orbital_data.append({
            'name': asteroid.name,
            'position': position,
            'body_type': body_type
        })

    return JsonResponse({'orbital_data': orbital_data})


def signup(request):
    """Handles user signup."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'orrery/signup.html', {'form': form})


@login_required
def nasa_data_logs(request):
    """View to display the NASA data logs."""
    logs = NasaDataLog.objects.all().order_by('-timestamp')
    return render(request, 'orrery/nasa_data_logs.html', {'logs': logs})
