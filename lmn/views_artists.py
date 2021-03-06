from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, ArtistNewPhotoForm
import webbrowser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse


def venues_for_artist(request, artist_pk):   # pk = artist_pk

    ''' Get all of the venues where this artist has played a show '''

    shows = Show.objects.filter(artist=artist_pk).order_by('show_date').reverse() # most recent first
    artist = Artist.objects.get(pk=artist_pk)

    return render(request, 'lmn/venues/venue_list_for_artist.html', {'artist' : artist, 'shows' :shows})


def artist_list(request):
    form = ArtistSearchForm()
    search_name = request.GET.get('search_name')
    if search_name:
        artists = Artist.objects.filter(name__icontains=search_name).order_by('name')
    else:
        artists_list = Artist.objects.all().order_by('name')
        # pagination
        page = request.GET.get('page', 1)

        paginator = Paginator(artists_list, 7)
        try:
            artists = paginator.page(page)
        except PageNotAnInteger:
            artists = paginator.page(1)
        except EmptyPage:
            artists = paginator.page(paginator.num_pages)


    return render(request, 'lmn/artists/artist_list.html', {'artists':artists, 'form':form, 'search_term':search_name})


def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)

    if request.method == 'POST':

        form = ArtistNewPhotoForm(request.POST, request.FILES)
        print('is form valid ' + str(form.is_valid()))
        if form.is_valid():

            artist.photo = request.FILES['photo']
            artist.save()
            return HttpResponseRedirect(reverse('lmn:artist_list'))


    else:
        form = ArtistNewPhotoForm()

    return render(request, 'lmn/artists/artist_detail.html', {'form': form, 'artist': artist})


def delete_artist(request):
    pk = request.POST['artist_pk']
    artist_record = get_object_or_404(Artist, pk=pk)
    artist_record.photo.delete()
    return redirect('lmn:artist_list')
