import csv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Planet, Comet, Asteroid


def home(request):
    return render(request, 'orrery/home.html')


def dashboard(request):
    planets = Planet.objects.all()
    comets = Comet.objects.all()
    asteroids = Asteroid.objects.all()

    celestial_bodies = []

    search_query = request.GET.get('search', '')
    if search_query:
        planets = planets.filter(name__icontains=search_query)
        comets = comets.filter(name__icontains=search_query)
        asteroids = asteroids.filter(name__icontains=search_query)

    filter_by = request.GET.get('filter_by', '')
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

    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'name':
        celestial_bodies = sorted(celestial_bodies, key=lambda x: x.name)
    elif sort_by == 'distance_from_earth':
        celestial_bodies = sorted(celestial_bodies, key=lambda x: x.distance)

    context = {
        'celestial_bodies': celestial_bodies,
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
    writer.writerow(['Name', 'Body Type', 'Size (meters)', 'Distance (km)', 'Last Updated', 'Image URL'])

    planets = Planet.objects.all()
    comets = Comet.objects.all()
    asteroids = Asteroid.objects.all()

    for body in planets:
        writer.writerow([body.name, 'Planet', body.size, body.distance, body.last_updated, body.image_url])

    for body in comets:
        writer.writerow([body.name, 'Comet', body.size, body.distance, body.last_updated, body.image_url])

    for body in asteroids:
        body_type = 'PHA' if body.is_potentially_hazardous else 'Asteroid'
        writer.writerow([body.name, body_type, body.size, body.distance, body.last_updated, body.image_url])

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
