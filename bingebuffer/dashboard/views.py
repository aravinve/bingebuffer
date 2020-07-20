from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from booking.models import Booking, Bookingmeta
import uuid
import io
import json
from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Userprofile, MovieReview

# Create your views here.
@login_required(login_url="/accounts/login")
def dashboard_home(request):
    return render(request, 'dashboard/dashboard_home.html', {'isHome': True})


@login_required(login_url="/accounts/login")
def dashboard_feed(request):
    reviews = MovieReview.objects.filter(review_public_status=True)
    return render(request, 'dashboard/dashboard_feed.html' , {'reviews': reviews})


@login_required(login_url="/accounts/login")
def dashboard_profile(request):
    if request.method == 'POST':
        editProfileForm = forms.EditProfileForm(request.POST, instance=request.user)
        userprofile = Userprofile.objects.get(user=request.user)
        if userprofile is None:
            userProfileForm = forms.UserProfileForm()
        else:
            initialData = {'nickname': userprofile.nickname, 'date_of_birth': userprofile.date_of_birth, 'badge': userprofile.badge}
            userProfileForm = forms.UserProfileForm(initial=initialData)
        if editProfileForm.is_valid():
            editProfileForm.save()
            return render(request, 'dashboard/dashboard_profile.html', {'editProfileForm': editProfileForm, 'userProfileForm': userProfileForm})
        else:
            return render(request, 'dashboard/dashboard_profile.html', {'editProfileForm': editProfileForm, 'userProfileForm': userProfileForm})
           
    else:
        editProfileForm = forms.EditProfileForm(instance=request.user)
        userprofile = Userprofile.objects.get(user=request.user)
        if userprofile is None:
            userProfileForm = forms.UserProfileForm()
        else:
            initialData = {'nickname': userprofile.nickname, 'date_of_birth': userprofile.date_of_birth, 'badge': userprofile.badge}
            userProfileForm = forms.UserProfileForm(initial=initialData)
        return render(request, 'dashboard/dashboard_profile.html', {'editProfileForm': editProfileForm, 'userProfileForm': userProfileForm})

@login_required(login_url="/accounts/login")
def dashboard_userprofile(request):
    if request.method == 'POST':
        userProfileForm = forms.UserProfileForm(request.POST, instance=request.user)
        editProfileForm = forms.EditProfileForm(instance=request.user)
        if userProfileForm.is_valid():
            userprofile = Userprofile(user=request.user, id=request.user, nickname=request.POST['nickname'], date_of_birth=request.POST['date_of_birth'], badge=request.POST['badge'])
            userprofile.save()
            return render(request, 'dashboard/dashboard_profile.html', {'userProfileForm': userProfileForm, 'editProfileForm': editProfileForm})
        else:
            return render(request, 'dashboard/dashboard_profile.html', {'userProfileForm': userProfileForm, 'editProfileForm': editProfileForm})
    else:
        return redirect('dashboard:profile')


@login_required(login_url="/accounts/login")
def dashboard_bookings(request):
    transactions_ids = []
    results = []
    datas = Booking.objects.filter(user=request.user)
    for data in datas:
        transactions_ids.append(data.booking_meta)
    for transaction_id in transactions_ids:
        key = uuid.UUID(str(transaction_id))
        results.append(Bookingmeta.objects.get(transaction_id=key))
    return render(request, 'dashboard/dashboard_content.html', {'results': results})

@login_required(login_url="/accounts/login")
def dashboard_settings(request):
    return render(request, 'dashboard/dashboard_settings.html')

@login_required(login_url="/accounts/login")
def dashboard_ticket_pdf(request, id):
    data = Bookingmeta.objects.get(transaction_id=id)
    response = HttpResponse('application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Ticket_Confirmation.pdf'
    cm = 2.54
    doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=6.5 * cm, topMargin=0.3 * cm, bottomMargin=0)
    elements = []
    data=[('Movie Name',data.movie_name),('Screen Name',data.screen_name), ('Date', data.show_date), ('Show Time', data.show_time), ('Seats', data.seats)]
    table = Table(data, colWidths=270, rowHeights=79)
    elements.append(table)
    doc.build(elements) 
    return response

@login_required(login_url="/accounts/login")
def dashboard_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('dashboard:home')
        else:
            return render(request, 'dashboard/dashboard_passwordchange.html', {'form': form})
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'dashboard/dashboard_passwordchange.html', {'form': form})

@login_required(login_url="/accounts/login")
def dashboard_postreview(request): 
    if request.method == 'POST':
        movie_name = request.POST['movieName']
        movie_rating = request.POST['movieRating']
        movie_review = request.POST['movieReview']
        review_title = request.POST['reviewTitle']
        if request.POST['reviewPublicStatus'] == 'true':
            review_public_status = True
        else:
            review_public_status = False
        review_hastags = request.POST['reviewHashTags']
        movie_id = request.POST['movieId']
        movie_list = json.loads(movie_id)
        review_slug = str(review_title).lower().strip().replace(r'/&/g', '-and-').replace(r'/[\s\W-]+/g', '-')
        movie_data_id = None
        movie_data_posterpath = None
        movie_data_backdroppath = None
        for movie in movie_list:
            if movie['title'] == movie_name:
                movie_data_id = json.dumps(movie['id'])
                movie_data_posterpath = json.dumps(movie['poster_path'])
                movie_data_backdroppath = json.dumps(movie['backdrop_path'])
        movie_review_id = uuid.uuid4()
        review = MovieReview(
            id=movie_review_id, user=request.user, movie_id=movie_data_id, movie_name=movie_name, 
            movie_posterpath=movie_data_posterpath, movie_backdroppath=movie_data_backdroppath, review_hash=review_hastags, review_public_status=review_public_status, review_title=review_title, review_slug=review_slug,
            movie_rating=movie_rating, movie_review=movie_review)
        review.save()
        return redirect('dashboard:feed')

@login_required(login_url="/accounts/login")
def dashboard_reviewdetail(request, reviewId, reviewTitle):
    review = MovieReview.objects.get(id=reviewId)
    review_hashtags = json.loads(review.review_hash)
    poster_path = review.movie_posterpath.strip('\"')
    backdrop_path = review.movie_backdroppath.strip('\"')
    request.session['page'] = 1;
    request.session['dataType'] = "now_playing";
    return render(request, 'dashboard/dashboard_reviewdetail.html', {'reviewId': reviewId, 'reviewTitle': reviewTitle, 'review': review, 'review_hashtags': review_hashtags, 'poster_path': poster_path,'backdrop_path': 'https://image.tmdb.org/t/p/original/{}'.format(backdrop_path)})