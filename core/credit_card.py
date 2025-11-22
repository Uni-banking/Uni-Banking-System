from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CreditCard
from account.models import Account
from decimal import Decimal

def card_detail(request, card_id):
    card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = Account.objects.get(user=request.user)
    
    context = {
        "card":card,
        "account":account,
    }
    return render(request, "cards/card-details.html", context)

def fund_card(request, card_id):
    card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = request.user.account 
    
    if request.method =="POST":
        amount = request.POST.get("funding-amount")
        
        if Decimal(amount) <= account.account_balance: 
            account.account_balance -= Decimal(amount)
            account.save()
            
            card.amount += Decimal(amount)
            card.save()
            
            messages.success(request, "Card funded successfully.")
            return redirect('core:card-details', card.card_id)
        else: 
            messages.warning(request, "Insufficient funds.")
            return redirect('core:card-details', card.card_id)

def withdraw_from_card(request, card_id):
    card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = request.user.account 
    
    if request.method == "POST":
        withdrawal_amount = request.POST.get("amount")
        if Decimal(withdrawal_amount) <= card.amount:
            card.amount -= Decimal(withdrawal_amount)
            card.save()
            
            account.account_balance += Decimal(withdrawal_amount)
            account.save()
            
            messages.success(request, "Withdrawal completed successfully")
            return redirect('account:dashboard')
        else: 
            messages.warning(request, "Insufficient funds.")
            return redirect('core:card-details', card.card_id)

def remove_card(request, card_id):
    card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = request.user.account 

    if card.amount > 0: 
        account.account_balance += card.amount
        account.save()
        
        card.delete()
        
        messages.success(request, "Card removed successfully")
        return redirect("account:dashboard")
    else:    
        card.delete()
            
        messages.success(request, "Card removed successfully")
        return redirect("account:dashboard")