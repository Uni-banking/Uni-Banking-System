from django.db import models
import uuid 
from shortuuid.django_fields import ShortUUIDField
from user_auths.models import CustomUser
from django.db.models.signals import post_save

ACCOUNT_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("inactive", "Inactive")
)

MARITAL_STATUS = (
    ("married", "Married"),
    ("single", "Single"),
    ("other", "Other")
)

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)

IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_license", "Driver's License"),
    ("international_passport", "International Passport")
)



def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s" % (instance.id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)

class Account(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) 
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) #123 345 789 102
    account_number = ShortUUIDField(unique=True, length=10, max_length=25, prefix="217", alphabet="1234567890") #2175893745
    account_id = ShortUUIDField(unique=True, length=7, max_length=25, prefix="DEX", alphabet="1234567890") #DEX7386
    pin_number = ShortUUIDField(unique=True, length=4, max_length=7, alphabet="1234567890") # e.g., 9376 
    ref_code = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh1234567890")
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default="inactive")
    date = models.DateTimeField(auto_now_add=True)      
    unibank_submitted = models.BooleanField(default=False)
    unibank_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="recommended_by")
    
    class Meta: 
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user}"
    
class Unibank(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="unibank", default="default.jpg")
    nationality = models.CharField(max_length=100)
    marital_status = models.CharField(choices=MARITAL_STATUS, max_length=40)
    gender = models.CharField(choices=GENDER, max_length=40)    
    identity_type = models.CharField(choices=IDENTITY_TYPE, max_length=140)
    identity_image = models.ImageField(upload_to="unibank", null=True, blank=True)
    date_of_birth = models.DateTimeField(auto_now_add=False)
    signature = models.ImageField(upload_to="unibank")
    
    # Address
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # Contact Detail
    mobile = models.CharField(max_length=1000)
    fax = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}"
    
def create_account(sender, instance, created, **kwargs):
    if created: 
        Account.objects.create(user=instance)
        
def save_account(sender, instance, **kwargs):
    instance.account.save()
    
post_save.connect(create_account, sender=CustomUser)
post_save.connect(save_account, sender=CustomUser)


