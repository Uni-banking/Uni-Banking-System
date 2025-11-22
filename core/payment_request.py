from django.shortcuts import render, redirect
from account .models import Unibank, Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal
from core.models import Transaction

@login_required
def search_users_request(request):
    unibank = Unibank.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    account_query = Account.objects.all()
    query = request.POST.get("account_number")
    
    if query:
        account_query = account_query.filter(
            Q(account_number=query),
        ).distinct()
        
    context = {
        "unibank": unibank,
        "account": account,
        "account_query": account_query,
        "query": query,
    }
    
    return render(request, "payment_request/search_user.html", context)

def amount_request(request, account_number):
    unibank = Unibank.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    account_query = Account.objects.get(account_number=account_number)
    
    context = {
        "unibank": unibank,
        "account": account,
        "account_query": account_query,
    }
    
    return render(request, "payment_request/amount-request.html", context)

def amount_request_process(request, account_number):
    account = Account.objects.get(account_number=account_number)
    request_sender = request.user
    request_recipient = account.user
    
    request_sender_account = request.user.account
    request_recipient_account = account
    
    if request.method == "POST":
        amount = request.POST.get("amount-request")
        description = request.POST.get("description")
        
        new_request = Transaction.objects.create(
            user=request.user,
            amount=amount,
            payment_description=description,
            
            sender=request_sender,
            recipient=request_recipient,
            
            sender_account=request_sender_account,
            recipient_account=request_recipient_account,
            
            status="request_processing",
            transaction_type="request",
        )
        new_request.save()
        
        transaction_id = new_request.transaction_id
        
        return redirect("core:amount-request-confirmation", account.account_number, transaction_id)        
    else: 
        messages.warning(request, "Error occurred. Try again later.")
        return redirect("account:dashboard")        

def amount_request_confirmation(request, account_number, transaction_id):
    unibank = Unibank.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    account_query = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        "unibank": unibank,
        "account": account,
        "account_query": account_query,
        "transaction": transaction,
    }
    
    return render(request, "payment_request/amount-request-confirmation.html", context)

def amount_request_dispatch(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number and request.user.account.pin_number == transaction.sender.account.pin_number :
            transaction.status = "request_sent"
            transaction.save()
            messages.success(request, "Your payment request has been sent successfully.")
            return redirect("core:amount-request-completed", account.account_number, transaction.transaction_id)
        else: 
            messages.warning(request, "The provided PIN is incorrect or you are not authorized to perform this action. Please verify your PIN and try again.")
            return redirect("core:transactions")
    else:
        messages.warning(request, "An error occurred, please try again later.") 
        return redirect("account:dashboard")
    
def amount_request_completed(request, account_number, transaction_id):
    unibank = Unibank.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    account_query = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        "unibank": unibank,
        "account": account,
        "account_query": account_query,
        "transaction": transaction,
    }
    
    return render(request, "payment_request/amount-request-completed.html", context)

def settlement_confirmation(request, account_number, transaction_id):
    unibank = Unibank.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    account_query = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        "unibank": unibank,
        "account": account,
        "account_query": account_query,
        "transaction": transaction,
    }
    
    return render(request, "payment_request/settlement-confirmation.html", context)

def settlement_processing(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    sender = request.user
    sender_account = request.user.account
    
    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.amount:
                messages.warning(request, "Insufficient Funds. Please ensure your account is funded and try again.")
            else: 
                sender_account.account_balance -= transaction.amount
                sender_account.save()
                
                account.account_balance += transaction.amount 
                account.save()
                
                transaction.status = "request_settled"
                transaction.save()
                
                messages.success(request, f"Payment request from {account.user. unibank.full_name} was settled successfully.")

                return redirect("core:settlement-completed", account.account_number, transaction.transaction_id)
        else: 
            messages.warning(request, "Incorrect PIN. Please check your PIN and try again.")
            return redirect("core:settlement-confirmation", account.account_number, transaction.transaction_id)
    else: 
        messages.warning(request, "An error occurred. Please try again later.")
        return redirect("account:dashboard")
    
def settlement_completed(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        "account": account,
        "transaction": transaction,
    }
    
    return render(request, "payment_request/settlement-completed.html", context)

def cancel_payment_request(request, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.user.account.account_number == transaction.sender.account.account_number:
        transaction.delete()
        messages.success(request, "Payment request successfully cancelled.")
        return redirect("core:transactions")
    else: 
        messages.warning(request, "You are not authorized to cancel this request.")
        return redirect("core:transactions")
