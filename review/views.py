from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from venue.models import Venue
from review.forms import ReviewForm

@login_required(login_url='/login')
def add_review(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    
    form = ReviewForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        review = form.save(commit=False)
        
        review.user = request.user
        review.venue = venue
        review.save()
        
        return redirect('venue_detail', pk=venue.id)

    context = {
        'form': form,
        'venue': venue
    }

    return render(request, "review/add_review.html", context)