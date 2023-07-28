from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .otp import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.


def home_view(request):
    return render(request, 'accounts/home.html')


def accounts_confirmation_view(request):
    return render(request, 'accounts/accounts_confirmation.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('booking:home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate Your BingeBuffer Account'
            message = render_to_string('accounts/accounts_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            subject, from_email, to = mail_subject, 'bingebufferin@gmail.com', to_email
            text_content = render_to_string('accounts/accounts_email.txt', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(message, "text/html")
            msg.content_subtype = "html"
            msg.send()
            return redirect('accounts:confirmation')
        else:
            return render(request, 'accounts/accounts_signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'accounts/accounts_signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:home')
    else:
        return HttpResponse('Activation link is invalid!')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('booking:home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('booking:home')
            else:
                return redirect('accounts:confirmation')
        else:
            return render(request, 'accounts/accounts_login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/accounts_login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
