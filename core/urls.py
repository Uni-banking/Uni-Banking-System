from django.urls import path
from core import views, transfer, transaction , payment_request, credit_card

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    
    # Money Transfers
    path("search-account/", transfer.search_users_by_account_number, name="search-account"),
    path("amount-transfer/<account_number>/", transfer.amount_transfer, name="amount-transfer"),
    path("amount-transfer-process/<account_number>/", transfer.amount_transfer_process, name="amount-transfer-process"),
    path("transfer-confirmation/<account_number>/<transaction_id>/", transfer.transfer_confirmation, name="transfer-confirmation"),
    path("transfer-process/<account_number>/<transaction_id>/", transfer.transfer_process, name="transfer-process"),
    path("transfer-completed/<account_number>/<transaction_id>/", transfer.transfer_completed, name="transfer-completed"),

    # Transactions
    path("transactions/", transaction.transaction_list, name="transactions"),
    path("transaction-detail/<transaction_id>", transaction.transaction_detail, name="transaction-detail"),
    
    # Paymennt Requests
    path("request-search-users/", payment_request.search_users_request, name="request-search-users"),
    path("amount-request/<account_number>/", payment_request.amount_request, name="amount-request"),
    path("amount-request-process/<account_number>/", payment_request.amount_request_process, name="amount-request-process"),
    path("amount-request-confirmation/<account_number>/<transaction_id>/", payment_request.amount_request_confirmation, name="amount-request-confirmation"),
    path("amount-request-dispatch/<account_number>/<transaction_id>/", payment_request.amount_request_dispatch, name="amount-request-dispatch"),
    path("amount-request-completed/<account_number>/<transaction_id>/", payment_request.amount_request_completed, name="amount-request-completed"),
    
    # Payment Request Settlement 
    path("settlement-confirmation/<account_number>/<transaction_id>/", payment_request.settlement_confirmation, name="settlement-confirmation"),
    path("settlement-processing/<account_number>/<transaction_id>/", payment_request.settlement_processing, name="settlement-processing"),
    path("settlement-completed/<account_number>/<transaction_id>/", payment_request.settlement_completed, name="settlement-completed"),

    # Delete Payment Request 
    path("cancel-payment-request/<transaction_id>/", payment_request.cancel_payment_request, name="cancel-payment-request"),

    # Card Details
    path("card/<card_id>/", credit_card.card_detail, name="card-details"),
    path("fund-card/<card_id>/", credit_card.fund_card, name="fund-card"),  
    path("withdraw-from-card/<card_id>/", credit_card.withdraw_from_card, name="withdraw-from-card"),      
    path("remove-card/<card_id>/", credit_card.remove_card, name="remove-card"),    
]
