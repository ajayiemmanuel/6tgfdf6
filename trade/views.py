from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from .forms import UserRegistrationForm, UserLoginForm, SetPasswordForm, PasswordResetForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from .models import *
from .forms import *
from django.http import HttpResponse
# Create your views here.
from typing import Protocol
from django.core.mail import send_mail
from django.conf import settings
from django.conf import settings


def index(request):
    context = {}
    return render (request, "trade/index.html", context)


def about(request):
    context = {}
    return render (request, "trade/about.html", context)

@login_required (login_url = "login")
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render (request, "trade/change_password.html", {'form': form})

@login_required (login_url = "login")
def dashboard(request):
    user = request.user

    bitcoin = Bitcoin.objects.filter(user=user)
    banktransfer = Banktransfer.objects.filter(user=user)
    transfer = Transfer.objects.filter(user=user)

    context = {'bitcoin':bitcoin, 'banktransfer' :banktransfer, 'transfer' :transfer}
    return render (request, "trade/dashboard.html", context)

@login_required (login_url = "login")
def deposit_wallet(request):
    context = {}
    return render (request, "trade/deposit_wallet.html", context)

@login_required (login_url = "login")
def deposit(request):
    depositlist = request.user.depositlist
    form = DepositlistForm (instance = depositlist)

    if request.method == 'POST':
        form = DepositlistForm (request.POST, request.FILES, instance = depositlist)
        if form.is_valid ():
            form.save ()

    context = {'form': form}
    return render (request, "trade/deposit.html", context)

@login_required (login_url = "login")
def interest_wallet(request):
    context = {}
    return render (request, "trade/interest_wallet.html", context)

@login_required (login_url = "login")
def interest(request):
    context = {}
    return render (request, "trade/interest.html", context)

@login_required (login_url = "login")
def invest(request):
    context = {}
    return render (request, "trade/invest.html", context)


def investment(request):
    context = {}
    return render (request, "trade/investment.html", context)

@login_required (login_url = "login")
def log(request):
    context = {}
    return render (request, "trade/log.html", context)

@user_not_authenticated
def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("dashboard")

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                
                messages.error(request, error) 

    form = UserLoginForm()

    return render(
        request=request,
        template_name="trade/login.html",
        context={"form": form}
        )

@login_required (login_url = "login")
def manual(request):
    depositlistimage = request.user.depositlistimage
    form = DepositlistimageForm (instance = depositlistimage)

    if request.method == 'POST':
        form = DepositlistimageForm (request.POST, request.FILES, instance = depositlistimage)
        if form.is_valid ():
            form.save ()

    context = {'form': form} 
    return render (request, "trade/manual.html", context)

@login_required (login_url = "login")
def new(request):
    user = request.user

    ticket = user.ticket_set.all()

    if request.method == 'POST':
        data = request.POST
        name = request.POST.getlist('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        picture = request.POST.get('picture')
        status = request.POST.get('status')



        ticket, created = Ticket.objects.get_or_create(
            user=user,
            name=name,
            email=email,
            subject=subject,
            message=message,
            picture=picture,
            status=status
            )
        
        return redirect('ticket')

    context = {'ticket':ticket}  
    return render (request, "trade/new.html", context)


def partners(request):
    context = {}
    return render (request, "trade/partners.html", context)

@login_required (login_url = "login")
def plan(request):
    context = {}
    return render (request, "trade/plan.html", context)

@login_required (login_url = "login")
def preview(request):

    return render (request, "trade/preview.html")

@login_required (login_url = "login")
def profile_setting(request):
    customer = request.user.customer
    form = CustomerForm (instance = customer)

    if request.method == 'POST':
        form = CustomerForm (request.POST, request.FILES, instance = customer)
        if form.is_valid ():
            form.save ()

    context = {'form': form}
    return render (request, "trade/profile_setting.html", context)

@login_required (login_url = "login")
def promotional_tool(request):
    context = {}
    return render (request, "trade/promotional_tool.html", context)

@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="trade/register.html",
        context={"form": form}
        )

def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")


