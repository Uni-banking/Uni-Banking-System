from django.shortcuts import render, redirect
from account .models import Unibank, Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal
from core.models import Transaction

@login_required
def search_users_by_account_number(request):
    
    unibank = Unibank.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    account_query = Account.objects.all()
    query = request.POST.get("account_number")
    
    if query:
        account_query = account_query.filter(
            Q(account_number=query)|
            Q(account_id=query) 
        ).distinct()
    
    context = {
        "unibank": unibank,
        "account": account,
        "account_query": account_query,
        "query": query,
    }
    return render(request, "transfer/search-user-by-account-number.html", context)

def amount_transfer(request, account_number):
    unibank = Unibank.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    
    try:
        account_query = Account.objects.get(account_number=account_number)
    except: 
        messages.warning(request, "Account does not exist.")
        return redirect("core:search-account")
    
    context = { 
        "unibank": unibank,
        "account": account,
        "account_query": account_query,
    }
    return render(request, "transfer/amount-transfer.html", context)
    
def amount_transfer_process(request, account_number): 
    account = Account.objects.get(account_number=account_number) 
    sender = request.user
    recipient = account.user
    
    sender_account = request.user.account 
    recipient_account = account 
    
    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")
        
        if sender_account.account_balance >= Decimal(amount):
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                payment_description=description,
                sender=sender,
                recipient=recipient,
                sender_account=sender_account,
                recipient_account=recipient_account,
                status="processing",
                transaction_type="transfer",
            )
            new_transaction.save()
            
            # Get ID of newly created transaction
            transaction_id = new_transaction.transaction_id
            return redirect("core:transfer-confirmation", account.account_number, transaction_id)
        else: 
            messages.warning(request, "Insufficient Funds.")
            return redirect("core:amount-transfer", account.account_number)
    else:
            messages.warning(request, "Error occurred. Try again later.")
            return redirect("account:account")
             
def transfer_confirmation(request, account_number, transaction_id):
    unibank = Unibank.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    
    try: 
        account_query = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transaction does not exist.")
        return redirect("account:account")
    
    context = {
        "unibank": unibank,
        "account": account,
        "account_query": account_query,
        "transaction": transaction,
    }
    return render(request, "transfer/transfer-confirmation.html", context)

def transfer_process(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    sender = request.user
    recipient = account.user
    
    sender_account = request.user.account 
    recipient_account = account 
    
    completed = False
    
    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        
        if pin_number == sender_account.pin_number:
            transaction.status = "completed"
            transaction.save()

            sender_account.account_balance -= transaction.amount
            sender_account.save()
            
            account.account_balance += transaction.amount
            account.save()
            
            messages.success(request, "Transfer Successful.")
            return redirect("core:transfer-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Incorrect Pin Number")
            return redirect("core:transfer-confirmation", account.account_number, transaction.transaction_id)
    else: 
        messages.warning(request, "An error occurred, try again later.")
        return redirect("account:account")

def transfer_completed(request, account_number, transaction_id):
    unibank = Unibank.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    
    try: 
        account_query = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transfer does not exist.")
        return redirect("account:account")
    
    context = {
        "unibank": unibank,
        "account": account,
        "account_query": account_query,
        "transaction": transaction,
    }
    return render(request, "transfer/transfer-completed.html", context)