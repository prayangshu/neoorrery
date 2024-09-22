import csv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Planet, Comet, Asteroid


def home(request):
    return render(request, 'orrery/home.html')


def dashboard(request):
    # Fetch counts for celestial bodies
    total_planets = Planet.objects.count()
    total_comets = Comet.objects.count()
    total_asteroids = Asteroid.objects.count()
    total_pha = Asteroid.objects.filter(is_potentially_hazardous=True).count()

    # Total celestial bodies = sum of all categories
    total_celestial_bodies = total_planets + total_comets + total_asteroids

    # Percentage change (dummy values for now, implement real logic)
    planet_change = 2  # Example: 2% increase since last fetch
    comet_change = -1  # Example: 1% decrease
    asteroid_change = 3
    pha_change = 1
    total_celestial_bodies_change = 5

    celestial_bodies = []

    # Search and filter logic
    search_query = request.GET.get('search', '')
    filter_by = request.GET.get('filter_by', '')
    sort_by = request.GET.get('sort_by', '')

    if search_query:
        planets = Planet.objects.filter(name__icontains=search_query)
        comets = Comet.objects.filter(name__icontains=search_query)
        asteroids = Asteroid.objects.filter(name__icontains=search_query)
    else:
        planets = Planet.objects.all()
        comets = Comet.objects.all()
        asteroids = Asteroid.objects.all()

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
    }
    return render(request, 'orrery/dashboard.html', context)


def body_detail(request, pk, body_type):
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


def export_bodies_csv(request):
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
    return render(request, 'orrery/3d_view.html')


def fetch_orbital_data(request):
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
