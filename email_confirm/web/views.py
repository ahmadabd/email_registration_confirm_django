from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm
from django.contrib.auth import authenticate
from .models import User, ConfirmMail
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required       # for login_required
import random
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

# Create your views here.

def index(request):
    return render(request, 'index.html')


@csrf_exempt
def signup(request):
    # signUp new Usre, after storing user makes Token of User and sends it to users mail address

    if request.method == 'POST':

        # stores datas of localhost:8000/register in form
        form = SignUpForm(request.POST)

        if form.is_valid():     # TODO: make else for if

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            usr = authenticate(username=username, password=raw_password)

            this_user = User.objects.get(username = username)

            # Verification Code
            confirm_rand_str = random.randint(100, 9999)
            ConfirmMail.objects.create(user = this_user, code = confirm_rand_str)

            # sends to user its token
            send_mail(
                'Remember Me Support',                               # subject
                '{}, Verification code is: {}'.format(this_user, confirm_rand_str),    # content
                'remembermealux@gmail.com',                          # From
                [email],                                             # To
                fail_silently = False,
            )

            url = get_random_string(length=12)

            return redirect('activeRegistration', url)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form })


@csrf_exempt
def activeRegistration(request, url):

    if request.method == 'POST':

        form = request.POST

        code = ConfirmMail.objects.filter(code = form['code'])

        for i in range(len(code)):
            if code[i].code == form['code']:

                user = code[i].user
                email = User.objects.filter(username = user)[i].email

                # delete this code row from db
                ConfirmMail.objects.filter(code = form['code']).delete()

                user.is_active = True
                user.save()

                return redirect('login')
            else:
                return redirect('activeRegistration')
    else:
        return render(request, 'registration/verification.html')
