import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Venue, City, Category
from .forms import VenueForm
from account.models import Profile

# Create your views here.
@login_required(login_url='/auth/login')
def show_main(request): 
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('authentication:register') 

    is_owner_role = user_profile.is_owner if user_profile else False

    cities = City.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    types = Venue.TYPE_CHOICES

    context = {
        'profile': user_profile,
        'is_owner_role': is_owner_role,
        'user': request.user,
        'cities': cities,
        'categories': categories,
        'types': types,
    }

    return render(request, "venue_main.html", context)

def show_details(request, id):
    venue = get_object_or_404(Venue, pk=id)
    context = {
        'venue': venue,
        'user': request.user,
    }
    return render(request, "venue_details.html", context)

@require_http_methods(["GET"])
def get_venues_json(request):
    venues = Venue.objects.select_related('owner__user', 'city', 'category').all()
    
    data = []
    for venue in venues:
        data.append({
            'id': venue.id,
            'name': venue.name,
            'price': venue.price,
            'city_name': venue.city.name, # Kirim nama, bukan objek
            'category_name': venue.category.name, # Kirim nama, bukan objek
            'type': venue.type,
            'address': venue.address,
            'description': venue.description,
            'image_url': venue.image_url,
            'owner_profile_pk': str(venue.owner_id), # Kirim PK profile sbg string
            'owner_username': venue.owner.user.username,
        })
        
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def get_venue_json_by_id(request, id):
    venue = get_object_or_404(Venue, pk=id)
    
    data = {
        'id': venue.id,
        'name': venue.name,
        'price': venue.price,
        'type': venue.type,
        'city': venue.city.name, 
        'category': venue.category.name,
        'address': venue.address,
        'description': venue.description,
        'image_url': venue.image_url,
    }
    return JsonResponse(data)

@login_required(login_url='/auth/login')
@require_http_methods(["POST"])
def add_venue_ajax(request):
    if not request.user.profile.is_owner:
        return JsonResponse({'error': 'You must be an owner to add a venue.'}, status=403)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    form = VenueForm(data)
    if form.is_valid():
        # Form valid, simpan data
        venue = form.save(commit=False)
        venue.owner = request.user.profile
        venue.save()
        return JsonResponse({'status': 'success', 'id': venue.id}, status=201)
    else:
        # Form tidak valid, kirim error validasi
        return JsonResponse(form.errors, status=400)

@login_required(login_url='/auth/login')
@require_http_methods(["PUT"])
def edit_venue_ajax(request, id):
    try:
        venue = get_object_or_404(Venue, pk=id)
    except Venue.DoesNotExist:
         return JsonResponse({'error': 'Venue not found.'}, status=404)

    if venue.owner != request.user.profile:
        return JsonResponse({'error': 'You do not have permission to edit this venue.'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    
    form = VenueForm(data, instance=venue)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'id': venue.id}, status=200)
    else:
        # Form tidak valid, kirim error
        return JsonResponse(form.errors, status=400)

@login_required(login_url='/auth/login')
@require_http_methods(["DELETE"])
def delete_venue_ajax(request, id):
    try:
        venue = get_object_or_404(Venue, pk=id)
    except Venue.DoesNotExist:
         return JsonResponse({'error': 'Venue not found.'}, status=44)

    if venue.owner != request.user.profile:
        return JsonResponse({'error': 'You do not have permission to delete this venue.'}, status=403)

    venue.delete()
    return JsonResponse({'status': 'success', 'message': 'Venue deleted successfully.'}, status=200)