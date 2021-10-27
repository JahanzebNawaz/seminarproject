from django.db import models  # noqa: F401
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from django.core.validators import RegexValidator
from datetime import date, datetime
from django.core.exceptions import ValidationError


class BaseModel(models.Model):

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


def upload_profile(instance, filename):
    return "Profiles/{user}/{filename}".format(user='{0}_{1}'.format(instance.first_name, instance.last_name),
                                               filename=filename)

GENDER = [('Male', 'Male'), ('Female', "Female")]
 


class User(AbstractUser):
    # first_name
    # last_name
    # password
    # password2
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(
                        upload_to=upload_profile,
                        default='Profiles/user/user.png',
                        null=True, blank=True
    )

    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return self.email




class UserKyc(BaseModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_kyc', verbose_name='User')
    kyc_documents = models.FileField(upload_to='uploads/KYC/%Y/%m/%d/',)
    is_approved = models.BooleanField(default=False, null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    comments = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = 'KYC Document'

    def __str__(self) -> str:
        return self.user.username


class Customer(BaseModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_user', verbose_name='User')
    date_of_birth = models.DateField(default='2000-01-01')
    phoneNumberRegex = RegexValidator(regex = r"^\+?46?\d{8,15}$")
    phone_no = models.CharField(validators = [phoneNumberRegex], max_length = 14)
    age = models.PositiveIntegerField(default=18)
    gender = models.CharField(max_length=15, choices=GENDER, verbose_name='Gender')
    address = models.CharField(max_length=150, null=True, blank=True)
    credit_card = models.CharField(max_length=14, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    # profile_image = models.ImageField(
    #                     upload_to=upload_profile,
    #                     default='Profiles/user/user.png',
    #                     null=True, blank=True
    # )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username



class Currencies(BaseModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=4, unique=True)
    total_amount = models.PositiveBigIntegerField(default=100000000)
    remaining_amount = models.PositiveBigIntegerField()
    rate = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = 'Currencie'
    
    def __str__(self) -> str:
        return '{}'.format(self.currency)
    



class Wallet(BaseModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallet_user', verbose_name='User')
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE, related_name='wallet_currency', verbose_name='Currency')
    balance = models.PositiveBigIntegerField(default=0)


    class Meta:
        verbose_name = 'Wallet'
        unique_together = ('user', 'currency',)

    def __str__(self) -> str:
        return '{} Wallet'.format(self.user.username)


class Proposals(BaseModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals', verbose_name='User')
    currency = models.CharField(max_length=4, verbose_name='Currency Name', help_text='Max limit is 4 (Alphabets, Digits)')
    balance = models.PositiveBigIntegerField(default=0, verbose_name='Total Balance', help_text='max amount 100 000 000')
    details = models.TextField(max_length=2000, null=True, blank=True )
    files = models.FileField(upload_to='uploads/proposals/%Y/%m/%d/', default='')


    class Meta:
        verbose_name = 'Proposal'

    def __str__(self) -> str:
        return 'New Currency {} Proposals'.format(self.currency)



class Tutorials(BaseModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutorial_user', verbose_name='User')
    title = models.CharField(max_length=200)
    details = models.TextField(max_length=2000, null=True)
    url = models.URLField(max_length=250, null=True)

    class Meta:
        verbose_name = 'Tutorial'

    def __str__(self) -> str:
        return '{}'.format(self.title)



class WatchList(BaseModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_list_user', verbose_name='User')
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE, related_name='watch_list_currency', verbose_name='Currency')
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Watch List'

    def __str__(self) -> str:
        return '{}'.format(self.currency)



class SellOrder(BaseModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sell_order_user', verbose_name='User')
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE, related_name='sell_order_amount', verbose_name='Currency')
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    sell_rate = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = 'Sell Order'

    def __str__(self) -> str:
        return '{}'.format(self.currency)




class Transactions(BaseModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_user', verbose_name='User')
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE, related_name='transaction_currency', verbose_name='Currency')
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    sell_rate = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Transaction'

    def __str__(self) -> str:
        return '{}'.format(self.currency)


