from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, VenueNewPhotoForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect
from django.urls import reverse

# pagination : https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse


def venue_list(request):

    form = VenueSearchForm()
    search_name = request.GET.get('search_name')

    if search_name:
        #search for this venue, display results
        venues = Venue.objects.filter(name__icontains=search_name).order_by('name')
    else :
        venue_list = Venue.objects.all().order_by('name')   # Todo paginate
        #user_list = Venue.objects.all().order_by('name')  # Todo paginate

        page = request.GET.get('page', 1)

        paginator = Paginator(venue_list, 7)
        try:
            venues = paginator.page(page)
        except PageNotAnInteger:
            venues = paginator.page(1)
        except EmptyPage:
            venues = paginator.page(paginator.num_pages)

    return render(request, 'lmn/venues/venue_list.html', { 'venues' : venues, 'form':form, 'search_term' : search_name })


def artists_at_venue(request, venue_pk):   # pk = venue_pk

    ''' Get all of the artists who have played a show at the venue with pk provided '''

    shows = Show.objects.filter(venue=venue_pk).order_by('show_date').reverse() # most recent first
    venue = Venue.objects.get(pk=venue_pk)

    return render(request, 'lmn/artists/artist_list_for_venue.html', {'venue' : venue, 'shows' :shows})



def venue_detail(request, venue_pk):

    venue = get_object_or_404(Venue, pk=venue_pk)

    if request.method == 'POST':

        form = VenueNewPhotoForm(request.POST, request.FILES)
        print('is form valid ' + str(form.is_valid()))
        if form.is_valid():
            venue.photo = request.FILES['photo']
            venue.save()
            return HttpResponseRedirect(reverse('lmn:venue_list'))

    else:
        form = VenueNewPhotoForm()

    return render(request, 'lmn/venues/venue_detail.html', {'form': form, 'venue': venue})


def delete_venue(request):
    pk = request.POST['venue_pk']
    venue_record = get_object_or_404(Venue, pk=pk)
    venue_record.photo.delete()
    return redirect('lmn:venue_list')

