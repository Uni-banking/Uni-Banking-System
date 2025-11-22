from django.db import models
from user_auths.models import CustomUser
from account.models import Account
from shortuuid.django_fields import ShortUUIDField

TRANSACTION_TYPES = (
    ("transfer", "Transfer"),
    ("receive", "Receieve"),
    ("withdraw", "Withdraw"),
    ("refund", "Refund"),
    ("request", "Payment Request"),
    ("none", "None"),
)

TRANSACTION_STATUS = (
    ("failed", "Failed"),
    ("completed", "Completed"),
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("request_sent", "Request Sent"),
    ("request_processing", "Request Processing"),
    ("request_settled", "Request Settled"),
)

CARD_TYPE = (
    ("master", "Master"),
    ("visa", "Visa"),
    ("verve", "Verve"),
)

class Transaction(models.Model):
    transaction_id = ShortUUIDField(unique=True, length=15, max_length=20, prefix="TRN")
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="user")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_description = models.CharField(max_length=1000, null=True, blank=True)
    
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="sender")
    recipient = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="recipient")
    
    sender_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="sender_account")    
    recipient_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="recipient_account")    
    
    status = models.CharField(choices=TRANSACTION_STATUS, max_length=100, default="pending")
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=100, default="none")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    
    def __str__(self):
        try:
            return f"{self.user}"
        except: 
            return f"Transaction"
        
class CreditCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    card_id = ShortUUIDField(unique=True, length=5, max_length=20, prefix="CARD", alphabet="1234567890")
    
    name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=19) 
    month = models.IntegerField()
    year = models.IntegerField()
    cvc = models.CharField(max_length=4)  
    
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    card_type = models.CharField(choices=CARD_TYPE, max_length=20, default="master")
    card_status = models.BooleanField(default=True)
    
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return f"{self.user}"
    
    