@user_not_authenticated
def reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("trade/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('login')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="trade/reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'trade/change_password.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("login")

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('login')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("trade/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def template_activate_account(request):
    context = {}
    return render (request, "trade/template-activate-account.html", context)

def subscribe(request):
    context = {}
    return render (request, "trade/subscribe.html", context)


def support(request):
    context = {}
    return render (request, "trade/support.html", context)

def terms(request):
    context = {}
    return render (request, "trade/terms.html", context)

@login_required (login_url = "login")
def ticket(request):
    user = request.user

    ticket = Ticket.objects.filter(user=user)
    context = {'ticket':ticket}
    return render (request, "trade/ticket.html", context)

@login_required (login_url = "login")
def transfer_balance(request):
    user = request.user

    transfer = user.transfer_set.all()

    if request.method == 'POST':
        data = request.POST
        name = request.POST.getlist('name')
        wallet = request.POST.getlist('wallet')
        amount = request.POST.get('amount')
        time = request.POST.get('time')
        transactionid = request.POST.get('transactionid')
        status = request.POST.get('status')
        rate = request.POST.get('rate')


        transfer, created = Transfer.objects.get_or_create(
            user=user,
            name=name,
            wallet=wallet,
            amount=amount,
            time=time,
            transactionid=transactionid,
            status=status,
            rate=rate
            )
        
        return redirect('pin')

    context = {'transfer':transfer}  
    return render (request, "trade/transfer_balance.html", context)

@login_required (login_url = "login")
def twofactor(request):
    context = {}
    return render (request, "trade/twofactor.html", context)

@login_required (login_url = "login")
def users(request):
    context = {}
    return render (request, "trade/users.html", context)

@login_required (login_url = "login")
def withdraw(request):
    context = {}
    return render (request, "trade/withdraw.html", context)

@login_required (login_url = "login")
def history(request):
    user = request.user

    bitcoin = Bitcoin.objects.filter(user=user)
    banktransfer = Banktransfer.objects.filter(user=user)

    context = {'bitcoin':bitcoin, 'banktransfer' :banktransfer}
    return render (request, "trade/history.html", context)

@login_required (login_url = "login")
def bitcoin(request):
    user = request.user

    bitcoin = user.bitcoin_set.all()

    if request.method == 'POST':
        data = request.POST
        name = request.POST.getlist('name')
        wallet = request.POST.getlist('wallet')
        address = request.POST.get('address')
        amount = request.POST.get('amount')
        purpose = request.POST.get('purpose')
        time = request.POST.get('time')
        transactionid = request.POST.get('transactionid')
        status = request.POST.get('status')
        rate = request.POST.get('rate')


        bitcoin, created = Bitcoin.objects.get_or_create(
            user=user,
            name=name,
            wallet=wallet,
            address=address,
            amount=amount,
            purpose=purpose,
            time=time,
            transactionid=transactionid,
            status=status,
            rate=rate
            )
        
        return redirect('pin')

    context = {'bitcoin':bitcoin}  
    return render (request, "trade/bitcoin.html", context)

@login_required (login_url = "login")
def banktransfer(request):
    user = request.user

    banktransfer = user.banktransfer_set.all()

    if request.method == 'POST':
        data = request.POST
        name = request.POST.getlist('name')
        wallet = request.POST.getlist('wallet')
        bank = request.POST.get('bank')
        accountnumber = request.POST.get('accountnumber')
        swift = request.POST.get('swift')
        amount = request.POST.get('amount')
        purpose = request.POST.get('purpose')
        time = request.POST.get('time')
        transactionid = request.POST.get('transactionid')
        status = request.POST.get('status')
        rate = request.POST.get('rate')



        banktransfer, created = Banktransfer.objects.get_or_create(
            user=user,
            name=name,
            wallet=wallet,
            bank=bank,
            accountnumber=accountnumber,
            swift=swift,
            amount=amount,
            purpose=purpose,
            time=time,
            transactionid=transactionid,
            status=status,
            rate=rate
            )
        
        return redirect('pin')

    context = {'banktransfer':banktransfer} 
    return render (request, "trade/banktransfer.html", context)


@login_required (login_url = "login")
def pin(request):
    context = {}
    return render (request, "trade/pin.html", context)

@login_required (login_url = "login")
def processing(request):
    context = {}
    return render (request, "trade/processing.html", context)

def privacy(request):
    context = {}
    return render (request, "trade/privacy.html", context)

def terms_condition(request):
    context = {}
    return render (request, "trade/terms_condition.html", context)