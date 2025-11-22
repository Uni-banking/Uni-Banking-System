from django.shortcuts import render, redirect
from core.models import Transaction
from account.models import Unibank, Account
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def transaction_list(request): 
    unibank = Unibank.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    
    sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by("-id")
    recipient_transaction = Transaction.objects.filter(recipient=request.user, transaction_type="transfer").order_by("-id")
    
    request_sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request").order_by("-id")
    request_recipient_transaction = Transaction.objects.filter(recipient=request.user, transaction_type="request").order_by("-id")
    
    context = {
        "unibank": unibank,
        "account": account,
        "sender_transaction": sender_transaction,
        "recipient_transaction": recipient_transaction,
        "request_recipient_transaction":request_recipient_transaction,
        "request_sender_transaction": request_sender_transaction,
    }
    
    return render(request, "transaction/transaction-list.html", context)

@login_required
def transaction_detail(request, transaction_id): 
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        "transaction": transaction,
    }
    
    return render(request, "transaction/transaction-detail.html", context) 