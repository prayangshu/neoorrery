import csv
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Planet, Comet, Asteroid, CelestialBodyStats, UserProfile, NasaDataLog, RealTimeCloseApproach, BlogPost, Topic, Comment
from .forms import EditProfileForm, UserProfileForm, CustomUserCreationForm, BlogPostForm, CommentForm
from .management.commands.email_close_approaches import Command as EmailCloseApproachesCommand
from .management.commands.fetch_real_time_close_approaches import Command as FetchRealTimeCloseApproachesCommand


@login_required
def dashboard(request):
    """Dashboard view displaying celestial body statistics and real-time close approaches."""
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
    search_query = request.GET.get('table_search', '')
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

    # Fetch real-time close approaches
    close_approaches = RealTimeCloseApproach.objects.filter(is_critical=False)
    critical_approaches = RealTimeCloseApproach.objects.filter(is_critical=True)

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    is_opted_in = user_profile.is_opted_in

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Return only the table section for AJAX calls
        return render(request, 'orrery/table_data.html', {
            'celestial_bodies': celestial_bodies
        })

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
        'close_approaches': close_approaches,
        'critical_approaches': critical_approaches
    }

    return render(request, 'orrery/dashboard.html', context)


@login_required
def profile(request):
    """View displaying the user's profile information."""
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'orrery/profile.html', {'user_profile': user_profile})


@login_required
def edit_profile(request):
    """View allowing users to edit their profile information, including their profile picture."""
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
    elif body_type == 'Asteroid' or body_type == 'PHA':
        body = get_object_or_404(Asteroid, pk=pk)
        template = 'orrery/pha_body_detail.html' if body.is_potentially_hazardous else 'orrery/asteroids_body_detail.html'
    else:
        return HttpResponse('Body type not found', status=404)

    return render(request, template, {'body': body})


@login_required
def toggle_alert_subscription(request):
    """Toggles the user's subscription to close approach alerts."""
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.is_opted_in = not user_profile.is_opted_in
    user_profile.save()

    if user_profile.is_opted_in:
        messages.success(request, 'You have successfully opted into Close Approaches Alert.')
    else:
        messages.success(request, 'You have opted out of Close Approaches Alert.')

    return redirect('dashboard')


@login_required
def email_close_approaches(request):
    """Allows users to manually trigger the email alert for close approaches."""
    if request.method == 'POST':
        email_alert = EmailCloseApproachesCommand()
        email_alert.handle()

        # Log this action
        NasaDataLog.objects.create(user=request.user, action='Requested Close Approaches Email Alert')

        messages.success(request, 'Close Approaches Alert has been sent to your email!')
        return redirect('dashboard')
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required
def fetch_real_time_close_approaches(request):
    """Allows users to fetch real-time close approaches."""
    if request.method == 'POST':
        fetch_approaches = FetchRealTimeCloseApproachesCommand()
        fetch_approaches.handle()

        # Log this action
        NasaDataLog.objects.create(user=request.user, action='Fetched Real-Time Close Approaches')

        messages.success(request, 'Real-Time Close Approaches have been updated!')
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
    """Renders the 3D view of celestial bodies."""
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
    """Handles user signup, including email registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'orrery/signup.html', {'form': form})


@login_required
def nasa_data_logs(request):
    """Displays the NASA data logs."""
    logs = NasaDataLog.objects.all().order_by('-timestamp')
    return render(request, 'orrery/nasa_data_logs.html', {'logs': logs})


# Blog Contribution Views
@login_required
def contribute(request):
    """Allows users to contribute a blog post."""
    topics = Topic.objects.all()  # Fetch topics for the form
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'NOT VERIFIED'  # Set the status to NOT VERIFIED by default
            post.save()

            # Update points for non-verified contributions
            user_profile = request.user.userprofile
            user_profile.points += 25  # Add points for non-verified contribution
            user_profile.save()

            messages.success(request, 'Your blog post has been submitted!')
            return redirect('all_contributions')
    else:
        form = BlogPostForm()

    return render(request, 'orrery/contribute.html', {'form': form, 'topics': topics})


@login_required
def all_contributions(request):
    """Displays all contributions made by users."""
    search_query = request.GET.get('search_query', '')
    contributions = BlogPost.objects.all()

    if search_query:
        contributions = contributions.filter(topic__name__icontains=search_query)  # Search by topic name

    return render(request, 'orrery/all_contributions.html', {'contributions': contributions})


@login_required
def verified_contributions(request):
    """Displays all verified contributions."""
    contributions = BlogPost.objects.filter(status='VERIFIED')[:20]
    return render(request, 'orrery/verified_contributions.html', {'contributions': contributions})


@login_required
def not_verified_contributions(request):
    """Displays all not verified contributions."""
    contributions = BlogPost.objects.filter(status='NOT VERIFIED')[:20]
    return render(request, 'orrery/not_verified_contributions.html', {'contributions': contributions})


@login_required
def my_contributions(request):
    """Displays the user's contributions."""
    contributions = BlogPost.objects.filter(author=request.user)  # Filter contributions by the logged-in user
    return render(request, 'orrery/my_contributions.html', {'contributions': contributions})


@login_required
def delete_contribution(request, pk):
    """Handles the deletion of a user's contribution."""
    contribution = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        contribution.delete()
        messages.success(request, 'Your contribution has been deleted successfully!')
        return redirect('my_contributions')

    return render(request, 'orrery/delete_contribution.html', {'contribution': contribution})


@login_required
def blog_detail(request, pk):
    """Displays a detailed view of a specific blog post and allows comments."""
    blog_post = get_object_or_404(BlogPost, pk=pk)
    comments = blog_post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog_post = blog_post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('blog_detail', pk=pk)
    else:
        comment_form = CommentForm()

    return render(request, 'orrery/blog_detail.html', {
        'blog_post': blog_post,
        'comments': comments,
        'comment_form': comment_form,
    })
