import logging

from django.shortcuts import render, redirect
from account.models import Unibank, Account
from account.forms import KYCForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard


logger = logging.getLogger(__name__)


# @login_required
def AccountView(request):
    if request.user.is_authenticated:
        try:
            unibank = Unibank.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your Unibank.")
            return redirect("account:unibank-reg")

        account = Account.objects.get(user=request.user)
    else: 
        messages.warning(request, "You need to login to access the dashboard.")
        return redirect("user_auths:sign-in")
    
    context = {
        "unibank": unibank,
        "account": account,
    }
    return render(request, "account/account.html", context)

@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)
    
    try: 
        unibank = Unibank.objects.get(user=user)
    except: 
        unibank = None
        
    if request.method == 'POST':
        form = UnibankForm(request.POST, request.FILES, instance=unibank)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "Your Unibank form has been successfully submitted and is currently pending review.")
            return redirect("core:index")
    else:
        form = UnibankForm(instance=unibank)
    context = {
        "account": account,
        "form": form,
        "unibank": unibank,
    }
    return render(request, "account/unibank-form.html", context)

def dashboard(request):
    
    if request.user.is_authenticated:
        try:
            unibank = Unibank.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your Unibank.")
            return redirect("account:unibank-reg")

        account = Account.objects.get(user=request.user)
        credit_cards = CreditCard.objects.filter(user=request.user).order_by("-id")
        
        if request.method == "POST":
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user 
                new_form.save()
                
                card_id = new_form.card_id
                messages.success(request, "Card has been added successfully.")
                return redirect("account:dashboard")
            else:
                messages.error(request, "There was an error adding your card. Please check the details and try again.")
        else: 
            form = CreditCardForm(request.POST)     
    else: 
        messages.warning(request, "You need to login to access the dashboard.")
        return redirect("user_auths:sign-in")

    context = {
        "CreditCardForm": form,
        "unibank": unibank,
        "account": account,
        "credit_cards": credit_cards
    }
    return render(request, "account/dashboard.html", context) 
